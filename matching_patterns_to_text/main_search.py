from matching_patterns_to_text.naive import naive_search
from matching_patterns_to_text.finite_automata import transition_table, finite_automata_search


def find_patterns(pattern, file_path):
    with open(file_path) as file:
        # text = file.read()
        text = "art"

        pattern_indices = naive_search(pattern, text)
        print(pattern_indices)
        print(len(pattern_indices))
        print()

        pattern_indices = finite_automata_search(text, transition_table(pattern))
        print(pattern_indices)
        print(len(pattern_indices))


find_patterns("art", "act_1997_714.txt")
