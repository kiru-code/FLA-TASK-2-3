"""Task 3, Case Study 3 - Nested if-else statement checker.

Symbols: i = "if (condition)", e = "else", a = an action statement.
CFG  G3:  S -> i S | i S e S | a          (ambiguous: dangling else)
PDA  P3:  built from the grammar, Q = {q0, q1, q2}, F = {q2}
          Gamma = {S, i, e, a, Z0}; NONdeterministic (3 ways to expand S).
"Z" stands for Z0.
"""
from automata import PDA, EPS, report


def build():
    d = {
        ("q0", EPS, "Z"): {("q1", "SZ")},                       # start: push S
        ("q1", EPS, "S"): {("q1", "iS"), ("q1", "iSeS"), ("q1", "a")},  # expand S
        ("q1", EPS, "Z"): {("q2", "Z")},                        # accept
    }
    for t in "iea":                                             # match terminals
        d[("q1", t, t)] = {("q1", EPS)}
    return PDA("P3 (nested if-else)", "q0", {"q2"}, d)


# Unambiguous "nearest-if" grammar from the report:
#   S -> M | U,  M -> i M e M | a,  U -> i S | i M e U
def language_up_to(n):
    """All strings of L(G3) of length <= n (used by the test-suite)."""
    gen = {1: {"a"}}
    for k in range(2, n + 1):
        cur = {"i" + s for s in gen[k - 1]}                     # S -> i S
        for l1 in range(1, k - 2):                              # S -> i S e S
            for s1 in gen.get(l1, ()):
                for s2 in gen.get(k - 2 - l1, ()):
                    cur.add("i" + s1 + "e" + s2)
        gen[k] = cur
    return set().union(*gen.values())


ACCEPTED = ["a", "ia", "iaea", "iiaea", "iiaeaea"]
REJECTED = ["", "i", "aea", "iea", "iaeaea", "aa"]

if __name__ == "__main__":
    p = build()
    report(p, ACCEPTED, REJECTED)
    print("\nLeftmost derivation of iaea: S => iSeS => iaeS => iaea")
    print()
    print(p.trace("iaea"))
    print()
    print(p.trace("iea"))
    print("\nAmbiguity (dangling else): number of different accepting")
    print("computations of 'iiaea' =", p.count_accepting("iiaea"),
          "(two parse trees); of 'iaea' =", p.count_accepting("iaea"))
