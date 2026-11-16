"""Generic DFA and PDA simulators used by Task 2 and Task 3.

Notation follows the report (21CSC301T):
  DFA  M = (Q, Sigma, delta, q0, F)
  PDA  P = (Q, Sigma, Gamma, delta, q0, Z0, F), acceptance by final state.
Stacks are strings written TOP FIRST, e.g. "([Z" has "(" on top.
"Z" stands for the bottom-of-stack symbol Z0.
"""
from collections import deque

EPS = ""  # the empty string (epsilon)


# --------------------------------------------------------------------------
# DFA
# --------------------------------------------------------------------------
class DFA:
    def __init__(self, name, start, finals, delta, classify=None, dead="qd"):
        self.name = name
        self.start = start
        self.finals = set(finals)
        self.delta = delta          # {(state, symbol): state}
        self.classify = classify    # classifier h: input -> list of symbols
        self.dead = dead            # any move not in delta goes here

    def symbols(self, w):
        return self.classify(w) if self.classify else list(w)

    def run(self, w):
        """Return (final_state, path) where path lists every state visited."""
        state = self.start
        path = [state]
        for sym in self.symbols(w):
            state = self.delta.get((state, sym), self.dead)
            path.append(state)
        return state, path

    def accepts(self, w):
        return self.run(w)[0] in self.finals

    def trace(self, w):
        syms = self.symbols(w)
        final, path = self.run(w)
        verdict = "Accepted" if final in self.finals else "Rejected"
        return (f"{w!r:<18} symbols: {' '.join(syms) or 'eps':<24} "
                f"path: {' -> '.join(path)}  => {verdict}")


# --------------------------------------------------------------------------
# PDA (nondeterministic simulator, breadth-first search over IDs)
# --------------------------------------------------------------------------
class PDA:
    """delta maps (state, input_symbol_or_EPS, stack_top) -> set of
    (next_state, string_pushed_in_place_of_top).  An ID (instantaneous
    description) is (state, position_in_input, stack)."""

    def __init__(self, name, start, finals, delta, z0="Z"):
        self.name = name
        self.start = start
        self.finals = set(finals)
        self.delta = delta
        self.z0 = z0

    def _moves(self, cfg, w):
        state, pos, stack = cfg
        if not stack:
            return
        top, rest = stack[0], stack[1:]
        reads = [EPS] + ([w[pos]] if pos < len(w) else [])
        for read in reads:
            for nxt_state, push in self.delta.get((state, read, top), ()):
                yield (nxt_state, pos + (read != EPS), push + rest)

    def _is_accepting(self, cfg, w):
        return cfg[1] == len(w) and cfg[0] in self.finals

    def _limit(self, w, prune):
        # Stack cap keeps the search finite.  With prune=True we also drop
        # IDs whose stack (above Z0) is longer than the unread input; this is
        # valid for all PDAs in this project because every stack symbol above
        # Z0 must be matched by at least one more input symbol.
        cap = 2 * len(w) + 4
        def ok(cfg):
            if len(cfg[2]) > cap:
                return False
            if prune and len(cfg[2]) - 1 > len(w) - cfg[1]:
                return False
            return True
        return ok

    def run(self, w, prune=False):
        """Return (accepted, list_of_IDs).  If accepted, the list is an
        accepting computation; otherwise it is the computation that got
        furthest before getting stuck (useful for a rejected trace)."""
        ok = self._limit(w, prune)
        start = (self.start, 0, self.z0)
        parent = {start: None}
        order = [start]
        queue = deque([start])
        target = None
        while queue:
            cfg = queue.popleft()
            if self._is_accepting(cfg, w):
                target = cfg
                break
            for nxt in self._moves(cfg, w):
                if nxt not in parent and ok(nxt):
                    parent[nxt] = cfg
                    order.append(nxt)
                    queue.append(nxt)
        accepted = target is not None
        if not accepted:
            target = max(order, key=lambda c: (c[1], order.index(c)))
        path = []
        while target is not None:
            path.append(target)
            target = parent[target]
        path.reverse()
        return accepted, [(s, w[p:] or "eps", st) for s, p, st in path]

    def accepts(self, w, prune=False):
        return self.run(w, prune)[0]

    def count_accepting(self, w, prune=False):
        """Number of different accepting computations (shows ambiguity)."""
        ok = self._limit(w, prune)
        memo = {}
        def count(cfg):
            if cfg in memo:
                return memo[cfg]
            total = 1 if self._is_accepting(cfg, w) else 0
            for nxt in self._moves(cfg, w):
                if ok(nxt):
                    total += count(nxt)
            memo[cfg] = total
            return total
        return count((self.start, 0, self.z0))

    def trace(self, w, prune=False):
        accepted, ids = self.run(w, prune)
        lines = [f"{self.name} on {w!r}:"]
        lines.append(f"  {'step':<5}{'state':<7}{'input left':<14}stack (top first)")
        for i, (s, left, st) in enumerate(ids):
            lines.append(f"  {i:<5}{s:<7}{left:<14}{' '.join(st)}")
        lines.append("  => " + ("Accepted (input finished in a final state)"
                                  if accepted else "Rejected (stuck / not in a final state)"))
        return "\n".join(lines)


# --------------------------------------------------------------------------
# Small helper to print "Table: accepted / rejected" style output
# --------------------------------------------------------------------------
def report(machine, accepted, rejected, show=lambda m, w: m.accepts(w)):
    print(f"=== {machine.name} ===")
    for label, group, expected in (("ACCEPTED", accepted, True), ("REJECTED", rejected, False)):
        print(f"-- expected {label}")
        for w in group:
            got = show(machine, w)
            flag = "ok " if got == expected else "BUG"
            print(f"  [{flag}] {w!r:<18} -> {'Accepted' if got else 'Rejected'}")
