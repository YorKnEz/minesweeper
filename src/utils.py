def clamp(x, a, b):
    """
    Clamp value x in interval [a, b].

    It is assumed a <= b.
    """
    return max(a, min(b, x))
