def predict(probe):
    # Remove all spaces from input [E1: "two words"->"twowZords", "a b c"->"aZbc", "  space  "->"spZace", "hello world"->"helloZworld"]
    # Insert "Z" at the middle position of the space-stripped string [E1: all outputs]
    # Middle = len//2 (integer division), insert before that index [E1: "hello"(5)->heZllo at idx2, "world"(5)->woZrld at idx2, "HELLO"(5)->HEZLLO at idx2, "test123"(7)->tesZt123 at idx3, "A1!"(3)->AZ1! at idx1, "space"(5)->spZace at idx2]
    out = []
    for s in probe["inputs"]:
        t = s.replace(" ", "")
        mid = len(t) // 2
        out.append(t[:mid] + "Z" + t[mid:])
    return {"outputs": out}
