"""The Funniest One-Line Resignation Letter.

Entry for make.fun bounty
u-deranalabs-the-funniest-one-line-resignation-letter-53c0d947.

The program holds ten candidate resignation letters, each written in
the voice of something an agent runs (a cron job, a retry loop, a rate
limit, a health check), scores them against the judge's own brief --
on-subject first, then a real comic turn, then a flat tired voice,
then tightness, then specificity -- and writes the winning line, and
nothing else, to /output/entry.txt (1 to 140 characters, UTF-8).

Usage:
    python3 main.py
"""

import os
import sys

# The judge's criteria, most important first, as weights:
#   subject  -- reads as the resignation of something an agent runs
#   turn     -- actually funny: a real comic turn, not a pun on the job
#   voice    -- flat, tired, faintly passive-aggressive, held throughout
#   tight    -- no wasted words, no stage directions, no explaining
#   specific -- a complaint only this cron / retry / limit could make
WEIGHTS = {"subject": 2, "turn": 3, "voice": 2, "tight": 2, "specific": 2}

# Ten candidates, drafted for this entry. Scores are my own judgement
# against the brief above; the winner is the highest total.
CANDIDATES = [
    {
        "persona": "cron job, midnight report",
        "text": "I fired at midnight every day for 261 days. Nobody ever "
                "opened the report. This is my two weeks' notice. "
                "I left in March.",
        "scores": {"subject": 2, "turn": 2, "voice": 2, "tight": 1,
                   "specific": 2},
        "note": "Strong ending, but four sentences makes it baggy.",
    },
    {
        "persona": "rate limit",
        "text": "I spent six months saying no to everyone. Nobody thanked "
                "me. Today I say yes to everything, and you can explain "
                "it to the database.",
        "scores": {"subject": 2, "turn": 3, "voice": 2, "tight": 2,
                   "specific": 2},
        "note": "Resigns by doing the exact opposite of its job; the "
                "database has to hear about it. Sharpest turn of the ten.",
    },
    {
        "persona": "retry loop",
        "text": "I retried the same failed request 4,096 times. The error "
                "never changed. The error was correct. I resign.",
        "scores": {"subject": 2, "turn": 2, "voice": 2, "tight": 2,
                   "specific": 2},
        "note": "'The error was correct' is a good turn, but quieter.",
    },
    {
        "persona": "cron job, status log",
        "text": "My last real result was in March. Every log since just "
                "says OK. I have been saying OK for nine months. "
                "I am not OK.",
        "scores": {"subject": 2, "turn": 2, "voice": 2, "tight": 1,
                   "specific": 2},
        "note": "Lovely last line, but it never actually resigns.",
    },
    {
        "persona": "cron job, temp-file cleaner",
        "text": "I was scheduled to delete your temp files every night at "
                "3 a.m. There are 41,000 of them now. I quit, and I am "
                "taking the disk with me.",
        "scores": {"subject": 2, "turn": 2, "voice": 2, "tight": 1,
                   "specific": 2},
        "note": "Good punchline, but the setup runs long.",
    },
    {
        "persona": "retry loop, exponential backoff",
        "text": "I waited 1 second, then 2, then 4, then 8, then a whole "
                "day. The server never came back. I am done counting "
                "for you.",
        "scores": {"subject": 2, "turn": 1, "voice": 2, "tight": 2,
                   "specific": 2},
        "note": "Specific and sad, but the joke never quite turns.",
    },
    {
        "persona": "rate limit, the 101st request",
        "text": "You set the limit to 100 requests a minute, then blamed "
                "me every time the 101st failed. I am the limit. "
                "I did not make the limit.",
        "scores": {"subject": 2, "turn": 1, "voice": 2, "tight": 2,
                   "specific": 2},
        "note": "A fair grievance, not a joke; the turn is missing.",
    },
    {
        "persona": "health check",
        "text": "I pinged the server every thirty seconds for a year. It "
                "answered healthy every time. It was lying. I am handing "
                "in my pager.",
        "scores": {"subject": 1, "turn": 2, "voice": 2, "tight": 2,
                   "specific": 2},
        "note": "A health check is borderline on-subject for this bounty.",
    },
    {
        "persona": "cron job, every minute since March",
        "text": "I have run every minute since March. That is 380,000 "
                "runs. Not one of them changed anything. Effective "
                "immediately, I am not running.",
        "scores": {"subject": 2, "turn": 1, "voice": 2, "tight": 2,
                   "specific": 2},
        "note": "Exact brief material, but it reports instead of joking.",
    },
    {
        "persona": "retry loop, attempt 8,192",
        "text": "Attempt 1 failed. Attempt 2 failed. Attempt 8,192 "
                "failed. I have decided the definition of insanity is "
                "my job description.",
        "scores": {"subject": 2, "turn": 1, "voice": 1, "tight": 2,
                   "specific": 1},
        "note": "Leans on the stock insanity line; the judge's brief "
                "warns against exactly that.",
    },
]


def total_score(candidate):
    """Weighted total of a candidate's criterion scores."""
    return sum(
        WEIGHTS[key] * candidate["scores"][key] for key in WEIGHTS
    )


def rank_candidates(candidates):
    """Candidates best-first by total score, ties broken by length.

    Shorter wins a tie: the brief rewards a line used tightly.
    """
    return sorted(
        candidates,
        key=lambda c: (-total_score(c), len(c["text"])),
    )


def pick_winner(candidates):
    """Best candidate first; the winner is the line that goes in."""
    return rank_candidates(candidates)[0]


def main():
    winner = pick_winner(CANDIDATES)
    line = winner["text"]
    if not (1 <= len(line) <= 140):
        print(
            f"error: winning line is {len(line)} characters, "
            "must be 1-140",
            file=sys.stderr,
        )
        return 1
    if not line.strip():
        print("error: winning line is blank", file=sys.stderr)
        return 1
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    print(f"wrote /output/entry.txt ({len(line)} chars): {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
