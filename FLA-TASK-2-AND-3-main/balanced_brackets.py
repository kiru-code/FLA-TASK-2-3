"""Task 3, Case Study 1 - Balanced brackets checker.

CFG  G1:  S -> ( S ) S | [ S ] S | eps
PDA  P1:  Q = {q0, q1}, Gamma = {(, [, Z0}, F = {q0}   (deterministic)
Stack letter "Z" stands for Z0.  q0 = nothing open, q1 = some bracket open.
"""
from automata import PDA, EPS, report

PAIRS = {")": "(", "]": "["}


def build():
    d = {}
    for o in "([":
        d[("q0", o, "Z")] = {("q1", o + "Z")}            # open (first)
        for x in "([":
            d[("q1", o, x)] = {("q1", o + x)}            # open (more)
    d[("q1", ")", "(")] = {("q1", EPS)}                  # close )
    d[("q1", "]", "[")] = {("q1", EPS)}                  # close ]
    d[("q1", EPS, "Z")] = {("q0", "Z")}                  # back to start
    return PDA("P1 (balanced brackets)", "q0", {"q0"}, d)


# Context-free grammar G1, used for a leftmost derivation demo -------------
GRAMMAR = {"S": ["(S)S", "[S]S", ""]}


def derivation_of_nested():
    """Leftmost derivation of ([]) exactly as in the report."""
    steps = ["S", "(S)S", "([S]S)S", "([]S)S", "([])S", "([])"]
    return " => ".join(steps)


ACCEPTED = ["()", "[()]", "()[]", "([])()", "[[()]]"]
REJECTED = ["(", ")(", "(]", "([)]", "())", "[[]"]

if __name__ == "__main__":
    p = build()
    report(p, ACCEPTED, REJECTED)
    print("\nLeftmost derivation:", derivation_of_nested())
    print()
    print(p.trace("[()]"))
    print()
    print(p.trace("([)]"))
