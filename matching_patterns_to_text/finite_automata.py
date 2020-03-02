def transition_table(pattern):
    alphabet = []
    for i in pattern:
        if i not in alphabet:
            alphabet.append(i)

    delta = []
    for q in range(len(pattern)+1):
        delta.append({})

        for letter in alphabet:
            k = min(len(pattern), q + 1)

            while k > 0 and pattern[:k] != (pattern[:q] + letter)[q - k + 1:]:
                k -= 1
            delta[q][letter] = k

    return delta


def finite_automata_matching(text, delta):
    pattern_shifts = []
    q = 0
    for s in range(0, len(text)):
        if text[s] in delta[q]:
            q = delta[q][text[s]]
            if q == len(delta) - 1:
                pattern_shifts.append(s + 1 - q)
                q = 0
        else:
            q = 0

    return pattern_shifts

