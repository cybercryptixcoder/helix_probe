def predict(probe):
    # Removes all whitespace characters (spaces, tabs, newlines) [E1, E2]
    # " Zebralower" -> "Zebralower" (leading space removed) [E1]
    # "Hello World function lazy" -> "HelloWorldfunctionlazy" [E1]
    # "a\tb" -> "ab", "a\nb" -> "ab" (tabs and newlines also removed) [E2]
    # "a  b" -> "ab" (multiple spaces all removed) [E2]
    import re
    return {"outputs": [re.sub(r"\s+", "", s) for s in probe["inputs"]]}
