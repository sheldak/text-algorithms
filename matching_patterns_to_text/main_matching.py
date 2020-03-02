from time import time

from matching_patterns_to_text.naive import naive_matching
from matching_patterns_to_text.finite_automata import transition_table, finite_automata_matching


def find_patterns(pattern, file_path):
    with open(file_path) as file:
        text = file.read()
        # text = "art"

        start_time = time()
        pattern_indices = naive_matching(pattern, text)
        print(pattern_indices)
        print(len(pattern_indices), "\n")
        print(time() - start_time, "\n")

        start_time = time()
        pattern_indices = finite_automata_matching(text, transition_table(pattern))
        print(pattern_indices)
        print(len(pattern_indices), "\n")
        print(time() - start_time, "\n")


find_patterns("art", "act_1997_714.txt")
