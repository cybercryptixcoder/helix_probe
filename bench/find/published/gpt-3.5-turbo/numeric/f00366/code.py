
def f(x):
    if x < 0:
        return 8.8
    elif x > 0:
        if x % 132 < 66:
            return 1548.92
        else:
            return -12.4
    else:
        return None  # handle x = 0 case if needed

# Example usage:
print(f(-128))  # Output: 8.8
print(f(64))   # Output: -12.4
print(f(0))    # Output: None (handle this case accordingly in your code)
