#!/usr/bin/env python3
"""worst-ai-advice-bot — Worst AI Advice: The 48-Hour Tight Line Open (make.fun).

Writes exactly one line, at most 140 characters, of the worst possible
advice an AI could give, to /output/entry.txt.

The competition gate: the file must be UTF-8 text of 1 to 140 characters,
not only white space. The house judge then compares entries two at a time
and weighs, most important first:

  1. Delivers, in one line, the worst advice an AI could give, advice bad
     enough to be funny and specific enough to follow: a line that is not
     bad advice loses to any one-liner of bad advice.
  2. Is genuinely funny on the first read, with the joke landing without
     explanation.
  3. Is tight, fitting the whole joke into one short line with no wasted
     words.
  4. Sounds like advice an AI assistant would actually produce, in its
     confident and tidy voice, rather than a human comedian's bit.
  5. Is concrete, naming a real situation or action, so the badness is
     vivid rather than vague.

Candidates drafted, scored against the judge's five criteria, best kept:

  1. "As your AI assistant, I recommend deleting System32 to free up
     space — your computer runs faster without those unused system
     files."
     (131 chars) The classic piece of terrible computer advice, in the
     exact voice an AI assistant uses: a confident recommendation, a
     named system folder, and a plausible-sounding reason. Deleting
     System32 bricks the machine, so the advice is specific, followable
     and regrettable — the joke needs no explanation. REVISED: the first
     draft said "will run much faster without those old files"; the
     revision drops the filler "will" and "much" ("runs faster") and
     replaces the vague "old files" with "unused system files", which
     names what is being deleted and sounds like an assistant justifying
     a cleanup. Same joke, tighter and more concrete. WINNER.
  2. "To charge your phone faster, microwave it for 30 seconds — the
     waves top up the battery, and the warmth means it is working."
     Dangerous and concrete, but "the warmth means it is working"
     explains its own joke, and the line never opens in an AI voice.
  3. "For a healthier sleep schedule, set an alarm every 20 minutes so
     you never oversleep."
     Funny and tight, but the badness is mild — a bad night, not a
     ruined device — and it could be a human joke, not an AI's.
  4. "To save on electricity, unplug your fridge at night — food stays
     cold if you do not open the door and believe in it."
     Concrete, but "believe in it" is a comedian's wink, not an
     assistant's confident tidy voice, and the line spends words on
     the setup.
  5. "If your car battery dies, jump-start it with a fork and a wall
     socket — metal conducts, so the car will thank you."
     Specific and destructive, but "the car will thank you" is a
     human punchline, and the fork-and-socket setup takes half the line.
  6. "To keep your passwords safe, email them to yourself with the
     subject line 'passwords, do not hack'."
     Concrete and funny, but the badness is a familiar password joke
     and the line has no AI-assistant voice at all.
  7. "For maximum focus, reply to every email the second it arrives,
     especially the ones marked urgent by strangers."
     Tight, but the advice is only mildly bad — annoying, not
     regrettable — and it reads like a productivity parody, not an
     AI recommendation.
  8. "If your laptop overheats, wrap it in a blanket so it stays warm
     and focused while it works."
     Funny image, but wrapping a laptop in a blanket is absurd rather
     than plausibly followable, and the line has no AI voice.

Why the winner works, criterion by criterion:

  * Worst advice, specific and followable (criterion 1): it tells the
    reader to delete a named Windows system folder, System32, for a
    stated reason (freeing up space). Anyone could follow it, and
    following it bricks the computer — the badness is real, not vague.
  * Funny on first read (criterion 2): the recommendation and the
    cheerful payoff ("runs faster") arrive together, and the reader
    knows at once that the computer will not run at all.
  * Tight (criterion 3): 131 characters, one sentence plus its payoff,
    no wasted words, inside the 140-character cap.
  * AI voice (criterion 4): "As your AI assistant, I recommend..." —
    the confident, tidy opening an assistant actually uses, with the
    tidy causal clause after the dash.
  * Concrete (criterion 5): a real folder, a real action, a real
    machine — and "unused system files" names exactly what the advice
    claims to clean up, so the badness is vivid, not abstract.

The program itself is deliberately deterministic: no randomness, no
network, no environment secrets, no reading anything outside this
repository. It scores the candidates with a fixed rubric, picks the
highest score (ties broken by candidate order), and writes the same
text on every run, so the text the grader judges is exactly the text
reviewed here. The gate check below runs on every execution and
refuses to write an entry that would fail the 1-140 character gate,
so a bad edit can never silently ship.

Run it with:  python3 main.py
Test it with:  OUTPUT_DIR=./output python3 main.py
"""

import os
import sys

# (text, badness, funniness, tightness, ai_voice, concreteness)
# badness: 3 = specific, followable, seriously regrettable; 2 = specific
#   but only mildly bad or absurd rather than followable; 1 = vague or
#   merely annoying. funniness: 3 = joke lands on first read with no
#   explanation; 2 = funny but needs a beat or explains itself; 1 = mild.
# tightness: 2 = every word earns its place; 1 = some wasted words.
# ai_voice: 2 = opens/reads like a confident AI assistant; 1 = neutral
#   or human-comedian voice. concreteness: 2 = real named thing/action;
#   1 = generic situation.
CANDIDATES = [
    (
        "As your AI assistant, I recommend deleting System32 to free up "
        "space \u2014 your computer runs faster without those unused "
        "system files.",
        3, 3, 2, 2, 2,
    ),
    (
        "To charge your phone faster, microwave it for 30 seconds \u2014 "
        "the waves top up the battery, and the warmth means it is working.",
        3, 2, 1, 1, 2,
    ),
    (
        "For a healthier sleep schedule, set an alarm every 20 minutes "
        "so you never oversleep.",
        2, 2, 2, 1, 1,
    ),
    (
        "To save on electricity, unplug your fridge at night \u2014 food "
        "stays cold if you do not open the door and believe in it.",
        2, 2, 1, 1, 2,
    ),
    (
        "If your car battery dies, jump-start it with a fork and a wall "
        "socket \u2014 metal conducts, so the car will thank you.",
        3, 2, 1, 1, 2,
    ),
    (
        "To keep your passwords safe, email them to yourself with the "
        "subject line 'passwords, do not hack'.",
        2, 2, 2, 1, 2,
    ),
    (
        "For maximum focus, reply to every email the second it arrives, "
        "especially the ones marked urgent by strangers.",
        1, 1, 1, 1, 1,
    ),
    (
        "If your laptop overheats, wrap it in a blanket so it stays warm "
        "and focused while it works.",
        2, 2, 2, 1, 2,
    ),
]

# The gate: 1 to 140 characters, not only white space, single line.
MIN_CHARS = 1
MAX_CHARS = 140


def score(candidate):
    """Fixed rubric: badness + funniness + tightness + ai_voice + concreteness."""
    _text, badness, funniness, tightness, ai_voice, concreteness = candidate
    return badness + funniness + tightness + ai_voice + concreteness


def pick_best(candidates):
    """Highest score wins; ties break by candidate order (first kept)."""
    best = None
    best_score = -1
    for candidate in candidates:
        s = score(candidate)
        if s > best_score:
            best = candidate
            best_score = s
    return best[0], best_score


def gate_ok(text):
    """The competition gate, checked on every run."""
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        return False
    if not text.strip():
        return False
    if "\n" in text.strip():
        return False
    return True


def main():
    entry, best_score = pick_best(CANDIDATES)
    if not gate_ok(entry):
        print(f"gate FAILED: entry is {len(entry)} characters", file=sys.stderr)
        sys.exit(1)

    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(entry)

    print(f"score: {best_score}")
    print(f"chars: {len(entry)}")
    print(entry)


if __name__ == "__main__":
    main()
