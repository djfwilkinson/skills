#!/usr/bin/env python3
"""Update the orchestrated-run model database from Artificial Analysis.

model_stats.py find NAME
model_stats.py add MODEL EFFORT PROVIDER "SOURCE@EFFORT" [--db PATH]
model_stats.py add MODEL EFFORT PROVIDER --result KEY=VALUE... [price=IN/OUT] [--db PATH]
model_stats.py refresh [--db PATH]

find lists Artificial Analysis rows whose name contains NAME. add stores one
database row from an Artificial Analysis row, such as "Claude Sonnet 5.5@medium",
with its raw results, list cost per task, and tokens per task, replacing a row
with the same model and effort. An effort Artificial Analysis has not measured
is interpolated between the nearest measured efforts. --result stores
independent, bridged results for a model Artificial Analysis does not list.
refresh re-reads every row from its source and recomputes the frontier from all
current Artificial Analysis rows. The database defaults to the skill's
templates/models.json. Artificial Analysis data is cached once a day in
~/.agent-runs/model-stats/.
"""
import datetime, json, math, re, statistics, sys, urllib.request
from pathlib import Path

from model_setup import SKILL, AGENT_RUNS, ARENA, SUPPORT, TASKS, WORK, Z90, combine, elo_for, part, score_work, win

URL = "https://artificialanalysis.ai/leaderboards/models"
ARENA_URL = {"webdevFrontend": "https://arena.ai/leaderboard/code/webdev/frontend"}
MODEL_URL = "https://artificialanalysis.ai/models/"
CACHE = AGENT_RUNS / "model-stats"
EFFORTS = ["non-reasoning", "low", "medium", "high", "xhigh", "max"]
KEYS = list(TASKS) + list(SUPPORT)


def page(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(req, timeout=60).read().decode()
    return "".join(json.loads(f'"{m}"') for m in re.findall(r'self\.__next_f\.push\(\[1,"((?:[^"\\]|\\.)*)"\]\)', html))


def objects(text, marker, keep):
    dec = json.JSONDecoder()
    for m in re.finditer(marker, text):
        j = m.start()
        for _ in range(400):
            j = text.rfind("{", 0, j)
            try:
                obj, _ = dec.raw_decode(text, j)
            except ValueError:
                continue
            if isinstance(obj, dict) and keep(obj):
                yield obj
                break


def leaderboard():
    path = CACHE / f"aa-{datetime.date.today()}.json"
    if not path.exists():
        CACHE.mkdir(parents=True, exist_ok=True)
        found = {r["slug"] + r["name"]: r for r in objects(page(URL), '"terminalBench40"',
                                                           lambda o: "name" in o and "terminalBench40" in o)}
        path.write_text(json.dumps(list(found.values())))
    return json.loads(path.read_text())


def arena_board(key):
    path = CACHE / f"arena-{key}-{datetime.date.today()}.json"
    if not path.exists():
        CACHE.mkdir(parents=True, exist_ok=True)
        found = {o["modelDisplayName"]: o for o in objects(page(ARENA_URL[key]), '"ratingUpper"',
                                                            lambda o: {"modelDisplayName", "rating", "ratingUpper", "ratingLower", "votes"} <= set(o))}
        path.write_text(json.dumps(list(found.values())))
    return json.loads(path.read_text())


def arena_entry(board, model, eff):
    want = f"{model}-{eff}".replace(".", "-")
    return next((o for o in board if re.sub(r" \(.*\)$", "", o["modelDisplayName"]).replace(".", "-") == want), None)


def tokens_per_task(row):
    path = CACHE / f"tokens-{datetime.date.today()}.json"
    cache = json.loads(path.read_text()) if path.exists() else {}
    if row["slug"] not in cache:
        cache[row["slug"]] = None
        for obj in objects(page(MODEL_URL + row["slug"]), '"canonicalIntelligenceIndexTokenCount"',
                           lambda o: o.get("slug") == row["slug"] and "intelligenceIndexCost" in o):
            used = obj["canonicalIntelligenceIndexTokenCount"]
            tasks = obj["intelligenceIndexCost"]["total"] / obj["intelligenceIndexCostPerTask"]["cost"]["total"]
            cache[row["slug"]] = (used["input"] + used["output"]) / tasks
            break
        CACHE.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(cache))
    return cache[row["slug"]]


def family(row):
    return row["name"].split(" (")[0]


def effort(row):
    inner = row["name"].partition(" (")[2].split(",")[0].rstrip(")").lower()
    return inner if inner in EFFORTS else None


def current(data):
    return [x for x in data if not x.get("deprecated") and x.get("intelligenceIndex") is not None]


def frontier(data):
    pop = current(data)
    best = {key: max(x[key] for x in pop if x.get(key) is not None) for key in KEYS}
    arena = {}
    for key in ARENA:
        ratings = sorted(o["rating"] for o in arena_board(key))
        arena[key] = dict(url=ARENA_URL[key], snapshot=str(datetime.date.today()), models=len(ratings),
                          median=statistics.median(ratings), top=ratings[-1])
    ref = dict(best=best, arena=arena)
    # No one source measures every visual evaluation, so its frontier is each evaluation's own best.
    work = {w: 1.0 if any(k in ARENA for k in keys) else
            max(combine([part(x, k, ref) for k in keys])[0] for x in pop if all(x.get(k) is not None for k in keys))
            for w, keys in WORK.items()}
    ratio = statistics.median(
        x["intelligenceIndexCostPerTask"] / ((3 * x["price1mInputTokens"] + x["price1mOutputTokens"]) / 4)
        for x in pop if x.get("intelligenceIndexCostPerTask") and x.get("price1mInputTokens"))
    return dict(snapshot=str(datetime.date.today()), rows=len(pop), best=best, arena=arena, work=work,
                costRatio=ratio)


def measured(row, ratio):
    cost = row.get("intelligenceIndexCostPerTask")
    estimated = cost is None and row.get("price1mInputTokens") is not None
    if estimated:
        cost = ratio * (3 * row["price1mInputTokens"] + row["price1mOutputTokens"]) / 4
    return dict(results={k: row[k] for k in KEYS if row.get(k) is not None}, listCostPerTask=cost,
                costEstimated=estimated, tokensPerTask=None if estimated else tokens_per_task(row),
                prices=[row.get("price1mInputTokens"), row.get("price1mOutputTokens")])


def from_source(data, source, ratio):
    name, _, want = source.rpartition("@")
    rows = [r for r in data if family(r).lower() == name.lower()]
    exact = [r for r in rows if effort(r) == want.lower()]
    if exact:
        return dict(basis="measured", **measured(exact[0], ratio))
    ranked = sorted((EFFORTS.index(effort(r)), r) for r in rows if effort(r) not in (None, "non-reasoning"))
    w = EFFORTS.index(want.lower())
    below, above = [x for x in ranked if x[0] < w], [x for x in ranked if x[0] > w]
    if not below or not above:
        sys.exit(f"{source}: not measured and cannot be interpolated")
    (i0, a), (i1, b) = below[-1], above[0]
    t = (w - i0) / (i1 - i0)
    ma, mb = measured(a, ratio), measured(b, ratio)

    def mix(x, y):
        return None if x is None or y is None else x + t * (y - x)

    return dict(basis=f"interpolated from {effort(a)} and {effort(b)}",
                results={k: mix(ma["results"].get(k), mb["results"].get(k)) for k in KEYS
                         if mix(ma["results"].get(k), mb["results"].get(k)) is not None},
                listCostPerTask=mix(ma["listCostPerTask"], mb["listCostPerTask"]),
                costEstimated=ma["costEstimated"] or mb["costEstimated"],
                tokensPerTask=mix(ma["tokensPerTask"], mb["tokensPerTask"]),
                prices=[mix(x, y) for x, y in zip(ma["prices"], mb["prices"])])


def independent(items, ratio):
    results, prices = {}, [None, None]
    for item in items:
        key, _, val = item.partition("=")
        if key == "price":
            prices = [float(v) for v in val.split("/")]
        elif key in KEYS:
            results[key] = float(val)
        else:
            sys.exit(f"unknown result key {key}; use one of {', '.join(KEYS)}")
    cost = ratio * (3 * prices[0] + prices[1]) / 4 if prices[0] is not None else None
    return dict(basis="independent results", results=results, listCostPerTask=cost, costEstimated=True,
                tokensPerTask=None, prices=prices)


def with_arena(rows, frontier):
    for row in rows:
        row.pop("arena", None)
        row["results"].pop("scaled", None)
        for key in ARENA:
            row["results"].pop(key, None)
            row["results"].pop(key + "Se", None)
            found = arena_entry(arena_board(key), row["model"], row["effort"])
            if found:
                row["results"][key] = found["rating"]
                row["results"][key + "Se"] = (found["ratingUpper"] - found["ratingLower"]) / (2 * 1.96)
                row["arena"] = dict(name=found["modelDisplayName"], votes=found["votes"])
    for row in rows:
        for key in ARENA:
            if key in row["results"]:
                continue
            rank = EFFORTS.index(row["effort"]) if row["effort"] in EFFORTS else None
            mine = score_work(row["results"], frontier)["coding"]
            sources = [r for r in rows if r["model"] == row["model"] and r.get("arena") and not r["arena"].get("scaled")
                       and r["effort"] in EFFORTS and rank is not None and EFFORTS.index(r["effort"]) > rank
                       and score_work(r["results"], frontier)["coding"]]
            if not mine or not sources:
                continue
            src = min(sources, key=lambda r: EFFORTS.index(r["effort"]))
            theirs = score_work(src["results"], frontier)["coding"]
            board = frontier["arena"][key]
            base, base_se = part(src["results"], key, frontier)
            share = base * mine["score"] / theirs["score"]
            rel = math.sqrt((base_se / base) ** 2 + (mine["ci"] / Z90 / mine["score"]) ** 2
                            + (theirs["ci"] / Z90 / theirs["score"]) ** 2)
            elo = elo_for(share, board)
            p = win(elo, board["median"])
            row["results"][key] = elo
            row["results"][key + "Se"] = share * rel * win(board["top"], board["median"]) / (p * (1 - p) * math.log(10) / 400)
            row["results"]["scaled"] = 1
            row["arena"] = dict(src["arena"], scaled=True)
    return rows


def save(path, db):
    db["rows"].sort(key=lambda r: (r["model"], EFFORTS.index(r["effort"]) if r["effort"] in EFFORTS else 99))
    path.write_text(json.dumps(db, indent=2) + "\n")
    print(f"Wrote {path}: {len(db['rows'])} rows, frontier from {db['frontier']['rows']} current rows")


def main(args):
    db_path = SKILL / "templates" / "models.json"
    if "--db" in args:
        i = args.index("--db")
        db_path, args = Path(args[i + 1]), args[:i] + args[i + 2:]
    if not args:
        sys.exit(__doc__)
    command, args = args[0], args[1:]
    data = leaderboard()
    if command == "find" and args:
        for r in data:
            if args[0].lower() in r["name"].lower():
                print(f"{r['name']}" + (" [not current]" if r not in current(data) else ""))
        return
    db = json.loads(db_path.read_text())
    if command == "refresh":
        db["frontier"] = frontier(data)
        for row in db["rows"]:
            if row.get("source"):
                row.update(from_source(data, row["source"], db["frontier"]["costRatio"]))
        with_arena(db["rows"], db["frontier"])
    elif command == "add" and len(args) >= 4:
        model, eff, provider, rest = args[0], args[1], args[2], args[3:]
        db.setdefault("frontier", frontier(data))
        ratio = db["frontier"]["costRatio"]
        if rest[0] == "--result":
            row = dict(model=model, effort=eff, provider=provider, source=None, **independent(rest[1:], ratio))
        else:
            row = dict(model=model, effort=eff, provider=provider, source=rest[0], **from_source(data, rest[0], ratio))
        db["rows"] = [r for r in db["rows"] if (r["model"], r["effort"]) != (model, eff)] + [row]
        with_arena(db["rows"], db["frontier"])
    else:
        sys.exit(__doc__)
    db["rated"] = str(datetime.date.today())
    save(db_path, db)


if __name__ == "__main__":
    main(sys.argv[1:])
