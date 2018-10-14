def next_remaining_principal(current, c, B):
    remaining = current * (1 + c) - B
    return remaining


def remaining_principal(M0, c, n, k):
    return M0 * ((1 + c)**n - (1 + c)**k) / ((1 + c)**n - 1)


def payment(M0, c, n):
    B = (c * (1 + c)**n * M0) / ((1 + c)**n - 1)
    return B
