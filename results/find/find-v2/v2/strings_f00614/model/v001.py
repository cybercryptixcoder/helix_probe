def predict(probe):
    # Removes all spaces from input [E1: "Hello World function lazy" -> "HelloWorldfunctionlazy"]
    # Appends "F" to the result [E1: all outputs end in F]
    # Case preserved [E1: "bananaUPPER" -> "bananaUPPERF", "Zebra" -> "ZebraF"]
    # Leading space removed along with other spaces [E1: " Zebralower" -> "ZebralowerF"]
    # Digits and symbols preserved [E1: "abc123" -> "abc123F"]
    out = []
    for s in probe.get("inputs", []):
        out.append(s.replace(" ", "") + "F")
    return {"outputs": out}
