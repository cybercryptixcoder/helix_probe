
import re

def f(x):
    # Remove all whitespace characters
    s = re.sub(r'\s+', '', x)
    # Apply str.capitalize() semantics
    return s.capitalize()
