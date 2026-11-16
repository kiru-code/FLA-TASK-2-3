"""Run every demo (Task 2 and Task 3) and print the test tables and traces."""
import runpy

MODULES = [
    "task2_dfa.coin_acceptor",
    "task2_dfa.mod3_checker",
    "task2_dfa.registration_check",
    "task3_pda.balanced_brackets",
    "task3_pda.request_ack_log",
    "task3_pda.if_else",
]

for name in MODULES:
    print("\n" + "#" * 70 + f"\n# {name}\n" + "#" * 70)
    runpy.run_module(name, run_name="__main__")
