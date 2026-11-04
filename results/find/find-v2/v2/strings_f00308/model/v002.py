import re

def predict(probe):
    # Removes all whitespace (spaces, tabs, newlines, CR, etc.) [E1, E2]
    #   E1: "Hello World function lazy" -> "HelloWorldfunctionlazy"
    #   E2: "a\tb" -> "ab", "a\nb" -> "ab", "a\r\nb" -> "ab", "a\t b" -> "ab"
    # Leading/trailing/multiple whitespace all removed [E2: " a"->"a", "a "->"a", " ab cd "->"abcd"]
    # Other chars (digits, letters, case) unchanged [E1]
    return {"outputs": [re.sub(r"\s+", "", x) for x in probe["inputs"]]}
