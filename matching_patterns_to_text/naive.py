def naive_search(pattern, text):
    pattern_indices = []
    pat_len = len(pattern)
    for i in range(len(text) - pat_len + 1):
        if pattern == text[i:(i+pat_len)]:
            pattern_indices.append(i)

    return pattern_indices
