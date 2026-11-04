
def f(x):
    if x.isdigit():  # Check if the string contains only numeric characters
        return x[::-1]  # If it does, reverse it as is
    else:
        return x[::-1].swapcase()  # Otherwise, reverse and invert the case

# Testing the function with examples provided
print(f("apple"))  # elppZ
print(f("banana"))  # ananaR
print(f("123"))  # 321
