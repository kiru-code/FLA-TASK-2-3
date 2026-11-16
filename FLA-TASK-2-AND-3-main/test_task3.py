import itertools
import re
import unittest

from task3_pda import balanced_brackets, request_ack_log, if_else


def reference_balanced(w):
    stack = []
    for c in w:
        if c in "([":
            stack.append(c)
        elif not stack or stack.pop() != {")": "(", "]": "["}[c]:
            return False
    return not stack


class TestBrackets(unittest.TestCase):
    p = balanced_brackets.build()

    def test_report_strings(self):
        for w in balanced_brackets.ACCEPTED:
            self.assertTrue(self.p.accepts(w), w)
        for w in balanced_brackets.REJECTED:
            self.assertFalse(self.p.accepts(w), w)

    def test_accepted_trace_matches_table16(self):
        ok, ids = self.p.run("[()]")
        self.assertTrue(ok)
        self.assertEqual([(s, st) for s, _, st in ids],
                         [("q0", "Z"), ("q1", "[Z"), ("q1", "([Z"),
                          ("q1", "[Z"), ("q1", "Z"), ("q0", "Z")])

    def test_rejected_trace_matches_table17(self):
        ok, ids = self.p.run("([)]")
        self.assertFalse(ok)
        self.assertEqual(ids[-1], ("q1", ")]", "[(Z"))

    def test_deterministic(self):
        for w in ["()", "([)]", "[()]()"]:
            self.assertLessEqual(self.p.count_accepting(w), 1)

    def test_all_strings_up_to_length_7(self):
        for n in range(0, 8):
            for t in itertools.product("()[]", repeat=n):
                w = "".join(t)
                self.assertEqual(self.p.accepts(w), reference_balanced(w), w)


class TestLog(unittest.TestCase):
    p = request_ack_log.build()

    def test_report_strings(self):
        for w in request_ack_log.ACCEPTED:
            self.assertTrue(self.p.accepts(w), w)
        for w in request_ack_log.REJECTED:
            self.assertFalse(self.p.accepts(w), w)

    def test_traces_match_tables_20_21(self):
        ok, ids = self.p.run("rraaaa")
        self.assertTrue(ok)
        self.assertEqual([st for _, _, st in ids],
                         ["Z", "XXZ", "XXXXZ", "XXXZ", "XXZ", "XZ", "Z", "Z"])
        ok, ids = self.p.run("rraaa")
        self.assertFalse(ok)
        self.assertEqual(ids[-1], ("q1", "eps", "XZ"))

    def test_all_strings_up_to_length_12(self):
        for n in range(0, 13):
            for t in itertools.product("ra", repeat=n):
                w = "".join(t)
                expected = bool(re.fullmatch(r"(r+)(a+)", w)) and \
                    w.count("a") == 2 * w.count("r") and "ar" not in w
                self.assertEqual(self.p.accepts(w), expected, w)

    def test_derivation_text(self):
        self.assertEqual(request_ack_log.derive(2), "S => rSaa => rraaaa")


class TestIfElse(unittest.TestCase):
    p = if_else.build()

    def test_report_strings(self):
        for w in if_else.ACCEPTED:
            self.assertTrue(self.p.accepts(w), w)
        for w in if_else.REJECTED:
            self.assertFalse(self.p.accepts(w), w)

    def test_dangling_else_is_ambiguous(self):
        self.assertEqual(self.p.count_accepting("iiaea"), 2)
        self.assertEqual(self.p.count_accepting("iaea"), 1)

    def test_agrees_with_grammar_up_to_length_7(self):
        lang = if_else.language_up_to(7)
        for n in range(0, 8):
            for t in itertools.product("iea", repeat=n):
                w = "".join(t)
                self.assertEqual(self.p.accepts(w, prune=True), w in lang, w)


if __name__ == "__main__":
    unittest.main()
