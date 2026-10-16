#!/usr/bin/env python3
"""Rate the model database against its frontier and choose models for persona levels.

model_setup.py [--db PATH] [--choices PATH] [--ratings]
               [--client NAME... | --available MODEL=EFFORT[,EFFORT]...]
               [--multi MODEL]... [--weight SLOT=N]... [--top N]
               [--write target] [--pin SLOT=MODEL@EFFORT]... [--unpin SLOT]...
               [--personas PATH]...

Scores every database row per work type as a percentage of the database's
frontier and prices it under the database's cost plan. Models are chosen per
slot: a work type at a level, such as coding/senior, shared by every persona of
that work type that may run at that level. A persona with a Models rule gets
its own slots, named persona/level. The persona table in PERSONAS.md,
and in every --personas file, gives each persona's Work, its Levels and an
optional Models rule.

Each level has a target score and a cost ceiling per task. A slot takes the
cheapest offered row at or under its ceiling whose score for its work type
reaches the target; otherwise the highest-scoring row under the ceiling,
marked below target; otherwise, when no row is under the ceiling, the cheapest
row, marked over ceiling. A row within two points below the target counts as
meeting it when it costs at most two-thirds of the cheapest row that does; it
is marked near target.

The best setup offers each model at one effort, or at any set of efforts for a
model named with --multi, and ranks setups by total shortfall below target,
then by mean cost per task, weighted by --weight, default 1.

A Models rule is "only <model>[, <model>]", which considers just those models,
or "not <model>[, <model>]", which considers every other model; each name
matches the start of a model name. A pin overrides it.

--client takes the client's model names as it lists them, such as
claude-haiku-5-5-thinking-high or grok-4.7-high, and skips fast variants;
--available gives models and efforts directly. Either adds the assignment the
client's models give now, using each slot's pin when the client offers it,
and the swaps that would reach the best setup.

The machine model choices file, ~/.agent-runs/model-choices.md unless
--choices is given, holds pins the user chose and a target, the best setup.
--write target saves the best setup as the target, keeping pins. --pin and
--unpin change one slot's pin. --ratings prints every row's scores. The
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
# Levels: the lowest score, as a share of the frontier, that meets one, and the
# most a row may cost per task. The model database's "levels" overrides these.
LEVELS = {"junior": dict(target=0.45, ceiling=0.40), "standard": dict(target=0.60, ceiling=0.80),
          "senior": dict(target=0.75, ceiling=1.50), "principal": dict(target=0.88, ceiling=4.00)}
EFFORTS = ["non-reasoning", "low", "medium", "high", "xhigh", "max"]
Z90 = 1.645
MARGIN = 0.03
# A row this far below target ranks as meeting it at this multiple of its cost.
NEAR, NEAR_PRICE = 0.02, 1.5
# A row over the ceiling ranks after every row under it, cheapest first.
OVER = 10.0


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


def models_rule(name, text):
    text = text.strip()
    if not text or text == "-":
        return None
    mode, _, names = text.partition(" ")
    if mode not in ("only", "not") or not names.strip():
        sys.exit(f"persona {name}: Models must be blank, 'only <model>[, <model>]' or 'not <model>[, <model>]'")
    return mode, tuple(n.strip() for n in names.split(",") if n.strip())


def personas(extra=()):
    found = table(SKILL / "PERSONAS.md", "Persona", "Work", "Levels")
    for path in extra:
        found += table(Path(path), "Persona", "Work", "Levels")
    seen, unique = {}, []
    for p in found:
        levels = tuple(l.strip().strip("`") for l in p["Levels"].split(",") if l.strip())
        bad = [l for l in levels if l not in LEVELS]
        if bad or not levels:
            sys.exit(f"persona {p['Persona']}: unknown level {', '.join(bad) or '(none)'}")
        spec = dict(name=p["Persona"], work=p["Work"], levels=levels, models=models_rule(p["Persona"], p.get("Models", "")))
        if p["Persona"] in seen:
            if seen[p["Persona"]] != spec:
                sys.exit(f"persona {p['Persona']} is defined twice differently")
            continue
        seen[p["Persona"]] = spec
        unique.append(spec)
    return unique


def slots(people, levels):
    found = {}
    for p in people:
        for level in p["levels"]:
            name = f"{p['name'] if p['models'] else p['work']}/{level}"
            slot = found.setdefault(name, dict(name=name, work=p["work"], level=level, models=p["models"],
                                               target=levels[level]["target"], ceiling=levels[level]["ceiling"],
                                               personas=[]))
            slot["personas"].append(p["name"])
    order = list(levels)
    return sorted(found.values(), key=lambda s: (list(WORK).index(s["work"]), order.index(s["level"]), s["name"]))


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
        if line.startswith("|") and len(cells) >= 3 and cells[0] not in ("Slot", "Persona") and not set(line) <= set("|-: "):
            pins[cells[0]] = dict(model=cells[1], effort=cells[2], reason=cells[3] if len(cells) > 3 else "")
    return pins


def write_choices(path, pins, target, db_path, db):
    stamp = datetime.datetime.now().astimezone().isoformat(timespec="minutes")
    old = path.read_text() if path.exists() else ""
    kept = old.split("## Target", 1)[1] if "## Target" in old and target is None else None
    lines = ["# Model choices", "", f"Written: {stamp} by scripts/model_setup.py", "",
             "## Pins", "",
             "Models the user chose for a slot, a work type at a level. A run uses a pin when",
             "the client offers it, and otherwise chooses that slot from the model database.", "",
             "| Slot | Model | Effort | Reason |", "| --- | --- | --- | --- |"]
    lines += [f"| {k} | {v['model']} | {v['effort']} | {v['reason']} |" for k, v in pins.items()]
    lines += ["", "## Target"]
    if target is not None:
        rule, offer, seats, weights = target
        lines += ["", "The best setup if the client's efforts could be changed. Runs do not choose",
                  "from it; the models question names swaps toward it.", "",
                  f"Database: {db_path}, version {db.get('version')}, rated {db.get('rated')}",
                  f"Rule: {rule}", f"Setup: {summary(offer, seats, weights)}", "",
                  "| Slot | Target | Ceiling | Model | Effort | Score | Cost per task |",
                  "| --- | --- | --- | --- | --- | --- | --- |"]
        lines += [f"| {s['name']} | {s['target']:.0%} | ${s['ceiling']:.2f} | {pick['model']} | {pick['effort']} | "
                  f"{pick['score'][s['work']]:.0%} | ${pick['usd']:.2f} |"
                  for s, pick, _ in assign(offer, seats) if pick]
        text = "\n".join(lines) + "\n"
    else:
        text = "\n".join(lines) + (kept if kept is not None else "\n\nNone written yet.\n")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    print(f"\nWrote {path}")


def label(row):
    return f"{row['model']} {row['effort']}"


def allowed(row, slot):
    rule = slot.get("models")
    if not rule:
        return True
    mode, names = rule
    listed = any(row["model"].startswith(n) for n in names)
    return listed if mode == "only" else not listed


def key(row, slot):
    s = row["score"][slot["work"]]
    if s is None or not row["usd"] or not allowed(row, slot):
        return math.inf, math.inf
    if row["usd"] > slot["ceiling"] + 1e-9:
        return OVER, row["usd"]
    short = max(0.0, slot["target"] - s)
    if 0 < short <= NEAR:
        return 0.0, row["usd"] * NEAR_PRICE
    return short, row["usd"]


def standing(pick, slot):
    if pick["usd"] > slot["ceiling"] + 1e-9:
        return " over ceiling"
    score = pick["score"][slot["work"]]
    if score is None or score >= slot["target"]:
        return ""
    return " near target" if slot["target"] - score <= NEAR else " below target"


def ranked(offer, slot):
    return sorted((r for r in offer if key(r, slot)[0] != math.inf), key=lambda r: key(r, slot))


def assign(offer, seats, pins=None):
    out = []
    for s in seats:
        found = ranked(offer, s)
        pick = found[0] if found else None
        pin = (pins or {}).get(s["name"])
        pinned = next((r for r in offer if pin and (r["model"], r["effort"]) == (pin["model"], pin["effort"])), None)
        if pinned:
            pick = dict(pinned, pinned=True)
        other = next((r for r in found if pick and r["provider"] != pick["provider"]
                      and key(r, s)[0] <= key(pick, s)[0]), None)
        out.append((s, pick, other))
    return out


def keys(offer, seats):
    return [min((key(r, s) for r in offer), default=(math.inf, math.inf)) for s in seats]


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


def search(rows, seats, weights, multi, top):
    options = []
    for m in sorted({r["model"] for r in rows}):
        own = undominated([r for r in rows if r["model"] == m])
        if m in multi:
            options.append([list(s) for k in range(1, len(own) + 1) for s in itertools.combinations(own, k)])
        elif own:
            options.append([[r] for r in own])
    vectors = [[keys(o, seats) for o in opts] for opts in options]
    none = [(math.inf, math.inf)] * len(seats)
    floor = [[min(v[i] for v in vs) for i in range(len(seats))] for vs in vectors] + [none]
    for k in range(len(options) - 1, -1, -1):
        floor[k] = [min(a, b) for a, b in zip(floor[k], floor[k + 1])]
    best = {}

    def cutoff():
        ranked = sorted(s for s, _ in best.values())
        return ranked[top - 1] if len(ranked) >= top else (math.inf, math.inf)

    def walk(k, chosen, vector):
        if k == len(options):
            offer = [r for o in chosen for r in o]
            used = frozenset(label(pick) for _, pick, _ in assign(offer, seats) if pick)
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


def used_rows(offer, seats, pins=None):
    found = {label(pick): pick for _, pick, _ in assign(offer, seats, pins) if pick}
    return [found[k] for k in sorted(found)]


def summary(offer, seats, weights, pins=None):
    picks = assign(offer, seats, pins)
    vector = [(key(pick, s)[0], pick["usd"]) if pick else (math.inf, math.inf) for s, pick, _ in picks]
    _, mean = score(vector, weights)
    marks = [standing(pick, s) if pick else " below target" for s, pick, _ in picks]
    counts = [f"{marks.count(' ' + m)} {m}" for m in ("below target", "near target", "over ceiling") if marks.count(" " + m)]
    by_model = {}
    for r in used_rows(offer, seats, pins):
        by_model.setdefault(r["model"], []).append(r["effort"])
    text = ", ".join(f"{m} {' and '.join(e)}" for m, e in by_model.items())
    return f"${mean:.2f} mean cost per task" + "".join(f", {c}" for c in counts) + f": {text}"


def show(title, offer, seats, weights, pins=None):
    print(f"\n## {title}\n\n{summary(offer, seats, weights, pins)}\n")
    print("| Slot | Personas | Target | Ceiling | Model | Effort | Score | Cost per task | Cheapest other provider |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for s, pick, other in assign(offer, seats, pins):
        head = f"| {s['name']} | {', '.join(s['personas'])} | {s['target']:.0%} | ${s['ceiling']:.2f}"
        if pick:
            v = pick["score"][s["work"]]
            mark = " (pinned)" if pick.get("pinned") else ""
            got = ("-" if v is None else f"{v:.0%}") + standing(pick, s)
            chosen = f"{pick['model']} | {pick['effort']}{mark} | {got} | ${pick['usd']:.2f}"
        else:
            chosen = "none | - | - | -"
        alternative = f"{label(other)} {other['score'][s['work']]:.0%} ${other['usd']:.2f}" if other else "-"
        print(f"{head} | {chosen} | {alternative} |")
    shaky = [f"{label(pick)} for {s['name']} ({s['work']} {pick['score'][s['work']]:.0%}, target {s['target']:.0%})"
             for s, pick, _ in assign(offer, seats, pins)
             if pick and not pick.get("pinned") and pick["score"][s["work"]] is not None
             and 0 <= pick["score"][s["work"]] - s["target"] < MARGIN]
    if shaky:
        print(f"\nWithin {MARGIN:.0%} above the slot's target: " + "; ".join(shaky))
    notes = sorted({f"{label(r)}: {', '.join(r['notes'])}" for r in used_rows(offer, seats, pins) if r["notes"]
                    and any("discount" not in n for n in r["notes"])})
    if notes:
        print("\nNotes: " + "; ".join(notes))
    if pins is not None:
        offered = {(r["model"], r["effort"]) for r in offer}
        lost = [f"{k} ({v['model']} {v['effort']})" for k, v in pins.items() if (v["model"], v["effort"]) not in offered]
        if lost:
            print("\nPins the client does not offer, chosen from the database instead: " + ", ".join(lost))


def swaps(now, best, seats):
    have = {}
    for r in used_rows(now, seats):
        have.setdefault(r["model"], []).append(r["effort"])
    want = {}
    for r in used_rows(best, seats):
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


def levels_of(db):
    out = {k: dict(v) for k, v in LEVELS.items()}
    for k, v in db.get("levels", {}).items():
        if k not in out:
            sys.exit(f"model database: unknown level {k}")
        out[k].update(v)
    return out


def setup(db_path=None, extra=()):
    machine = AGENT_RUNS / "models.json"
    db_path = db_path or (machine if machine.exists() else SKILL / "templates" / "models.json")
    db, rows = load(db_path)
    levels = levels_of(db)
    return db_path, db, rows, levels, slots(personas(extra), levels)


def main(args):
    db_path, show_ratings, available, client, multi, weight, top = None, False, {}, [], set(), {}, 3
    write, choices, pin, unpin, extra = False, None, {}, [], []
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
            name, _, spec = value.partition("=")
            model, _, eff = spec.rpartition("@")
            pin[name] = dict(model=model, effort=eff, reason="user choice")
        elif flag == "--unpin":
            unpin.append(value)
        elif flag == "--choices":
            choices = Path(value)
        elif flag == "--personas":
            extra.append(value)
        else:
            sys.exit(__doc__)
    db_path, db, rows, levels, seats = setup(db_path, extra)
    choices = choices or AGENT_RUNS / "model-choices.md"
    names = {s["name"] for s in seats}
    for name in list(pin) + unpin + list(weight):
        if name not in names:
            sys.exit(f"unknown slot {name}; slots are {', '.join(sorted(names))}")
    pins = {k: v for k, v in {**read_choices(choices), **pin}.items() if k not in unpin}
    weights = [weight.get(s["name"], 1) for s in seats]
    print(f"Database: {db_path}, version {db.get('version')}, rated {db.get('rated')}, {len(rows)} rows")
    print(f"Cost plan: {db.get('plan', {}).get('description', 'list prices')}")
    print("Levels: " + ", ".join(f"{k} {v['target']:.0%} up to ${v['ceiling']:.2f}" for k, v in levels.items())
          + (" (from the database)" if db.get("levels") else ""))
    print(f"Choices: {choices}" + (f", pins for {', '.join(pins)}" if pins else ", no pins"))
    print(f"Slots: {len(seats)} from PERSONAS.md" + (f" and {', '.join(extra)}" if extra else "")
          + (f", weighted {weight}" if weight else ", equally weighted"))
    if show_ratings:
        ratings(rows)

    results = search(rows, seats, weights, multi, top)
    best = results[0][1]
    rule = "one effort per model" + (f", any set of efforts for {', '.join(sorted(multi))}" if multi else "")
    show(f"Best setup, {rule}", best, seats, weights)
    if len(results) > 1:
        print("\nNext best:\n" + "\n".join(f"- {summary(o, seats, weights)}" for _, o in results[1:]))

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
        show("Available now", now, seats, weights, pins)
        if missing:
            print("\nNot rated, or excluded, in the database: " + ", ".join(missing))
        lines = swaps(now, best, seats)
        if lines:
            print("\n## Swaps from available now to the best setup\n\n" + "\n".join(lines))

    if write or pin or unpin:
        write_choices(choices, pins, (rule, best, seats, weights) if write else None, db_path, db)


if __name__ == "__main__":
    main(sys.argv[1:])
