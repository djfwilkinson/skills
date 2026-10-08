#!/usr/bin/env python3
"""Report which personas and models orchestrated runs used, and their cost share.

run_usage.py [--db PATH] [--choices PATH]
             [--client NAME... | --available MODEL=EFFORT[,EFFORT]...] [PATH...]

Each PATH is a run directory, an orchestrated-run directory holding runs, or a
project holding .agent-runs/orchestrated-run. Without paths, it reads every run
registered in the device action ledger, ~/.agent-runs/action-ledger/runs.

It counts tickets per run, per persona, and per model, with work units, human
tickets, and fix tickets: those whose title cites a finding or names fixes.
Only personas recorded in ticket YAML count; tickets without one are listed
by type. Each persona's model is the one its run's ROSTER.md table gives, or,
with --client or --available, the one Choosing a model gives for the client's
models now. Cost share weights each ticket by its model's cost per task under
the model database's cost plan, so it compares models, not dollars spent.
"""
import collections, json, re, sys
from pathlib import Path

from model_setup import AGENT_RUNS, assign, client_names, load, personas, read_choices

HUMAN = {"Discuss/Gather Inputs", "Human Task", "Human and Agent Task"}
FIX = re.compile(r"\bF-?\d+\b|\bfix(es)?\b|remediation", re.I)


def run_dirs(paths):
    if not paths:
        ledger = AGENT_RUNS / "action-ledger" / "runs"
        return [Path(json.loads(f.read_text())["run"]["dir"]) for f in sorted(ledger.glob("*.json"))]
    found = []
    for p in map(Path, paths):
        p = p.expanduser()
        if (p / "tickets").is_dir():
            found.append(p)
            continue
        base = p / ".agent-runs" / "orchestrated-run" if (p / ".agent-runs").is_dir() else p
        found += sorted(d for d in base.iterdir() if (d / "tickets").is_dir())
    return found


def tickets(run):
    out = []
    for f in sorted((run / "tickets").glob("T-*.md")):
        m = re.match(r"---\n(.*?)\n---\n(.*)", f.read_text(errors="replace"), re.S)
        if not m:
            continue
        meta = dict(line.split(":", 1) for line in m.group(1).splitlines() if ":" in line and line[0] != " ")
        meta = {k.strip(): v.strip() for k, v in meta.items()}
        units = re.search(r"^## Work units\n(.*?)(?=^## |\Z)", m.group(2), re.S | re.M)
        persona = meta.get("persona", "")
        out.append(dict(type=meta.get("type", ""), title=meta.get("title", ""),
                        persona="" if persona in ("", "null", "~") else persona,
                        units=max(1, len(re.findall(r"^### ", units.group(1), re.M))) if units else 1))
    return out


def roster(run):
    path = run / "ROSTER.md"
    if not path.exists():
        return {}
    rows, head = {}, None
    for line in path.read_text().splitlines():
        if not line.startswith("|"):
            if rows:
                break
            head = None
            continue
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if head is None:
            head = cells
        elif not set(line) <= set("|-: ") and "Persona" in head and "Model" in head:
            row = dict(zip(head, cells))
            strip = lambda c: re.sub(r"\s*\(.*?\)", "", c).strip()
            rows[row["Persona"]] = (strip(row["Model"]), strip(row.get("Effort") or row.get("Preferred effort", "")))
    return rows


def main(args):
    db_path, choices, client, available, paths = None, None, [], {}, []
    while args:
        flag, args = args[0], args[1:]
        if flag == "--client":
            while args and not args[0].startswith("--"):
                client.append(args.pop(0))
        elif flag in ("--db", "--choices", "--available") and args:
            value, args = args[0], args[1:]
            if flag == "--db":
                db_path = Path(value)
            elif flag == "--choices":
                choices = Path(value)
            else:
                model, _, efforts = value.partition("=")
                available.setdefault(model, []).extend(efforts.split(","))
        elif flag.startswith("--"):
            sys.exit(__doc__)
        else:
            paths.append(flag)
    machine = AGENT_RUNS / "models.json"
    db_path = db_path or (machine if machine.exists() else Path(__file__).resolve().parent.parent / "templates" / "models.json")
    _, rows = load(db_path)
    usd = {(r["model"], r["effort"]): r["usd"] for r in rows}
    current = None
    if client or available:
        for model, efforts in client_names(client, rows)[0].items():
            available.setdefault(model, []).extend(efforts)
        offer = [r for r in rows if r["effort"] in available.get(r["model"], [])]
        pins = read_choices(choices or AGENT_RUNS / "model-choices.md")
        current = {p["name"]: (pick["model"], pick["effort"]) for p, pick, _ in assign(offer, personas(), pins) if pick}

    runs = run_dirs(paths)
    per_persona, per_model, cost_model, unrecorded = (collections.Counter() for _ in range(4))
    persona_units, persona_cost, persona_model, unpriced = collections.Counter(), collections.Counter(), {}, 0
    print(f"Database: {db_path}\nModels: {'current client assignment' if current else 'each run ROSTER.md'}\n")
    print("| Run | Tickets | Agent | Human | Fix tickets | Units per agent ticket | Persona recorded |")
    print("| --- | --- | --- | --- | --- | --- | --- |")
    for run in runs:
        ts = tickets(run)
        agent = [t for t in ts if t["type"] not in HUMAN]
        recorded = [t for t in agent if t["persona"]]
        models = current or roster(run)
        for t in agent:
            if not t["persona"]:
                unrecorded[t["type"]] += 1
                continue
            p = t["persona"]
            per_persona[p] += 1
            persona_units[p] += t["units"]
            m = models.get(p)
            cost = usd.get(m) if m else None
            name = f"{m[0]} {m[1]}" if m else "unknown"
            persona_model.setdefault(p, collections.Counter())[name] += 1
            per_model[name] += 1
            if cost:
                cost_model[name] += cost
                persona_cost[p] += cost
            else:
                unpriced += 1
        mean = sum(t["units"] for t in agent) / len(agent) if agent else 0
        print(f"| {run.name} | {len(ts)} | {len(agent)} | {len(ts) - len(agent)} | "
              f"{sum(bool(FIX.search(t['title'])) for t in agent)} | {mean:.1f} | {len(recorded)} |")

    total = sum(cost_model.values()) or 1
    n = sum(per_persona.values()) or 1
    print("\n| Persona | Tickets | Units | Model | Share | Cost share |\n| --- | --- | --- | --- | --- | --- |")
    for p, count in per_persona.most_common():
        model = ", ".join(f"{m} ({c})" if len(persona_model[p]) > 1 else m for m, c in persona_model[p].most_common())
        print(f"| {p} | {count} | {persona_units[p]} | {model} | {count / n:.0%} | {persona_cost[p] / total:.0%} |")
    print("\n| Model | Tickets | Share | Cost share |\n| --- | --- | --- | --- |")
    for m, count in per_model.most_common():
        print(f"| {m} | {count} | {count / n:.0%} | {cost_model[m] / total:.0%} |")
    if unrecorded:
        print("\nAgent tickets with no persona recorded, by type: "
              + ", ".join(f"{k} {v}" for k, v in unrecorded.most_common()))
    if unpriced:
        print(f"\n{unpriced} tickets have a model the database does not price; they count in tickets, not cost.")


if __name__ == "__main__":
    main(sys.argv[1:])
