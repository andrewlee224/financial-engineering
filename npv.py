def discount(r, n):
    return 1 / (1 + r)**n


def npv(value, r, n):
    return value * discount(r, n)
