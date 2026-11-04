def predict(probe):
    # Observations from E1:
    # - "apple" -> "akkle": 'p'->'k' (both p's), other chars unchanged
    # - "test case " -> unchanged (no 'p')
    # - "test caseMiXeD" -> unchanged (no 'p')
    # - "data a Python " -> unchanged (no 'p'... wait, "Python" has no lowercase p? 'P' is uppercase)
    # - "test case Zebra" -> unchanged (no 'p')
    # - "Mississippi Hello World data" -> "Mississikki Hello World data": 'pp'->'kk'
    # Rule hypothesis: replace lowercase 'p' with 'k'. Uppercase 'P' unchanged.
    return {"outputs": [s.replace("p", "k") for s in probe["inputs"]]}
