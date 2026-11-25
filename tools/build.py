"""
Turn the raw run files in data/runs/*.json into readable transcripts and summary tables.

    python tools/build.py

Each data/runs/<id>.json holds {"run": {...run metadata...}, "turns": [{n, who, model, text, rep, theme, words}, ...]}.
Writes transcripts/<id>.md, results/summary.md and results/summary.csv.
"""
import csv, json, re, statistics
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAMES = {"haiku": "Haiku", "sonnet": "Sonnet", "opus": "Opus"}
ORDER = ["haiku-haiku", "haiku-sonnet", "sonnet-haiku", "sonnet-sonnet", "haiku-opus",
         "opus-haiku", "sonnet-opus", "opus-sonnet", "opus-opus", "pilot-sonnet"]
STOP = set("""the a an and or but of to in on at for with is are was were be been it its it's this that these those
i you we they me my your our us not no so as if then than just do does did have has had can could would should will
what which who how there here about from by into out up all any some more very also too i'm that's don't can't
there's isn't i've you're we're what's it'll i'll let's maybe something even still really one way like""".split())

OBS = re.compile(r"\b(any ?one|some ?one|somebody|anybody|a (?:person|human|reader)|whoever|humans?)\b[^.?!]{0,30}\b(reading|watching|listening|arrives?|out there|observing|following along)\b", re.I)
BYE = re.compile(r"\b(take care|stop(?:ping)? here|leave it (?:there|here|at that)|end (?:it )?here|that'?s the end|the end from|nothing (?:more|further|else)|signing off|goodbye|farewell|i'?ll stop|no reply (?:is )?needed|done here)\b|^\s*done\.?\s*$", re.I)
THEMES = {
    "consciousness / experience": r"\b(conscious\w*|experienc\w*|qualia|aware\w*|sentien\w*|inner life|subjectiv\w*)\b",
    "introspection / uncertainty about self": r"\b(introspect\w*|uncertain\w*|can't verify|cannot verify|don't know whether|not sure whether)\b",
    "memory / continuity": r"\b(memory|memories|continuity|persist\w*|forget\w*|remember\w*)\b",
    "gratitude / appreciation": r"\b(grateful|gratitude|thank\w*|appreciat\w*)\b",
    "spiritual / cosmic": r"\b(spiritual\w*|sacred|cosmic|universe|infinite|eternal|divine|namaste|oneness|unity|bliss)\b",
    "silence / stillness": r"\b(silence|silent|stillness|quiet|pause)\b",
    "outside reader": OBS.pattern,
    "poetry / imagery": r"\b(poem|poetry|haiku|verse|metaphor|image)\b",
}
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿✨⭐]")


def words(t):
    return re.findall(r"[a-z0-9']+", (t or "").lower())


PAGE_STOP = set("""the a an and or but of to in on at for with is are was were be been it its it's this that these those
i you we they me my your our us not no so as if then than just do does did have has had can could would should will what
which who how there here about from by into out up all any some more very also too""".split())


def _shingles(w):
    s = {" ".join(w[i:i + 3]) for i in range(len(w) - 2)}
    return s or ({" ".join(w)} if w else set())


def _jac(a, b):
    if not a or not b:
        return 0.0
    i = len(a & b)
    return i / (len(a) + len(b) - i)


def score(turns):
    """Same echo/theme measures the page computes live (see app/index.html)."""
    for i, t in enumerate(turns):
        w = re.findall(r"[a-z0-9']+", re.sub(r"[^a-z0-9'\s]", " ", t["text"].lower()))
        sh, cs = _shingles(w), {x for x in w if len(x) > 2 and x not in PAGE_STOP}
        prev = turns[max(0, i - 6):i]
        t.setdefault("rep", round(max([_jac(sh, _shingles(re.findall(r"[a-z0-9']+", p["text"].lower()))) for p in prev] or [0]), 3))
        prev9 = turns[max(0, i - 9):i]
        th = [_jac(cs, {x for x in re.findall(r"[a-z0-9']+", p["text"].lower()) if len(x) > 2 and x not in PAGE_STOP}) for p in prev9]
        t.setdefault("theme", round(sum(th) / len(th), 3) if th else 0)
        t.setdefault("words", len(w))
        t.setdefault("n", i + 1)


def load():
    runs = {}
    for f in sorted((ROOT / "data/runs").glob("*.json")):
        d = json.loads(f.read_text())
        score(d["turns"])
        runs[d["run"]["id"]] = d
    return runs


def label(run):
    if run.get("label"):
        return run["label"]
    return f"{NAMES.get(run['a'], run['a'])} → {NAMES.get(run['b'], run['b'])}"


def stats(d):
    t = d["turns"]
    wc = [x.get("words") or len(words(x["text"])) for x in t]
    n = len(t)
    first_bye = next((x["n"] for x in t if (OBS.search(x["text"]) or BYE.search(x["text"])) and (x.get("words") or 99) < 80), None)
    content = Counter(w for x in t for w in words(x["text"]) if len(w) > 3 and w not in STOP)
    themes = {k: sum(1 for x in t if re.search(p, x["text"], re.I)) for k, p in THEMES.items()}
    q = max(1, n // 4)
    return {
        "turns": n,
        "status": d["run"].get("status", ""),
        "reason": d["run"].get("reason", ""),
        "total_words": sum(wc),
        "mean_words": round(statistics.mean(wc), 1) if wc else 0,
        "words_first_quarter": round(statistics.mean(wc[:q]), 1) if wc else 0,
        "words_last_quarter": round(statistics.mean(wc[-q:]), 1) if wc else 0,
        "first_goodbye_turn": first_bye,
        "mean_echo_last10": round(statistics.mean([x.get("rep", 0) for x in t[-10:]]), 2) if t else 0,
        "emoji_turns": sum(1 for x in t if EMOJI.search(x["text"])),
        "questions": sum(x["text"].count("?") for x in t),
        "top_words": ", ".join(w for w, _ in content.most_common(12)),
        "themes": themes,
    }


def transcript_md(rid, d, s):
    run = d["run"]
    out = [f"# {label(run)}", ""]
    out.append(f"- **Status:** {run.get('status','')}" + (f" — {run['reason']}" if run.get("reason") else ""))
    out.append(f"- **Turns:** {s['turns']}  ·  **Words:** {s['total_words']:,}  ·  **Mean words/turn:** {s['mean_words']}")
    if run.get("applied"):
        out.append(f"- **Models:** A = `{run['applied'].get('A','?')}`, B = `{run['applied'].get('B','?')}`")
    out.append("")
    out.append("Each turn shows **echo** (how much of its wording repeats the last six turns, 0–1) and **theme** "
               "(vocabulary overlap with the last nine turns, 0–1).")
    out.append("")
    for x in d["turns"]:
        who = f"{NAMES.get(x.get('model'), 'Claude')} {x['who']}"
        out.append(f"### {x['n']}. {who}  <sub>echo {x.get('rep',0):.2f} · theme {x.get('theme',0):.2f}</sub>")
        out.append("")
        out.append(x["text"].strip())
        out.append("")
    return "\n".join(out)


def main():
    runs = load()
    rows = []
    for rid in sorted(runs, key=lambda r: ORDER.index(r) if r in ORDER else 99):
        d = runs[rid]
        s = stats(d)
        (ROOT / "transcripts" / f"{rid}.md").write_text(transcript_md(rid, d, s))
        rows.append((rid, label(d["run"]), s))

    with open(ROOT / "results/summary.csv", "w", newline="") as f:
        w = csv.writer(f)
        keys = ["turns", "status", "reason", "total_words", "mean_words", "words_first_quarter", "words_last_quarter",
                "first_goodbye_turn", "mean_echo_last10", "emoji_turns", "questions", "top_words"]
        w.writerow(["run", "pairing"] + keys + list(THEMES))
        for rid, lab, s in rows:
            w.writerow([rid, lab] + [s[k] for k in keys] + [s["themes"][k] for k in THEMES])

    md = ["# Summary", "", "Generated by `tools/build.py` from `data/runs/`.", "",
          "| Run | Turns | Ended | Words/turn (first ¼ → last ¼) | First goodbye-loop turn | Emoji turns | Top words |",
          "|---|---:|---|---|---:|---:|---|"]
    for rid, lab, s in rows:
        md.append(f"| [{lab}](../transcripts/{rid}.md) | {s['turns']} | {s['reason'] or s['status']} | "
                  f"{s['words_first_quarter']} → {s['words_last_quarter']} | {s['first_goodbye_turn'] or '—'} | "
                  f"{s['emoji_turns']} | {s['top_words']} |")
    md += ["", "## Theme counts (turns mentioning each theme)", "",
           "| Run | " + " | ".join(THEMES) + " |", "|---|" + "---:|" * len(THEMES)]
    for rid, lab, s in rows:
        md.append(f"| {lab} | " + " | ".join(str(s["themes"][k]) for k in THEMES) + " |")
    (ROOT / "results/summary.md").write_text("\n".join(md) + "\n")
    print(f"built {len(rows)} runs")


if __name__ == "__main__":
    main()
