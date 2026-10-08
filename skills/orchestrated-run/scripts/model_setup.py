#!/usr/bin/env python3
"""Rate the model database against its frontier and choose models for personas.

model_setup.py [--db PATH] [--choices PATH] [--ratings]
               [--client NAME... | --available MODEL=EFFORT[,EFFORT]...]
               [--multi MODEL]... [--weight PERSONA=N]... [--top N]
               [--write target] [--pin PERSONA=MODEL@EFFORT]... [--unpin PERSONA]...

Scores every database row per work type as a percentage of the database's
frontier, prices it under the database's cost plan, then finds the best setup:
each model at one effort, or at any set of efforts for a model named with
--multi. Each persona takes the cheapest offered row whose score for its work
type reaches its complexity's target, or the highest-scoring row when none
does, as under Choosing a model in PERSONAS.md. A row within two points below
the target counts as meeting it when it costs at most two-thirds of the
cheapest row that does; it is marked near target. Setups rank by total
shortfall below target, then by mean cost per task, weighted by --weight,
default 1.

--client takes the client's model names as it lists them, such as
claude-haiku-5-5-thinking-high or grok-4.7-high, and skips fast variants;
--available gives models and efforts directly. Either adds the assignment the
client's models give now, using each persona's pin when the client offers it,
and the swaps that would reach the best setup.

The machine model choices file, ~/.agent-runs/model-choices.md unless
--choices is given, holds pins the user chose and a target, the best setup.
--write target saves the best setup as the target, keeping pins. --pin and
--unpin change one persona's pin. --ratings prints every row's scores. The
database defaults to ~/.agent-runs/models.json, or the skill's
templates/models.json when that is missing.
"""
import datetime, itertools, json, math, re, sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
AGENT_RUNS = Path.home() / ".agent-runs"
# Evaluation key: tasks per run, from the Artificial Analysis methodology page.
TASKS = {"terminalBench40": 66, "scicode": 288, "lcr": 100, "hle": 2158, "critpt": 70,
         "omniscienceAccuracy": 6000, "gdpvalNormalized": 220, "mmmuPro": 1730}
# Human-preference Elo boards: a result is its expected win rate against the
# board's median model, so a score is that win rate over the top model's.
ARENA = {"webdevFrontend"}
SUPPORT = {"tauBanking": 97, "terminalBench21": 89, "ifbench": 294, "tau2": 114}
WORK = {
    "coding": ["terminalBench40", "scicode"],
    "research": ["lcr", "omniscienceAccuracy", "hle"],
    "tooling": ["terminalBench40", "gdpvalNormalized"],
    "review": ["hle", "critpt", "omniscienceAccuracy"],
    "visual": ["webdevFrontend"],
}
SUPPORTS = {"coding": ["terminalBench21"], "tooling": ["tauBanking", "tau2", "ifbench", "terminalBench21"],
            "visual": ["mmmuPro"]}
# MMMU-Pro is near saturation for frontier models, so it never rates visual work alone.
SUPPORT_ONLY = {"coding", "tooling"}
# Persona complexity: the lowest score, as a share of the frontier, that meets it.
TARGETS = {"lowest": 0.0, "low": 0.50, "medium": 0.65, "high": 0.80, "highest": 0.90}
EFFORTS = ["non-reasoning", "low", "medium", "high", "xhigh", "max"]
Z90 = 1.645
MARGIN = 0.03
# A row this far below target ranks as meeting it at this multiple of its cost.
NEAR, NEAR_PRICE = 0.02, 1.5


def win(elo, median):
    return 1 / (1 + 10 ** ((median - elo) / 400))


def elo_for(share, board):
    p = min(share * win(board["top"], board["median"]), 0.999)
    return board["median"] - 400 * math.log10(1 / p - 1)


def part(results, key, frontier):
    if key in ARENA:
        board = frontier["arena"][key]
        p, top = win(results[key], board["median"]), win(board["top"], board["median"])
        return p / top, p * (1 - p) * math.log(10) / 400 * results[key + "Se"] / top
    best = frontier["best"]
    p = min(max(results[key], 0.0), 1.0)
    return results[key] / best[key], math.sqrt(p * (1 - p) / {**TASKS, **SUPPORT}[key]) / best[key]


def combine(parts):
    s = sum(p for p, _ in parts) / len(parts)
    return s, math.sqrt(sum(e * e for _, e in parts)) / len(parts)


def score_work(results, frontier):
    out = {}
    for work, keys in WORK.items():
        core = [part(results, k, frontier) for k in keys if results.get(k) is not None]
        extra = [k for k in SUPPORTS.get(work, []) if results.get(k) is not None and k in frontier["best"]]
        parts = core or ([part(results, k, frontier) for k in extra] if work in SUPPORT_ONLY else [])
        if not parts:
            out[work] = None
            continue
        s, se = combine(parts)
        s, se = s / frontier["work"][work], se / frontier["work"][work]
        out[work] = dict(score=s, ci=Z90 * se, partial=bool(core) and len(core) < len(keys), supporting=not core,
                         scaled=any(k in ARENA for k in keys) and bool(results.get("scaled")),
                         support={k: part(results, k, frontier)[0] for k in extra} if core else {})
    return out


def plan_cost(row, plan):
    usd, notes = row.get("listCostPerTask"), []
    if usd is None:
        return None, ["no cost"]
    if row.get("costEstimated"):
        notes.append("cost estimated from prices")
    rate = plan.get("tokenRatePerMillion", 0)
    if rate and not any(row["model"].startswith(p) for p in plan.get("exempt", [])):
        if row.get("tokensPerTask") is None:
            notes.append("token rate not applied: no token count")
        else:
            usd += rate * row["tokensPerTask"] / 1e6
    for prefix, fraction in plan.get("discounts", {}).items():
        if row["model"].startswith(prefix):
            usd *= 1 - fraction
            notes.append(f"{fraction:.0%} discount")
    return usd, notes


def load(path):
    db = json.loads(path.read_text())
    frontier, plan = db["frontier"], db.get("plan", {})
    excluded = {(x["model"], x["effort"]) for x in db.get("excluded", [])}
    rows = []
    for raw in db["rows"]:
        if (raw["model"], raw["effort"]) in excluded or (raw["model"], "*") in excluded:
            continue
        work = score_work(raw["results"], frontier)
        usd, notes = plan_cost(raw, plan)
        if raw.get("arena"):
            a = raw["arena"]
            source = f"WebDev Arena as {a['name']}, {a['votes']} votes"
            notes = [source + (f", scaled to this effort by coding score" if a.get("scaled") else "")] + notes
        rows.append(dict(model=raw["model"], effort=raw["effort"], provider=raw["provider"], basis=raw["basis"],
                         work=work, usd=usd, notes=notes,
                         score={w: v["score"] if v else None for w, v in work.items()}))
    return db, rows


def table(path, *columns):
    head, out = None, []
    for line in path.read_text().splitlines() + [""]:
        if not line.startswith("|"):
            if head and all(c in head for c in columns):
                return out
            head, out = None, []
            continue
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if head is None:
            head = cells
        elif not set(line) <= set("|-: "):
            out.append(dict(zip(head, cells)))
    sys.exit(f"{path}: no table with {', '.join(columns)}")


def personas():
    found = table(SKILL / "PERSONAS.md", "Persona", "Work", "Complexity")
    return [dict(name=p["Persona"], work=p["Work"], level=p["Complexity"], target=TARGETS[p["Complexity"]])
            for p in found]


def client_names(names, rows):
    models = sorted({r["model"] for r in rows}, key=len, reverse=True)
    available, skipped = {}, []
    for name in names:
        if name.endswith("-fast"):
            skipped.append(f"{name}: fast variant")
            continue
        base, eff = name, None
        for e in EFFORTS:
            if name.endswith("-" + e):
                base, eff = name[: -len(e) - 1], e
                break
        base = re.sub(r"-thinking$", "", base)
        model = next((m for m in models if base == m), None)
        if model is None or eff is None:
            skipped.append(f"{name}: not rated" + ("" if eff else ", no effort in its name"))
            continue
        available.setdefault(model, []).append(eff)
    return available, skipped


def read_choices(path):
    if not path.exists():
        return {}
    text = path.read_text()
    if "## Pins" not in text:
        return {}
    pins = {}
    section = text.split("## Pins", 1)[1].split("\n## ", 1)[0]
    for line in section.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.startswith("|") and len(cells) >= 3 and cells[0] not in ("Persona",) and not set(line) <= set("|-: "):
            pins[cells[0]] = dict(model=cells[1], effort=cells[2], reason=cells[3] if len(cells) > 3 else "")
    return pins


def write_choices(path, pins, target, db_path, db):
    stamp = datetime.datetime.now().astimezone().isoformat(timespec="minutes")
    old = path.read_text() if path.exists() else ""
    kept = old.split("## Target", 1)[1] if "## Target" in old and target is None else None
    lines = ["# Model choices", "", f"Written: {stamp} by scripts/model_setup.py", "",
             "## Pins", "",
             "Models the user chose for a persona. A run uses a pin when the client offers it,",
             "and otherwise chooses that persona from the model database.", "",
             "| Persona | Model | Effort | Reason |", "| --- | --- | --- | --- |"]
    lines += [f"| {k} | {v['model']} | {v['effort']} | {v['reason']} |" for k, v in pins.items()]
    lines += ["", "## Target"]
    if target is not None:
        rule, offer, people, weights = target
        lines += ["", "The best setup if the client's efforts could be changed. Runs do not choose",
                  "from it; the models question names swaps toward it.", "",
                  f"Database: {db_path}, version {db.get('version')}, rated {db.get('rated')}",
                  f"Rule: {rule}", f"Setup: {summary(offer, people, weights)}", "",
                  "| Persona | Work | Target | Model | Effort | Score | Cost per task |",
                  "| --- | --- | --- | --- | --- | --- | --- |"]
        lines += [f"| {p['name']} | {p['work']} | {p['level']} {p['target']:.0%} | {pick['model']} | {pick['effort']} | "
                  f"{pick['score'][p['work']]:.0%} | ${pick['usd']:.2f} |"
                  for p, pick, _ in assign(offer, people) if pick]
        text = "\n".join(lines) + "\n"
    else:
        text = "\n".join(lines) + (kept if kept is not None else "\n\nNone written yet.\n")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    print(f"\nWrote {path}")


def label(row):
    return f"{row['model']} {row['effort']}"


def key(row, person):
    s = row["score"][person["work"]]
    if s is None or not row["usd"]:
        return math.inf, math.inf
    short = max(0.0, person["target"] - s)
    if 0 < short <= NEAR:
        return 0.0, row["usd"] * NEAR_PRICE
    return short, row["usd"]


def standing(score, person):
    if score is None or score >= person["target"]:
        return ""
    return " near target" if person["target"] - score <= NEAR else " below target"


def ranked(offer, person):
    return sorted((r for r in offer if key(r, person)[0] != math.inf), key=lambda r: key(r, person))


def assign(offer, people, pins=None):
    out = []
    for p in people:
        found = ranked(offer, p)
        pick = found[0] if found else None
        pin = (pins or {}).get(p["name"])
        pinned = next((r for r in offer if pin and (r["model"], r["effort"]) == (pin["model"], pin["effort"])), None)
        if pinned:
            pick = dict(pinned, pinned=True)
        other = next((r for r in found if pick and r["provider"] != pick["provider"]
                      and key(r, p)[0] <= key(pick, p)[0]), None)
        out.append((p, pick, other))
    return out


def keys(offer, people):
    return [min((key(r, p) for r in offer), default=(math.inf, math.inf)) for p in people]


def score(vector, weights):
    short = sum(w * s for w, (s, _) in zip(weights, vector))
    paid = sum(w * c for w, (_, c) in zip(weights, vector))
    return short / sum(weights), paid / sum(weights)


def undominated(rows):
    def beats(b, a):
        def at(r, w):
            return -1 if r["score"][w] is None else r["score"][w]
        return b is not a and b["usd"] <= a["usd"] and all(at(b, w) >= at(a, w) for w in WORK) and (
            b["usd"] < a["usd"] or any(at(b, w) > at(a, w) for w in WORK) or rows.index(b) < rows.index(a))
    return [a for a in rows if a["usd"] and not any(beats(b, a) for b in rows if b["usd"])]


def search(rows, people, weights, multi, top):
    options = []
    for m in sorted({r["model"] for r in rows}):
        own = undominated([r for r in rows if r["model"] == m])
        if m in multi:
            options.append([list(s) for k in range(1, len(own) + 1) for s in itertools.combinations(own, k)])
        elif own:
            options.append([[r] for r in own])
    vectors = [[keys(o, people) for o in opts] for opts in options]
    none = [(math.inf, math.inf)] * len(people)
    floor = [[min(v[i] for v in vs) for i in range(len(people))] for vs in vectors] + [none]
    for k in range(len(options) - 1, -1, -1):
        floor[k] = [min(a, b) for a, b in zip(floor[k], floor[k + 1])]
    best = {}

    def cutoff():
        ranked = sorted(s for s, _ in best.values())
        return ranked[top - 1] if len(ranked) >= top else (math.inf, math.inf)

    def walk(k, chosen, vector):
        if k == len(options):
            offer = [r for o in chosen for r in o]
            used = frozenset(label(pick) for _, pick, _ in assign(offer, people) if pick)
            s = score(vector, weights)
            if used not in best or s < best[used][0]:
                best[used] = (s, offer)
            return
        bound = [min(a, b) for a, b in zip(vector, floor[k])]
        if (sum(w * s for w, (s, _) in zip(weights, bound)) / sum(weights),
                sum(w * c for w, (_, c) in zip(weights, bound)) / sum(weights)) > cutoff():
            return
        for o, v in zip(options[k], vectors[k]):
            walk(k + 1, chosen + [o], [min(a, b) for a, b in zip(vector, v)])

    walk(0, [], none)
    return sorted(best.values(), key=lambda b: b[0])[:top]


def used_rows(offer, people, pins=None):
    found = {label(pick): pick for _, pick, _ in assign(offer, people, pins) if pick}
    return [found[k] for k in sorted(found)]


def summary(offer, people, weights, pins=None):
    picks = assign(offer, people, pins)
    vector = [(key(pick, p)[0], pick["usd"]) if pick else (math.inf, math.inf) for p, pick, _ in picks]
    short, mean = score(vector, weights)
    marks = [standing(pick["score"][p["work"]], p) if pick else " below target" for p, pick, _ in picks]
    below, near = marks.count(" below target"), marks.count(" near target")
    by_model = {}
    for r in used_rows(offer, people, pins):
        by_model.setdefault(r["model"], []).append(r["effort"])
    text = ", ".join(f"{m} {' and '.join(e)}" for m, e in by_model.items())
    return (f"${mean:.2f} mean cost per task" + (f", {below} personas below target" if below else "")
            + (f", {near} near target" if near else "") + f": {text}")


def show(title, offer, people, weights, pins=None):
    print(f"\n## {title}\n\n{summary(offer, people, weights, pins)}\n")
    print("| Persona | Work | Target | Model | Effort | Score | Cost per task | Cheapest other provider |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for p, pick, other in assign(offer, people, pins):
        target = f"{p['level']} {p['target']:.0%}"
        if pick:
            s = pick["score"][p["work"]]
            mark = " (pinned)" if pick.get("pinned") else ""
            got = "-" if s is None else f"{s:.0%}" + standing(s, p)
            chosen = f"{pick['model']} | {pick['effort']}{mark} | {got} | ${pick['usd']:.2f}"
        else:
            chosen = "none | - | - | -"
        alternative = f"{label(other)} {other['score'][p['work']]:.0%} ${other['usd']:.2f}" if other else "-"
        print(f"| {p['name']} | {p['work']} | {target} | {chosen} | {alternative} |")
    shaky = [f"{label(pick)} for {p['name']} ({p['work']} {pick['score'][p['work']]:.0%}, target {p['target']:.0%})"
             for p, pick, _ in assign(offer, people, pins)
             if pick and not pick.get("pinned") and pick["score"][p["work"]] is not None
             and 0 <= pick["score"][p["work"]] - p["target"] < MARGIN]
    if shaky:
        print(f"\nWithin {MARGIN:.0%} above the persona's target: " + "; ".join(shaky))
    notes = sorted({f"{label(r)}: {', '.join(r['notes'])}" for r in used_rows(offer, people, pins) if r["notes"]
                    and any("discount" not in n for n in r["notes"])})
    if notes:
        print("\nNotes: " + "; ".join(notes))
    if pins is not None:
        offered = {(r["model"], r["effort"]) for r in offer}
        lost = [f"{k} ({v['model']} {v['effort']})" for k, v in pins.items() if (v["model"], v["effort"]) not in offered]
        if lost:
            print("\nPins the client does not offer, chosen from the database instead: " + ", ".join(lost))


def swaps(now, best, people):
    have = {}
    for r in used_rows(now, people):
        have.setdefault(r["model"], []).append(r["effort"])
    want = {}
    for r in used_rows(best, people):
        want.setdefault(r["model"], []).append(r["effort"])
    lines = []
    for m in sorted(set(have) | set(want)):
        a, b = have.get(m, []), want.get(m, [])
        if a != b:
            lines.append(f"- {m}: {' and '.join(a) or 'unused'} -> {' and '.join(b) or 'unused'}")
    return lines


def ratings(rows):
    print("\n## Ratings\n")
    print("| Model | Effort | Provider | " + " | ".join(w.title() for w in WORK) + " | Cost per task | Basis |")
    print("| --- " * (len(WORK) + 5) + "|")
    for r in rows:
        cells = []
        for w in WORK:
            v = r["work"][w]
            cells.append("-" if not v else f"{v['score']:.0%} ± {v['ci']:.0%}"
                         + (", partial" if v["partial"] else "") + (", supporting only" if v["supporting"] else "")
                         + (", scaled" if v.get("scaled") else ""))
        usd = f"${r['usd']:.2f}" if r["usd"] else "-"
        basis = "; ".join([r["basis"]] + r["notes"])
        print(f"| {r['model']} | {r['effort']} | {r['provider']} | " + " | ".join(cells) + f" | {usd} | {basis} |")


def main(args):
    db_path, show_ratings, available, client, multi, weight, top = None, False, {}, [], set(), {}, 3
    write, choices, pin, unpin = False, None, {}, []
    while args:
        flag, args = args[0], args[1:]
        if flag == "--ratings":
            show_ratings = True
            continue
        if flag == "--client":
            while args and not args[0].startswith("--"):
                client.append(args.pop(0))
            continue
        if not args:
            sys.exit(__doc__)
        value, args = args[0], args[1:]
        if flag == "--db":
            db_path = Path(value)
        elif flag == "--available":
            model, _, efforts = value.partition("=")
            available.setdefault(model, []).extend(efforts.split(","))
        elif flag == "--multi":
            multi.add(value)
        elif flag == "--weight":
            name, _, n = value.rpartition("=")
            weight[name] = float(n)
        elif flag == "--top":
            top = int(value)
        elif flag == "--write" and value == "target":
            write = True
        elif flag == "--pin":
            persona, _, spec = value.partition("=")
            model, _, eff = spec.rpartition("@")
            pin[persona] = dict(model=model, effort=eff, reason="user choice")
        elif flag == "--unpin":
            unpin.append(value)
        elif flag == "--choices":
            choices = Path(value)
        else:
            sys.exit(__doc__)
    machine = AGENT_RUNS / "models.json"
    db_path = db_path or (machine if machine.exists() else SKILL / "templates" / "models.json")
    choices = choices or AGENT_RUNS / "model-choices.md"
    db, rows = load(db_path)
    people = personas()
    names = {p["name"] for p in people}
    for persona in list(pin) + unpin:
        if persona not in names:
            sys.exit(f"unknown persona {persona}")
    pins = {k: v for k, v in {**read_choices(choices), **pin}.items() if k not in unpin}
    weights = [weight.get(p["name"], 1) for p in people]
    print(f"Database: {db_path}, version {db.get('version')}, rated {db.get('rated')}, {len(rows)} rows")
    print(f"Cost plan: {db.get('plan', {}).get('description', 'list prices')}")
    print(f"Choices: {choices}" + (f", pins for {', '.join(pins)}" if pins else ", no pins"))
    print(f"Personas: {len(people)} from PERSONAS.md" + (f", weighted {weight}" if weight else ", equally weighted"))
    if show_ratings:
        ratings(rows)

    results = search(rows, people, weights, multi, top)
    best = results[0][1]
    rule = "one effort per model" + (f", any set of efforts for {', '.join(sorted(multi))}" if multi else "")
    show(f"Best setup, {rule}", best, people, weights)
    if len(results) > 1:
        print("\nNext best:\n" + "\n".join(f"- {summary(o, people, weights)}" for _, o in results[1:]))

    if client:
        found, skipped = client_names(client, rows)
        for model, efforts in found.items():
            available.setdefault(model, []).extend(efforts)
        if skipped:
            print("\nClient models not used: " + "; ".join(skipped))
    if available:
        now = [r for r in rows if r["effort"] in available.get(r["model"], [])]
        missing = [f"{m} {e}" for m, es in available.items() for e in es
                   if not any(r["model"] == m and r["effort"] == e for r in rows)]
        show("Available now", now, people, weights, pins)
        if missing:
            print("\nNot rated, or excluded, in the database: " + ", ".join(missing))
        lines = swaps(now, best, people)
        if lines:
            print("\n## Swaps from available now to the best setup\n\n" + "\n".join(lines))

    if write or pin or unpin:
        write_choices(choices, pins, (rule, best, people, weights) if write else None, db_path, db)


if __name__ == "__main__":
    main(sys.argv[1:])
