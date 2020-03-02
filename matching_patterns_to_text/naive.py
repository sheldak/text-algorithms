def naive_matching(pattern, text):
    pattern_shifts = []
    pat_len = len(pattern)
    for s in range(len(text) - pat_len + 1):
        if pattern == text[s:(s+pat_len)]:
            pattern_shifts.append(s)

    return pattern_shifts
