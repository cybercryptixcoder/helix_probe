def predict(probe):
    # Leading whitespace stripped before any check [E4: "   Hello"->"ello", "\tHello"->"ello", " Hello"->"ello"]
    # "Hello" is replaced by "ello" wherever it occurs, not just at start [E1: "Hello World function lazy"->"ello World function lazy"; E5: "function Hello World"->"function ello World"; E4: "HelloHello"->"elloello"]
    # Trailing whitespace stripped [E3: "banana data banana "->"banana data banana", E5: "Example "->"Example"]
    # Other uppercase starts unchanged [E2: "Zebra"->"Zebra", "Apple"->"Apple"]
    out = []
    for s in probe["inputs"]:
        s = s.lstrip()
        s = s.replace("Hello", "ello")
        s = s.rstrip()
        out.append(s)
    return {"outputs": out}
