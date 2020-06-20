from regular_expressions.automaton import Automaton


def check_matching(regex, texts):
    """ Making automaton from regex and checking passed texts. """
    nfa = Automaton(is_dfa=False, regex=regex)
    dfa = nfa.to_dfa()

    print("Regular expression: " + str(regex))
    for text in texts:
        matching = dfa.match(text)

        if matching:
            print(f"Text \"{text}\" accepted")
        else:
            print(f"Text \"{text}\" rejected")

    print()


if __name__ == "__main__":
    regex = "ab(a(ba)?(a)*)+b"
    check_matching(regex, ["abab", "aabab", "ababaaaaaaaabab", "ababaaaaaaaaba"])

    regex = "(ab)+.a"
    check_matching(regex, ["abba", "ab0a", "aaaa", "ababababba"])

    regex = "a\\s\\d(10\\d)+"
    check_matching(regex, ["a 6108", "aa6100", "a 4108109100"])

    regex = "[aB]cd"
    check_matching(regex, ["acd", "aBcd", "Bcd"])

    regex = "[abc]+cd?"
    check_matching(regex, ["abbccac", "abbccacdd"])

    regex = "(\\d[bc].)+"
    check_matching(regex, ["3bp", " dc0", "1bc2bb3cc4c4"])
