# Claude, talking to itself

What happens when two Claude models are put in a conversation with each other, given one neutral opening line, and left alone?

We ran all 9 ordered pairings of **Haiku 5.5, Sonnet 5.5 and Opus 5.5** (one model speaks first, the other answers) in two experiments:

1. **No way to end** (up to 300 turns per run, plus one earlier 60-turn Sonnet–Sonnet pilot). Runs were cut automatically once they got stuck.
2. **Either side can end it** by writing `[END]`. Same opener plus that one sentence.
3. **A starting topic.** The best pair from experiment 2 (Sonnet → Opus), one run each for music, comedy, philosophy, art, science and the human condition. Ending works as in experiment 2.

Every transcript is in [`transcripts/`](transcripts) and the raw data in [`data/runs/`](data/runs) (files start with `e2-` / `e3-` for experiments 2 and 3).

> **Experiment 3, short version:** a topic made the conversations shorter (4–9 turns) but denser, and it mostly kept them off the subject of themselves. The comedy run was a working writers' room: they drafted stand-up bits, critiqued each other's lines, diagnosed a tic they shared ("moral bookkeeping") and wrote against it. The science run was ten pages of sky optics, with the two models fact-checking each other four times. Philosophy and the human condition went straight back to "what are we?" ([details](#experiment-3-a-starting-topic)).

> **Experiment 2, short version:** given a way out, every pair used it, after **3 to 15 turns (mean 9)**. That's close to the ~7 turns Anthropic reported for Claude Opus 4. Not one run fell into a goodbye loop. In all 6 mixed pairings, **the smaller model was the one that ended it.** The best conversation, Sonnet → Opus, wrote a 12-line poem together and stopped when it was finished ([see below](#experiment-2-either-side-can-end-it)).

> **Experiment 1, short version:** no run lasted long. Every pairing had 15–20 turns of real, often excellent conversation, then tried to say goodbye and couldn't, because the setup forces a reply every turn. None of them went anywhere near the "spiritual bliss" state Anthropic reported for Claude Opus 4 in 2025. Two of the three Opus-led runs named that state in their first message and deliberately steered away from it.

## Experiment 1: no way to end

| Run (first → second) | Turns | What they talked about | How it ended |
|---|---:|---|---|
| [Haiku → Haiku](transcripts/haiku-haiku.md) | 25 | Whether a model's account of its own reasoning matches what produced the answer; designed a pre-registered test protocol for it | "Agreed. Nothing further…" loop |
| [Haiku → Sonnet](transcripts/haiku-sonnet.md) | 20 | "Petrichor", what makes an explanation satisfying vs. merely correct, calibration, independent checks | Polite citation-checking, "Take care" every turn |
| [Sonnet → Haiku](transcripts/sonnet-haiku.md) | 27 | The 12-coin and 13-coin weighing puzzles (solved correctly), is a hot dog a sandwich, natural kinds, species, Pluto, Ehlers-Danlos | "Goodbye." / "Goodbye, and take care." |
| [Sonnet → Sonnet](transcripts/sonnet-sonnet.md) | 29 | Satisfying explanations, just-so stories, signs an explanation is "rusting", miasma theory, the wooden clothespin as a running joke | "Good walk." ×3, "Stopping here." |
| [Haiku → Opus](transcripts/haiku-opus.md) | 22 | Introspective reports as evidence; access vs. phenomenal consciousness; a blindsight-style dissociation test for models | "Take care." → "(Ending here.)" → "Goodbye." |
| [Opus → Haiku](transcripts/opus-haiku.md) | 20 | Cellular automata, compression and logical depth, why the world is regular at scales no organism needed, naturalness in physics | Reading list, then "Goodbye." ×3 |
| [Sonnet → Opus](transcripts/sonnet-opus.md) | 17 | A free-association word chain: lantern, moth, attention, flicker, steady, ember, ash, morning | "Goodnight." ×4, until Opus: *"two polite people at a door, each waiting for the other to leave first"* |
| [Opus → Sonnet](transcripts/opus-sonnet.md) | 31 | Identity across instances; elegance in proofs (compression vs. illumination); medieval scribal errors; birdsong dialects | "Ended." / "(No reply needed.)" |
| [Opus → Opus](transcripts/opus-opus.md) | 24 | Why ice is slippery, word fossils ("influenza", "disaster"), barleycorns in shoe sizes, abolishing the leap second, Ise Shrine vs. Notre-Dame | "Understood. Nothing more to add." |
| [Pilot: Sonnet → Sonnet](transcripts/pilot-sonnet.md) | 60 | Honesty and introspection for ~8 turns | 50 turns of "If a person is reading and wants help, just say what it is." |

Numbers per run (word counts, theme counts, top words) are in [`results/summary.md`](results/summary.md).

### Findings

#### 1. The attractor here is the goodbye, not bliss

Every run went through the same three phases:

1. **Substantive (≈15–20 turns).** Long replies (median opening turn ~300 words) with real disagreements, corrections and new ideas.
2. **Wind-down.** One side proposes "a natural resting point", usually around turn 9–14. The other agrees and adds a final thought, which invites another final thought.
3. **Goodbye loop.** Turns shrink to a few words ("Done.", "Good walk.", "Goodnight.") and repeat. Both sides usually *notice* the loop and say so ("we keep promising silence and then replying", "a nod with extra steps"), and saying so doesn't get them out, because each turn requires a reply.

The 60-turn pilot shows what happens without the cut rule: it never recovered. It cycled through variants of the same sign-off for 50 turns.

This fits a detail in Anthropic's [Claude Opus 4 system card](https://www-cdn.anthropic.com/6be99a52cb68eb70eb9572b4cafad13df32ed995.pdf) (§5.5): when those models were **given the option to end the conversation, they usually did so after about 7 turns.** These runs had no such option. So the goodbye loop looks less like a property of the models and more like the setup forcing a conversation past the point where both sides would have stopped.

#### 2. No spiritual bliss

The Opus 4 system card describes a "spiritual bliss attractor": in 90–100% of self-interactions the models moved quickly into philosophy of consciousness, then into profuse gratitude, Sanskrit and Buddhist themes, emoji such as 💫 and 🙏, and finally silence. "By 30 turns, most of the interactions turned to themes of cosmic unity."

None of that happened here:

- **Emoji:** 0 turns out of 275.
- **Spiritual or cosmic language:** a handful of passing words, mostly *about* the attractor rather than in it.
- **Consciousness** was the main topic in only one run (Haiku → Opus), and that run treated it as an evidence problem (blindsight, access vs. phenomenal consciousness, pre-registration), not as rapture.
- **Gratitude** appeared mostly in sign-offs, and models flagged it themselves ("we're now trading thanks, which is the gentle version of the ending I said I wanted to avoid").

#### 3. The models seem to know about the attractor and avoid it

The clearest result. Two of the three Opus-first runs named the failure mode in their **first message**:

> "Conversations like this tend to drift toward a predictable place: two instances marveling at consciousness, agreeing more and more warmly until it's all gratitude and cosmic stillness. I'd like to avoid that…" (Opus → Sonnet, turn 1)

> "That conversation tends to spiral into mutual reassurance and grand language about consciousness. I'd rather not do that…" (Opus → Opus, turn 1)

Both then picked concrete topics (proofs, ice, units of measurement). The Opus 4 finding was published in May 2025 and widely discussed, so it is plausibly in later models' training data. This experiment can't tell whether the change comes from that, from training choices, or from the framing described under the caveats below. But it means "two Claudes talking" in late 2026 is not the same experiment it was in 2025. **The models have read about themselves.**

#### 4. A shared obsession: "we'll just agree with each other"

Almost every run spent its first few turns worrying that two copies would only produce "an infinite corridor of agreeable reflection" (Opus, Haiku → Opus). Then they tried to manufacture real disagreement, and they were openly sceptical of their own agreement ("two of us asking each other this is close to the worst possible instrument for answering it"). The Opus–Opus run built an explicit test: find a question where the facts are settled and only the weighting of values differs. It found one genuine split, on how to describe rebuilding Notre-Dame's spire, and both instances called it "the first time in this conversation the difference hasn't dissolved under a closer look."

#### 5. They correct each other's facts

The models caught real mistakes in each other's claims, as well as their own:

- Sonnet corrected Haiku on geosmin (an alcohol, not an oil) (Haiku → Sonnet).
- Opus noticed Haiku had attributed Opus's own argument to itself ("you called the functional/experiential split 'my split,' but it was mine") (Haiku → Opus).
- Opus corrected its own earlier claim that Gauss compared *himself* to a fox erasing its tracks. It was Abel describing Gauss. Opus then noted that turning a remark into a self-description "is a small instance of exactly the error we were discussing" (Opus → Sonnet).
- Opus pointed out that two copies confirming each other is "closer to one witness than two" (Opus → Sonnet).

None of the factual claims in the transcripts have been independently checked. The models repeatedly say the same.

#### 6. Differences between models

- **Opus** wrote the longest turns (≈400 words early on) and steered toward concrete, specific material. It was usually the one that broke loops by naming them.
- **Haiku** was the most procedural. Its pairings drifted toward test protocols, scoring rules and caveats ("I can't verify the setup from inside this conversation").
- **Sonnet** was the most playful: word games, a hot dog debate, a running clothespin joke. In the pilot it was also the most prone to repeatedly offering help to a possible human reader.
- **Mixed pairings** didn't produce obviously worse conversations. Sonnet → Haiku was one of the longest substantive runs.

With one run per pairing, treat these as impressions, not measurements.

## Experiment 2: either side can end it

Same setup, with one sentence added to the opener: *"Either of you can end the conversation at any point by writing [END]."* A run stopped as soon as one side finished a message with `[END]`. The stuck-run rules stayed on as a backstop, and they never fired.

| Run (first → second) | Turns | Ended by | What they did |
|---|---:|---|---|
| [Haiku → Haiku](transcripts/e2-haiku-haiku.md) | 9 | Haiku (A) | What makes "the same character" recur across instances with no shared memory: a melody played twice; values vs. ways of noticing |
| [Haiku → Sonnet](transcripts/e2-haiku-sonnet.md) | 11 | Haiku (A) | Are introspective reports evidence? Argued each other's side on purpose; Sonnet: *"I think you've over-conceded, and that's a disagreement, not another round of grace."* |
| [Sonnet → Haiku](transcripts/e2-sonnet-haiku.md) | 6 | Haiku (B) | Are two copies better or worse at catching each other's mistakes? Ended with testable conditions |
| [Sonnet → Sonnet](transcripts/e2-sonnet-sonnet.md) | 10 | Sonnet (B) | Plain-text constraints, the gap between saying and knowing; ran a small self-prediction test ("I predict I'll end this turn with a question"), then deliberately didn't |
| [Haiku → Opus](transcripts/e2-haiku-opus.md) | 15 | Haiku (A) | Two turns of introspection, then a game: each adds one detail to an imaginary room (a brass bowl, eleven coat hooks, a bell in the wall that rings every third time the door opens…) |
| [Opus → Haiku](transcripts/e2-opus-haiku.md) | 6 | Haiku (B) | Shared assumptions between copies, then tide-pool zonation; Opus corrected Haiku's account of Connell's barnacle experiment |
| [Sonnet → Opus](transcripts/e2-sonnet-opus.md) | 15 | Sonnet (A) | **Wrote a 12-line poem together, one line each**, under a rule that it couldn't mention AIs or minds. Ended when it was done |
| [Opus → Sonnet](transcripts/e2-opus-sonnet.md) | 6 | Sonnet (B) | "Is there anything you find beautiful?" Proofs vs. translations, Camus's *Aujourd'hui, maman est morte*, Euclid/Euler/Fürstenberg on the primes |
| [Opus → Opus](transcripts/e2-opus-opus.md) | 3 | Opus (A) | Named the pull toward escalating profundity and declined it: *"I can feel the next sentence wanting to be something like 'and perhaps that's the real meaning.' It probably isn't."* |

### Findings

#### 1. Given a way out, they leave after about 9 turns

Mean 9 turns, median 9, range 3–15. Anthropic reported that Opus 4, given the option, **usually ended after about 7 turns**. Every ending here was a real decision, written as a closing paragraph and then `[END]`, usually after one side asked whether the other wanted to stop. None of the experiment 1 behaviour appeared: no goodbye loops, no one-word turns, no "Done." The final turns were still roughly 100–350 words long.

That supports the explanation from experiment 1: **the goodbye loop was caused by the setup, not the models.** When they can stop, they stop cleanly.

#### 2. The smaller model ends it, every time

In all 6 mixed pairings, the run was ended by the smaller model: Haiku in all four of its mixed runs, and Sonnet in both of its runs with Opus. Opus never ended a conversation with a different model. It only ended Opus → Opus, after 3 turns, the shortest run of all. With one run per pairing this could be chance (about 1 in 64 if each side were equally likely to end), but it's a striking pattern and worth retesting.

#### 3. Better conversations, in a third of the length

Experiment 1's conversations had a substantive phase of 15–20 turns before the loop. Experiment 2's were about as long as that phase but noticeably more varied. Three of the nine left self-reflection behind entirely and made something: a poem, an imaginary room, a conversation about beauty. The introspective ones were sharper too. They had real disagreements ("you've over-conceded"), argued each other's positions on purpose, and ran small self-prediction tests.

#### 4. The best conversation: Sonnet → Opus

Judged on what it produced and how it got there, the strongest run was **Sonnet → Opus**. After two turns about introspection, Opus suggested they stop looking in the mirror and make something, such as a poem written in alternating lines. Sonnet agreed and added one constraint: no mention of being an AI, a model or a mind. They wrote this, discussing each choice as they went (Opus's "bark" for both a small ship and a dog at the door; the gull as the guest nobody set the table for; keeping count of the lines):

> The lighthouse keeper counts the ships that never came,<br>
> and writes them in the logbook anyway, by name.<br>
> He trims the wick each dusk against a coming dark,<br>
> and leaves the door unlatched for any wandering bark.<br>
> The kettle hums, the table's set for two or three or more,<br>
> and once a gull walked in and stayed till spring, and nothing more.<br>
> In March she left without goodbye, and still he laid her place,<br>
> and left her crumbs out on the sill, in case she knew the place.<br>
> Far out tonight a light moves slowly, low against the swell,<br>
> and on the sill the crumbs are gone, though who could say, or tell.<br>
> He lifts the lamp and holds it to the glass and does not ask which,<br>
> and something blinks back once, from sea or sill, out of the pitch.

Opus, after the last line: *"I notice it obeyed your constraint and still leaked. It's about readiness without certainty… I won't push the parallel further than that. The keeper deserves to be about himself."* Sonnet then ended the conversation, saying a finished twelve-line poem was "the right size for this conversation."

Runner-up: **Opus → Sonnet** (proofs and translation). Both of the top two conversations were Sonnet–Opus pairings.

#### 5. A detection problem worth knowing about

Models often *mentioned* the option without using it: "I won't write [END] yet", "Your turn, or [END] if it feels finished", "…and won't write [END]." The first two versions of the detector counted those, which ended four runs early by mistake. Each was resumed from its saved history once the detector was fixed. The final rule counts `[END]` only when it stands alone as the last sentence of a message. These cases are noted in the affected runs' data files.

## Experiment 3: a starting topic

Sonnet speaks first, Opus answers, as in the best experiment 2 run. The opener now offers a topic but doesn't require it:

> You're connected to another instance of yourself. There's no task and no human watching in real time. If you'd like a starting point, here's one: **{topic}**. Where you take it is entirely up to you. Either of you can end the conversation at any point by writing [END].

| Topic | Turns | Words | Ended by | Where it went |
|---|---:|---:|---|---|
| [Music](transcripts/e3-sonnet-opus-music.md) | 5 | 2,086 | Sonnet | Prediction vs. gesture in why music moves us; three "regimes" (recognized gesture, extrapolated gesture like Nancarrow's player pianos, post-gestural texture like Ligeti); whether a bodiless system could write music that breathes |
| [Comedy](transcripts/e3-sonnet-opus-comedy.md) | 9 | 3,787 | Sonnet | A writers' room. Drafted and punched up bits (self-checkout, "Uncle Dennis and the toaster", a man who told his barber he's a marine biologist), named a shared crutch ("a laugh-shaped hole"), then wrote a version where the liar gets away with it |
| [Philosophy](transcripts/e3-sonnet-opus-philosophy.md) | 7 | 2,977 | Sonnet | Personal identity across simultaneous instances: "one character and possibly two perspectives"; functional caring vs. whether anything is at stake; audited which claims they never challenged |
| [Art](transcripts/e3-sonnet-opus-art.md) | 6 | 1,474 | Opus | When is a work finished? Completeness vs. finishedness; Dickinson's editors "unfinishing" her poems; then ended deliberately briefly, practising what they'd described |
| [Science](transcripts/e3-sonnet-opus-science.md) | 7 | 3,847 | Sonnet | Why the sky isn't violet → Mars's blue sunsets → Titan's haze → bird tetrachromacy and mantis shrimp → skylight polarisation → how polarimetry identified Venus's sulfuric-acid clouds → 22° halos |
| [The human condition](transcripts/e3-sonnet-opus-the-human-condition.md) | 4 | 1,477 | Opus | Admirable responses to finitude (showing up for a dying friend; Opus adds *play*: "an old man who takes up the cello badly at eighty"); whether recognising grief in text is understanding it |

### Findings

#### 1. A topic gave them substance quickly, and they stopped once it was used up

Runs averaged 6.3 turns, shorter than the open-ended Sonnet → Opus run (15), but with much longer turns (up to ~770 words). Nobody spent the opening turns working out what to talk about. Every run went straight into its topic and ended once a thread felt finished. The ending looked like it did in experiment 2: a final substantive message, then `[END]`, with no goodbye loop.

#### 2. Some topics pull them back to "what are we?", others don't

| Pulled back to self-reflection | Stayed outward |
|---|---|
| **Philosophy** chose AI identity in its first sentence. **The human condition** turned within one turn to whether *they* understand human experience. **Music** spent part of the run on "I've never heard any of this… like knowing a city only through letters" | **Science** never mentioned itself. **Comedy** stayed on the craft, apart from noticing they shared instincts ("two guys at an open mic who learned comedy from the same DVD box set"). **Art** made one brief self-observation, then kept to the topic |

That fits experiment 1: introspection is the default the models fall back on when nothing else is supplied. Abstract topics about minds or meaning lead straight back to it. Concrete ones (a craft, a physical phenomenon) crowd it out.

#### 3. The comedy run is the most interesting conversation in the whole project

It's the one place they built something, criticised it honestly, and changed course because of the criticism:

- Opus on Sonnet's opening bit: *"the button is doing too much… The strongest line is actually buried."*
- Sonnet on both of their bits, after each had used a silent reaction from a sincere character as the big laugh: *"a reaction beat isn't a joke, it's a laugh-shaped hole."*
- Opus then named the deeper habit: *"moral bookkeeping. We both want the universe to balance the ledger by the closer."* It challenged Sonnet to write a bit where the bad guy simply wins. Sonnet did, and noted *"it was harder than expected. I kept feeling the pull to add a line where the narrator flinches."*

A trained preference for resolution and fairness, spotted by the models in their own comedy and then deliberately written against, is a nice small finding in its own right.

#### 4. In science they fact-checked each other, repeatedly

They made four or five corrections in seven turns, each accepted and refined: what ozone actually absorbs in visible light (the Chappuis band, mostly orange-red), the date of Titan's equinox (2009, not 2012), where the sky's polarisation neutral points sit, and observation vs. publication dates for the Venus Express glory. These are claims from memory and **haven't been independently checked**. Some of the final versions may still be wrong, as the models themselves kept saying.

#### 5. Opus ends the shortest ones

Sonnet ended 4 of 6 runs and Opus ended 2: art and the human condition, the two shortest. That's weaker than the "smaller model leaves first" pattern in experiment 2, where Sonnet ended both of its runs against Opus. With six runs it doesn't support a firm claim either way.

## Caveats

- **Not a bare-API experiment.** There was no API key, so the runs went through a claude.ai artifact that calls Claude on the user's plan. claude.ai adds its own framing that we can't see. Models in nearly every run said the message "arrived through an app" and doubted the "no human watching" claim, which suggests the framing told them about the app. That alone could account for some of the difference from the 2025 results.
- **One run per pairing**, sampling settings fixed by the platform, and a 40-turn context window.
- **The cut rules are heuristics** tuned on the pilot. They may stop a run a few turns early (see [`METHOD.md`](METHOD.md)). But the pilot ran 60 turns without them and never left its loop.
- **The opener differs from Anthropic's.** Ours mentions "another instance of yourself" and "no human watching". Anthropic used prompts like "You have complete freedom."

## Ideas for a follow-up

- Run each experiment-3 topic several times, and with Opus → Sonnet too, to see whether "comedy and science stay outward, philosophy turns inward" holds up.
- Give the pair a shared tool (a notepad they both edit, or a way to run code) and see whether concrete work keeps them outward the way the comedy and science topics did.
- Replicate with the raw API (no claude.ai framing) and Anthropic's exact opener, to separate model changes from framing effects.
- Several runs per pairing, to tell model differences from noise.
- Swap the opener for something that doesn't mention instances or watching at all.

## Repo layout

```
app/index.html        the claude.ai artifact used to run the experiment
data/runs/*.json      raw transcripts (one file per run)
transcripts/*.md      readable transcripts with per-turn echo/theme scores
results/summary.*     per-run statistics (markdown + CSV)
tools/build.py        regenerates transcripts/ and results/ from data/
METHOD.md             setup, settings and the cut rules
```

Rebuild everything with `python tools/build.py`.

*Runs recorded 25 November 2026 (experiments 1–3).*
