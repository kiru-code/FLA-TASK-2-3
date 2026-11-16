"""Task 2, Application 3 - Vehicle registration number check (M_PLATE).

Simplified format (teaching format, not the official rule):
    2 capital letters, 2 digits, 1 or 2 capital letters, 4 digits
Classifier h:  A-Z -> L,  0-9 -> D,  everything else -> O.
Language: h(w) in  L L D D L (L + eps) D D D D
States q0..q10 (q10 accepting) and the dead state qd (Tables 9 and 10).
"""
from automata import DFA, report

LETTERS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
DIGITS = set("0123456789")


def classify(w):
    return ["L" if c in LETTERS else "D" if c in DIGITS else "O" for c in w]


def build():
    delta = {
        ("q0", "L"): "q1",
        ("q1", "L"): "q2",
        ("q2", "D"): "q3",
        ("q3", "D"): "q4",
        ("q4", "L"): "q5",
        ("q5", "L"): "q6",   # second series letter
        ("q5", "D"): "q7",   # only one series letter: straight to digits
        ("q6", "D"): "q7",
        ("q7", "D"): "q8",
        ("q8", "D"): "q9",
        ("q9", "D"): "q10",
    }
    return DFA("M_PLATE (registration number)", "q0", {"q10"}, delta,
               classify=classify, dead="qd")


ACCEPTED = ["TN45AB1234", "KA05M2345", "MH12XY9876", "DL01C4455", "AP39ZZ0001"]
REJECTED = ["TN45AB123", "TN45AB12345", "T45AB1234", "TN4AB1234",
            "TN45ABC1234", "tn45ab1234", "TN 45 AB 1234"]

if __name__ == "__main__":
    m = build()
    report(m, ACCEPTED, REJECTED)
    print("\nTraces (Table 12):")
    for w in ("KA05M2345", "TN45ABC1234"):
        print(m.trace(w))
        print("   h(w) =", "".join(classify(w)))
