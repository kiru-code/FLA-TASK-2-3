"""Task 2, Application 1 - Vending machine coin acceptor (M_COIN).

A snack costs Rs. 20.  Coins: 5 and 10; anything else is the symbol O.
Language: coins that add up to exactly 20.
States: s0, s5, s10, s15, s20 (accepting), sd (dead).
Input is a string of coins separated by spaces, e.g. "5 10 5".
"""
from automata import DFA, report

PRICE = 20
COINS = {"5": 5, "10": 10}


def classify(w):
    """Classifier h: each space-separated token becomes 5, 10 or O."""
    return [t if t in COINS else "O" for t in w.split()]


def build():
    delta = {}
    for n in range(0, PRICE + 1, 5):
        for coin, value in COINS.items():
            delta[(f"s{n}", coin)] = f"s{n + value}" if n + value <= PRICE else "sd"
    # every move on O, and every move from s20 / sd, goes to the dead state
    # (handled by the DFA's default dead state, as in Table 2 of the report).
    return DFA("M_COIN (vending machine)", "s0", {f"s{PRICE}"}, delta,
               classify=classify, dead="sd")


ACCEPTED = ["5 5 5 5", "5 5 10", "5 10 5", "10 5 5", "10 10"]
REJECTED = ["5 10", "10 10 5", "5 5 10 10", "5 10 10", "10 O", ""]

if __name__ == "__main__":
    m = build()
    report(m, ACCEPTED, REJECTED)
    print("\nTraces (Table 4):")
    print(m.trace("5 10 5"))
    print(m.trace("10 5 10"))
