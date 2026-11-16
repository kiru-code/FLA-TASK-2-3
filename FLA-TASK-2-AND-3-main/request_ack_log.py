"""Task 3, Case Study 2 - Request-acknowledgement log validator.

Language  L_log = { r^n a^(2n) | n >= 1 }
CFG  G2:  S -> r S a a | r a a
PDA  P2:  Q = {q0, q1, q2}, Gamma = {X, Z0}, F = {q2}   (deterministic)
Every r pushes two markers X; every a pops one X.
"""
from automata import PDA, EPS, report


def build():
    d = {
        ("q0", "r", "Z"): {("q0", "XXZ")},   # push (first r): two X
        ("q0", "r", "X"): {("q0", "XXX")},   # push (more r): replace X by XXX
        ("q0", "a", "X"): {("q1", EPS)},     # first a: pop one X, go to q1
        ("q1", "a", "X"): {("q1", EPS)},     # later a: pop one X
        ("q1", EPS, "Z"): {("q2", "Z")},     # accept: only Z0 left
    }
    return PDA("P2 (request-acknowledgement log)", "q0", {"q2"}, d)


def derive(n):
    """Leftmost derivation of r^n a^(2n) in G2."""
    if n < 1:
        raise ValueError("n must be at least 1")
    steps, left, right = ["S"], "", ""
    for _ in range(n - 1):
        left, right = left + "r", right + "aa"
        steps.append(f"{left}S{right}")
    steps.append("r" * n + "a" * (2 * n))
    return " => ".join(steps)


ACCEPTED = ["raa", "rraaaa", "rrraaaaaa", "rrrraaaaaaaa", "rrrrraaaaaaaaaa"]
REJECTED = ["ra", "raaa", "rraaa", "rraaaaa", "aar", "raraa", ""]

if __name__ == "__main__":
    p = build()
    report(p, ACCEPTED, REJECTED)
    print("\nDerivations:")
    print("  n=2:", derive(2))
    print("  n=3:", derive(3))
    print()
    print(p.trace("rraaaa"))
    print()
    print(p.trace("rraaa"))
