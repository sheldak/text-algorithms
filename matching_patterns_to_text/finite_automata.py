def transition_table(pattern):  # jeszcze dodac obsluge sytuacji gdy jakis prefix wzorca pojawia sie pozniej
    alphabet = []
    for i in pattern:
        if i not in alphabet:
            alphabet.append(i)

    delta = []
    for q in range(len(pattern)):
        delta.append({})
        delta[q][pattern[q]] = q+1

        for letter in alphabet:
            if letter != pattern[q]:
                delta[q][letter] = 0

    delta.append({})
    for letter in alphabet:
        delta[len(pattern)][letter] = 0

    print(delta)
    return delta


def finite_automata_search(text, delta):
    pattern_indices = []
    q = 0
    for s in range(0, len(text)):
        try:
            q = delta[q][text[s]]
            if q == len(delta):
                pattern_indices.append(s + 1 - q)
                q = 0
        except:
            q = 0

    return pattern_indices
