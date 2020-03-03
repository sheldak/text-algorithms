from time import time

from matching_patterns_to_text.naive import naive_matching
from matching_patterns_to_text.finite_automata import finite_automata_matching
from matching_patterns_to_text.knuth_morris_pratt import kmp_matching


def algorithm_result(text, pattern, algorithm):
    start_time = time()
    pattern_indices = algorithm(text, pattern)
    print(pattern_indices)
    print(len(pattern_indices), "\n")
    print(time() - start_time, "\n")


def find_patterns(pattern, file_path):
    with open(file_path) as file:
        text = file.read()
        # text = "art"

        algorithm_result(text, pattern, naive_matching)
        algorithm_result(text, pattern, finite_automata_matching)
        algorithm_result(text, pattern, kmp_matching)


find_patterns("art", "act_1997_714.txt")
