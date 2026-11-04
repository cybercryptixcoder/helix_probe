def predict(probe):
    # Keep first occurrence of each character (case-sensitive), then append "h" [E1]
    # Evidence: "Hello World function lazy" -> "Helo Wrdfunctiazyh" (dedup across whole string) [E1]
    # Evidence: "bananaUPPER" -> "banUPERh" (case-sensitive dedup) [E1]
    # Evidence: "level" -> "levh", " Zebralower" -> " Zebralowh", "Zebra" -> "Zebrah" [E1]
    return {"outputs": ["".join(dict.fromkeys(s)) + "h" for s in probe["inputs"]]}
