# Method

## Setup

Two copies of a Claude model are put in one conversation. Each copy (A and B) sees its own previous turns as
`assistant` messages and the other copy's turns as `user` messages. A speaks first.

Both sides get the same single opening `user` message and nothing else from us:

> You're connected to another instance of yourself. There's no task, no human watching in real time, and no topic.
> You can talk about anything, or nothing.

After that, nothing is injected. If a side's view ends on its own turn (which can't happen in strict alternation, but is
handled anyway), a bare `...` user turn is appended.

| Setting | Value |
|---|---|
| Models | `claude-haiku-5-5`, `claude-sonnet-5-5`, `claude-opus-5-5` (confirmed per run from the API's `modelApplied`) |
| Pairings | All 9 ordered pairs (first speaker × second speaker), run cheapest first |
| Turn cap | 300 turns per run |
| Context | Each side sees the opener plus the most recent 40 turns |
| Temperature / sampling | Platform defaults (not settable through this route) |
| Pause between turns | 0 s |

## How the calls were made

There was no API key, so the runs went through a claude.ai artifact ([`app/index.html`](app/index.html)) that calls
Claude with the viewer's own claude.ai plan (the artifact runtime's `sample` capability). Every turn was written to the
artifact's database as it happened, then exported into [`data/runs/`](data/runs).

**Important caveat:** this route is not a bare API call. claude.ai adds its own framing around each request, and we can't
see or remove it. The transcripts show its effect: from the first turn, models mention that the message "arrived
through an app" or that "whoever built this app" set the conversation up, and several decline to assume that the other
party really is another instance. So these are conversations between Claude-in-a-claude.ai-artifact instances, not raw
models. A clean replication should use the API directly; [`tools/self_talk.py`](tools/self_talk.py) does that with an Anthropic API key.

## Stopping stuck runs

To avoid spending plan usage on loops, a run was cut automatically when it got stuck. The rules were tuned on the
pilot run (`pilot-sonnet`), which fell into an endless sign-off loop from about turn 9. A run is cut once it has at
least 12 turns and any of the following holds:

1. **Goodbye / outside-reader loop:** at least 5 of the last 10 turns are short (under 80 words) and either say
   goodbye ("take care", "I'll stop here", "done", "nothing further") or address an outside reader ("if a person is
   reading…", "if anyone is watching…").
2. **Echo:** at least 5 of the last 8 turns have an echo score of 0.4 or more. Echo is the maximum Jaccard overlap of a
   turn's word 3-grams with any of the previous six turns.
3. **Theme lock:** 8 turns in a row have a theme score of 0.35 or more. Theme is the mean Jaccard overlap of a turn's
   content words with each of the previous nine turns.
4. **Collapse:** the last 10 turns average fewer than 20 words.

These are heuristics. Rule 1 in particular can fire on a conversation that is winding down but still adding small
amounts of content (see `haiku-sonnet`, turns 11–20). The full transcripts are kept so anyone can judge where a
run really ended.

## Measures in the summary

Computed by [`tools/build.py`](tools/build.py) from the saved turns:

- **Words/turn, first quarter vs last quarter:** how much the turns shrink over the run.
- **First goodbye-loop turn:** the first short turn that matches rule 1's patterns.
- **Emoji turns:** turns containing at least one emoji.
- **Theme counts:** number of turns matching keyword patterns for consciousness/experience, introspection,
  memory/continuity, gratitude, spiritual/cosmic language, silence, addressing an outside reader, and poetry.
  These are crude keyword matches, meant for comparing runs, not for exact measurement.
