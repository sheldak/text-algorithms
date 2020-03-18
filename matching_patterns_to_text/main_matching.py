from time import time

from matching_patterns_to_text.naive import naive_matching
from matching_patterns_to_text.finite_automata import finite_automata_matching, transition_table
from matching_patterns_to_text.knuth_morris_pratt import kmp_matching, prefix_function


def algorithm_result(text, pattern, algorithm, table=None):
    if table is None:
        start_time = time()
        pattern_indices = algorithm(text, pattern)
        res_time = time() - start_time
    else:
        start_time = time()
        pattern_indices = algorithm(text, pattern, table)
        res_time = time() - start_time
    print("number of indices:", len(pattern_indices), "  all indices: ", pattern_indices)
    print("time: ", res_time, "\n")


def compare_tables(pattern):
    print("for pattern: \"", pattern, "\"")

    start_time = time()
    _ = transition_table(pattern)
    print("transition table time: ", time() - start_time)

    start_time = time()
    _ = prefix_function(pattern)
    print("prefix function time:  ", time() - start_time)


def find_patterns_in_text(pattern, text, file=False):
    if not file:
        print("pattern: \"", pattern, "\" in text: \"", text, "\"\n")

    algorithm_result(text, pattern, naive_matching)

    delta = transition_table(pattern)
    algorithm_result(text, pattern, finite_automata_matching, delta)

    pi = prefix_function(pattern)
    algorithm_result(text, pattern, kmp_matching, pi)

    print()


def find_patterns_in_file(pattern, file_path):
    with open(file_path) as file:
        text = file.read()
        print("pattern: \"", pattern, "\" in file:", file_path, "\n")
        find_patterns_in_text(pattern, text, file=True)


find_patterns_in_file("ustawa", "act_1997_714.txt")
find_patterns_in_file("5", "act_1997_714.txt")
find_patterns_in_file("las", "act_1997_714.txt")

find_patterns_in_file("art", "act_1997_714.txt")
find_patterns_in_file("kruszwil", "wikipedia-tail-kruszwil.txt")

find_patterns_in_file("5"*10000, "act_1997_714.txt")

compare_tables("abcd")
