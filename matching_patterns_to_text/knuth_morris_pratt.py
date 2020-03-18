def prefix_function(pattern):
    pi = []
    pi.append(-1)
    k = -1
    for q in range(1, len(pattern)):
        while k >= 0 and pattern[k+1] != pattern[q]:
            k = pi[k]

        if pattern[k+1] == pattern[q]:
            k += 1

        pi.append(k)

    return pi


def kmp_matching(text, pattern, pi):
    pattern_shifts = []

    q = -1
    for i in range(len(text)):
        while q >= 0 and pattern[q+1] != text[i]:
            q = pi[q]

        if pattern[q+1] == text[i]:
            q += 1

        if q == len(pattern) - 1:
            pattern_shifts.append(i-q)
            q = pi[q]

    return pattern_shifts
