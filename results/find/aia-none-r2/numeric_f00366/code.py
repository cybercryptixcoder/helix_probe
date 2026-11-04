
def f(x):
    if x == 0:
        return 1548.92
    if x < -4.1:
        return 8.8
    if x < 0:              # -4.1 <= x < 0
        return 9.8
    if x <= 4.1:           # 0 < x <= 4.1
        return -11.4
    return -12.4           # x > 4.1
