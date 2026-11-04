def predict(probe):
    # Observations [E1]:
    # - Spaces are removed from input.
    # - A 'Z' is inserted somewhere.
    # Let's analyze positions of Z in outputs:
    #   "apple" -> "apZple"          (Z after 2 chars of "apple")
    #   "test case " -> "testZcase"  (Z after 4 chars of "testcase")
    #   "test caseMiXeD" -> "testcaZseMiXeD" (Z after 6 chars of "testcaseMiXeD")
    #   "data a Python " -> "dataaZPython" (Z after 5 chars of "dataaPython")
    #   "test case Zebra" -> "testcaZseZebra" (Z after 6 chars of "testcaseZebra")
    #   "Mississippi Hello World data" -> "MississippiHZelloWorlddata" (Z after 12 chars)
    #
    # Hmm, positions don't match a simple fixed index. Let's look at lengths:
    #   apple (5) -> Z at index 2
    #   testcase (8) -> Z at index 4
    #   testcaseMiXeD (13) -> Z at index 6
    #   dataaPython (11) -> Z at index 5
    #   testcaseZebra (13) -> Z at index 6
    #   MississippiHelloWorlddata (25) -> Z at index 12
    # Looks like Z is inserted at floor(len/2) of the space-removed string!
    #   apple: 5//2=2 ✓
    #   testcase: 8//2=4 ✓
    #   testcaseMiXeD: 13//2=6 ✓
    #   dataaPython: 11//2=5 ✓
    #   testcaseZebra: 13//2=6 ✓
    #   MississippiHelloWorlddata: 25//2=12 ✓
    # So: remove spaces, insert 'Z' at index len//2.
    out = []
    for s in probe["inputs"]:
        t = s.replace(" ", "")
        mid = len(t) // 2
        out.append(t[:mid] + "Z" + t[mid:])
    return {"outputs": out}
