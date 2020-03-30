import random
import math
import string
from time import time

from suffix_trees.suffix_trie_links import make_suffix_trie
from suffix_trees.simple_mccreight import simple_mccreight
from suffix_trees.mccreight import mccreight


def test(word, struct):
    # printing name of algorithm
    if struct == "trie":
        print("Using trie")
        algorithm = make_suffix_trie
    elif struct == "simple McCreight":
        print("Using simple McCreight algorithm")
        algorithm = simple_mccreight
    elif struct == "McCreight":
        print("Using McCreight algorithm")
        algorithm = mccreight
    else:
        raise NameError("Invalid algorithm")

    # opening file if we have got the act
    text_name = word
    if word[-4:] == ".txt":
        with open(word) as file:
            print("text in file: " + word)
            word = file.read()
            # word = word[:2000]
            word += "$"  # marker at the end of the text
            print(len(word))
    else:
        print("word: " + word + "\n")

    # running algorithm
    start_time = time()
    tree = algorithm(word)
    time_of_running = time() - start_time

    # test: 1000 random words which must be in the tree
    for _ in range(1000):
        start = random.randint(0, len(word)-1)
        end = random.randint(start, len(word))
        test_word = word[start:end]
        if not tree.find(test_word):
            print(struct + " for word " + word + " is incorrect")
            return False

    # test: 1000 completely random words, it is possible that some of them will be in the tree
    # words which are in the tree will be printed
    found_words = set()
    for _ in range(1000):
        length = random.randint(1, math.ceil(min(math.sqrt(len(word)) + 2, 12)))
        test_word = ""
        for _ in range(length):
            test_word += random.choice(string.ascii_letters)
        if tree.find(test_word):
            found_words.add(test_word)

    # in such place we know that algorithm is correct for this set of tests
    print("random words found in tree:", found_words)
    if text_name[-4:] == ".txt":
        print(struct + " for text \"" + text_name + "\" is correct")
    else:
        print(struct + " for word \"" + word + "\" is correct")

    print("time of running:", time_of_running, "\n\n")
    return True


def compare_algorithms(word):
    test(word, "trie")
    test(word, "simple McCreight")
    test(word, "McCreight")


def main_func(words):
    for word in words:
        compare_algorithms(word)


words_to_check = ["bbb$", "aabbabd", "ababcd", "abcbccd", "short_act_1997_714.txt"]
main_func(words_to_check)

