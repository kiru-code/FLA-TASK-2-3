# FLA CLA-2 – Tasks 2 and 3: DFA, CFG and PDA models

Course: **21CSC301T – Formal Language and Automata**, SRM Institute of Science and Technology, Tiruchirappalli
Author: Sri Harihara Sudhan VB (RA2411026050231) · Guide: Dr. C. Gunasundari

Python implementations of every automaton in the report
*"DFA, CFG and PDA Models for Practical Input Checking and Structure Recognition"*.
Each program follows the report exactly (same states, transitions, test strings and traces).

## Task 2 – DFAs (`task2_dfa/`)

| File | Report section | Machine | Language |
|---|---|---|---|
| `coin_acceptor.py` | 3.2 | M_COIN | coins of Rs. 5 / 10 adding to exactly Rs. 20 |
| `mod3_checker.py` | 3.3 | M_MOD3 | binary numbers divisible by 3 |
| `registration_check.py` | 3.4 | M_PLATE | `LLDD L(L) DDDD` vehicle number format |

## Task 3 – CFG + PDA (`task3_pda/`)

| File | Report section | Grammar | PDA |
|---|---|---|---|
| `balanced_brackets.py` | 4.2 | `S → (S)S \| [S]S \| ε` | P1, deterministic |
| `request_ack_log.py` | 4.3 | `S → rSaa \| raa` (`rⁿa²ⁿ`) | P2, deterministic |
| `if_else.py` | 4.4 | `S → iS \| iSeS \| a` | P3, nondeterministic, grammar is ambiguous |

`automata.py` holds the generic `DFA` and `PDA` simulators. The PDA simulator is a
breadth-first search over instantaneous descriptions (state, unread input, stack),
so it handles nondeterminism and can count accepting computations (ambiguity of `iiaea`).

## Run

Requires only Python 3.8+ (no external packages).

```bash
python run_all.py                           # all tables and traces
python -m task2_dfa.coin_acceptor           # one machine
python -m task3_pda.if_else
python -m unittest discover -s tests -t . -v   # 23 tests
```

The tests check every accepted/rejected string from the report tables, the stack traces
(Tables 16, 17, 20, 21), and compare each machine with an independent reference
(regex, arithmetic, grammar enumeration) on all short strings.

## Layout

```
automata.py        generic DFA / PDA simulators
task2_dfa/         three DFA validators
task3_pda/         three PDAs
tests/             unittest suite
run_all.py         runs every demo
```
