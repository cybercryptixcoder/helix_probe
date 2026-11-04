def predict(probe):
    # Capitalize first letter of each word, lowercase the rest [E1]
    # "apple" -> "Apple"; "test case " -> "Test case"
    # "test caseMiXeD" -> "Test casemixed"; "data a Python " -> "Data a python"
    # "test case Zebra" -> "Test case zebra"; "Mississippi Hello World data" -> "Mississippi hello world data"
    # Trailing spaces are stripped; internal spaces preserved.
    return {"outputs": [" ".join(w[:1].upper() + w[1:].lower() for w in s.split(" ")) for s in probe["inputs"]]}
