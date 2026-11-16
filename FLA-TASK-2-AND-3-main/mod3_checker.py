"""Task 2, Application 2 - Binary number divisible by 3 (M_MOD3).

State q_r means "the bits read so far have value with remainder r".
Reading bit b from q_r goes to q_((2r + b) mod 3).  Start and final: q0.
The most significant bit is read first.  The empty input has value 0, so
it is accepted (as stated in the report).
"""
from automata import DFA, report


def classify(w):
    if any(c not in "01" for c in w):
        raise ValueError("input must contain only the bits 0 and 1")
    return list(w)


def build():
    delta = {(f"q{r}", str(b)): f"q{(2 * r + b) % 3}" for r in range(3) for b in (0, 1)}
    return DFA("M_MOD3 (binary divisible by 3)", "q0", {"q0"}, delta, classify=classify)


ACCEPTED = ["11", "110", "1001", "1100", "10101"]
REJECTED = ["1", "10", "101", "111", "1000", "1101"]

if __name__ == "__main__":
    m = build()
    report(m, ACCEPTED, REJECTED)
    print("\nTraces (Table 7):")
    for w in ("1001", "1101"):
        print(m.trace(w), "  value =", int(w, 2))
