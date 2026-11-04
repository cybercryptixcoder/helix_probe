import re

def predict(probe):
    # Remove all whitespace characters (spaces, tabs, newlines, etc.) [E5: "a\tb"->"aZb", "a\nb"->"aZb", "a\tb\tc"->"aZbc", "x\ty z"->"xZyz"]
    # Insert "Z" at the middle position of the whitespace-stripped string [E1-E5]
    # Middle = len//2 (integer division), insert before that index [E1: "hello"(5)->heZllo, "test123"(7)->tesZt123, "A1!"(3)->AZ1!]
    out = []
    for s in probe["inputs"]:
        t = re.sub(r"\s", "", s)
        mid = len(t) // 2
        out.append(t[:mid] + "Z" + t[mid:])
    return {"outputs": out}
