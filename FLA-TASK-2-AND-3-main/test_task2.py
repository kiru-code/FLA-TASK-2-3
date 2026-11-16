import itertools
import re
import unittest

from task2_dfa import coin_acceptor, mod3_checker, registration_check


class TestCoin(unittest.TestCase):
    m = coin_acceptor.build()

    def test_table3_inputs(self):
        for w in coin_acceptor.ACCEPTED:
            self.assertTrue(self.m.accepts(w), w)
        for w in coin_acceptor.REJECTED:
            self.assertFalse(self.m.accepts(w), w)

    def test_final_states(self):
        self.assertEqual(self.m.run("5 10")[0], "s15")
        self.assertEqual(self.m.run("10 10 5")[0], "sd")
        self.assertEqual(self.m.run("")[0], "s0")

    def test_trace_paths(self):
        self.assertEqual(self.m.run("5 10 5")[1], ["s0", "s5", "s15", "s20"])
        self.assertEqual(self.m.run("10 5 10")[1], ["s0", "s10", "s15", "sd"])

    def test_language_is_exactly_the_five_strings(self):
        ok = {"5 5 5 5", "5 5 10", "5 10 5", "10 5 5", "10 10"}
        for n in range(0, 6):
            for combo in itertools.product(["5", "10", "O"], repeat=n):
                w = " ".join(combo)
                self.assertEqual(self.m.accepts(w), w in ok, w)


class TestMod3(unittest.TestCase):
    m = mod3_checker.build()

    def test_table6_inputs(self):
        for w in mod3_checker.ACCEPTED:
            self.assertTrue(self.m.accepts(w), w)
        for w in mod3_checker.REJECTED:
            self.assertFalse(self.m.accepts(w), w)

    def test_final_states_match_remainder(self):
        for w in mod3_checker.ACCEPTED + mod3_checker.REJECTED:
            self.assertEqual(self.m.run(w)[0], f"q{int(w, 2) % 3}")

    def test_all_strings_up_to_length_10(self):
        for n in range(0, 11):
            for bits in itertools.product("01", repeat=n):
                w = "".join(bits)
                value = int(w, 2) if w else 0
                self.assertEqual(self.m.accepts(w), value % 3 == 0, w)

    def test_rejects_non_bits(self):
        with self.assertRaises(ValueError):
            self.m.accepts("10a")


class TestPlate(unittest.TestCase):
    m = registration_check.build()
    pattern = re.compile(r"^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$")

    def test_table11_inputs(self):
        for w in registration_check.ACCEPTED:
            self.assertTrue(self.m.accepts(w), w)
        for w in registration_check.REJECTED:
            self.assertFalse(self.m.accepts(w), w)

    def test_final_states(self):
        self.assertEqual(self.m.run("TN45AB123")[0], "q9")
        self.assertEqual(self.m.run("TN45AB12345")[0], "qd")
        self.assertEqual(self.m.run("")[0], "q0")

    def test_agrees_with_regular_expression(self):
        samples = ["TN45AB1234", "KA05M2345", "TN45ABC1234", "tn45ab1234", "T45AB1234",
                   "TN45A1234", "TN45AB 1234", "ZZ00Z0000", "ZZ00ZZ000", "AB12CD3456X"]
        for w in samples:
            self.assertEqual(self.m.accepts(w), bool(self.pattern.match(w)), w)


if __name__ == "__main__":
    unittest.main()
