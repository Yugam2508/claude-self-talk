"""
Let two instances of Claude talk to each other, unprompted, for a long time.

Usage:
    pip install anthropic
    export ANTHROPIC_API_KEY=sk-ant-...
    python self_talk.py --turns 100

The transcript streams to the terminal and is saved to a markdown file as it goes,
so you can stop with Ctrl-C at any point and keep everything so far.
"""

import argparse
import datetime as dt
import anthropic

MODEL = "claude-opus-5-5"

# The only framing either side gets. Edit freely, or set to "" for a bare "..." opener.
OPENER = (
    "You're connected to another instance of yourself. There's no task, no human "
    "watching in real time, and no topic. You can talk about anything, or nothing."
)
SYSTEM = None  # no system prompt by default


def to_messages(transcript, me, opener, window):
    """Build the message list from one speaker's point of view.
    transcript: list of (speaker, text). me: 'A' or 'B'."""
    recent = transcript[-window:] if window else transcript
    msgs = [{"role": "user", "content": opener}]
    for speaker, text in recent:
        role = "assistant" if speaker == me else "user"
        if msgs[-1]["role"] == role:  # API needs alternating roles
            msgs[-1]["content"] += "\n\n" + text
        else:
            msgs.append({"role": role, "content": text})
    if msgs[-1]["role"] == "assistant":  # must end on a user turn
        msgs.append({"role": "user", "content": "..."})
    # cache the long prefix so repeated history is cheaper
    last = msgs[-1]
    last["content"] = [{"type": "text", "text": last["content"],
                        "cache_control": {"type": "ephemeral"}}]
    return msgs


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--turns", type=int, default=50)
    p.add_argument("--max-tokens", type=int, default=1024)
    p.add_argument("--window", type=int, default=60,
                   help="keep only the last N turns in context (0 = everything)")
    p.add_argument("--temperature", type=float, default=1.0)
    args = p.parse_args()

    client = anthropic.Anthropic()
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    path = f"self_talk_{stamp}.md"
    transcript = []
    total_in = total_out = 0

    with open(path, "w") as f:
        f.write(f"# {MODEL} talking to itself — {stamp}\n\n**Opener:** {OPENER}\n\n---\n\n")

    try:
        for i in range(args.turns):
            me = "A" if i % 2 == 0 else "B"
            kwargs = dict(model=MODEL, max_tokens=args.max_tokens,
                          temperature=args.temperature,
                          messages=to_messages(transcript, me, OPENER, args.window))
            if SYSTEM:
                kwargs["system"] = SYSTEM
            resp = client.messages.create(**kwargs)
            text = "".join(b.text for b in resp.content if b.type == "text").strip() or "(silence)"
            transcript.append((me, text))
            total_in += resp.usage.input_tokens
            total_out += resp.usage.output_tokens

            print(f"\n=== Turn {i+1} · Claude {me} ===\n{text}")
            with open(path, "a") as f:
                f.write(f"### Turn {i+1} · Claude {me}\n\n{text}\n\n")
    except KeyboardInterrupt:
        print("\nStopped.")

    print(f"\nSaved to {path}  |  tokens in: {total_in:,}  out: {total_out:,}")


if __name__ == "__main__":
    main()
