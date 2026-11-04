
def f(x: str) -> str:
    n = len(x)
    mid = n // 2
    return x[:mid] + "Z" + x[mid:]
