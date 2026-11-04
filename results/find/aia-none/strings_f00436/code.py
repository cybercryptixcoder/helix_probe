
def f(x):
    # Keep only alphanumeric characters, lowercase them
    cleaned = ''.join(c.lower() for c in x if c.isalnum())
    # Check if cleaned string is a palindrome
    return cleaned == cleaned[::-1]
