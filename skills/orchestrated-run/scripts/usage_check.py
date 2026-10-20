#!/usr/bin/env python3
"""Compare a Cursor usage export with the model database plan addend.

usage_check.py EXPORT [--db PATH] [--guess MODEL@EFFORT=COUNT]...

Reads a Cursor token-usage HTML export and the model database. For each
database model it prints event counts, dollars, and dollar-weighted dollars
per million total tokens, for included-in-plan, for on-demand, and pooled,
beside the plan addend. The rate is total dollars divided by total tokens,
times one million. Included-in-plan is the export kind Included. On-demand is
On-Demand. Free, errored, and aborted rows stay out.

A usage name matches a database model when it is that model plus an effort,
with an optional -thinking before the effort and an optional -fast at the end.
The plan addend is tokenRatePerMillion, or zero when the model name starts
with a prefix in exempt.

A database row with no tokensPerTask needs --guess. The report uses that
count, says it is a guess, and shows the fee the plan addend produces. The
database defaults to ~/.agent-runs/models.json, or the skill's
templates/models.json when that is missing. This command does not write the
database or the model choices file.
"""
import json, sys
from pathlib import Path

from model_setup import AGENT_RUNS, EFFORTS, SKILL

KINDS = {"Included": "included", "On-Demand": "ondemand"}
BUCKETS = ("included", "ondemand", "pooled")


def database(path):
    machine = AGENT_RUNS / "models.json"
    path = Path(path) if path else (machine if machine.exists() else SKILL / "templates" / "models.json")
    return path, json.loads(path.read_text())


def load_export(path):
    text = Path(path).read_text()
    marker = "const DATA = "
    start = text.find(marker)
    if start < 0:
        sys.exit(f"{path}: no usage data")
    try:
        data, _ = json.JSONDecoder().raw_decode(text, start + len(marker))
    except json.JSONDecodeError as error:
        sys.exit(f"{path}: {error}")
    for key in ("models", "kinds", "events"):
        if key not in data:
            sys.exit(f"{path}: usage data has no {key}")
    return data


def resolve(name, models):
    base = name[:-5] if name.endswith("-fast") else name
    for effort in EFFORTS:
        suffix = "-" + effort
        if base.endswith(suffix):
            base = base[: -len(suffix)]
            break
    if base.endswith("-thinking"):
        base = base[: -len("-thinking")]
    return base if base in models else None


def addend(model, plan):
    rate = plan.get("tokenRatePerMillion") or 0
    if any(model.startswith(prefix) for prefix in plan.get("exempt", [])):
        return 0
    return rate


def money(n):
    return f"${n:.2f}"


def rate(dollars, tokens):
    if not tokens:
        return "-"
    per = dollars / tokens * 1e6
    return f"${per:.2f}" if per >= 0.01 else f"${per:.4f}"


def blank():
    return dict(events=0, dollars=0.0, tokens=0)


def main(args):
    export, db_path, guesses = None, None, {}
    while args:
        flag, args = args[0], args[1:]
        if flag == "--db":
            if not args:
                sys.exit(__doc__)
            db_path, args = args[0], args[1:]
        elif flag == "--guess":
            if not args:
                sys.exit(__doc__)
            value, args = args[0], args[1:]
            model, _, rest = value.partition("@")
            effort, _, count = rest.partition("=")
            if not model or effort not in EFFORTS or not count:
                sys.exit(f"--guess must be MODEL@EFFORT=COUNT, not {value}")
            guesses[(model, effort)] = float(count)
        elif flag.startswith("--"):
            sys.exit(__doc__)
        elif export is None:
            export = flag
        else:
            sys.exit(__doc__)
    if export is None:
        sys.exit(__doc__)
    db_path, db = database(db_path)
    data = load_export(export)
    plan = db.get("plan", {})
    order, models = [], set()
    for row in db["rows"]:
        if row["model"] not in models:
            models.add(row["model"])
            order.append(row["model"])
    totals = {model: {name: blank() for name in BUCKETS} for model in order}
    for event in data["events"]:
        kind = KINDS.get(data["kinds"][event[3]])
        model = resolve(data["models"][event[2]], models)
        if kind is None or model is None:
            continue
        tokens = sum(event[4:8])
        dollars = event[8] / 1000
        for name in (kind, "pooled"):
            bucket = totals[model][name]
            bucket["events"] += 1
            bucket["dollars"] += dollars
            bucket["tokens"] += tokens
    print(f"Database: {db_path}, version {db.get('version')}, rated {db.get('rated')}")
    print(f"Export: {export}")
    exempt = ", ".join(plan.get("exempt", [])) or "none"
    print(f"Plan addend: ${plan.get('tokenRatePerMillion', 0):.2f} per million tokens; exempt: {exempt}")
    print()
    head = ["Model", "Plan addend"]
    for label in ("Included-in-plan", "On-demand", "Pooled"):
        head += [f"{label} events", f"{label} dollars", f"{label} $/M"]
    print("| " + " | ".join(head) + " |")
    print("| " + " | ".join("---" for _ in head) + " |")
    for model in order:
        cells = [model, f"{money(addend(model, plan))}/M"]
        for name in BUCKETS:
            bucket = totals[model][name]
            cells += [str(bucket["events"]), money(bucket["dollars"]), rate(bucket["dollars"], bucket["tokens"])]
        print("| " + " | ".join(cells) + " |")
    for row in db["rows"]:
        if row.get("tokensPerTask") is not None:
            continue
        key = (row["model"], row["effort"])
        if key not in guesses:
            sys.exit(f"no token count for {row['model']} {row['effort']}; pass --guess {row['model']}@{row['effort']}=COUNT")
        count = guesses[key]
        fee = addend(row["model"], plan) * count / 1e6
        print(f"\nNote: {row['model']} {row['effort']} has no Artificial Analysis token count. "
              f"Using {count:.0f} tokens per task, a guess. "
              f"Plan addend {money(addend(row['model'], plan))} per million produces a fee of {money(fee)} per task.")


if __name__ == "__main__":
    main(sys.argv[1:])
