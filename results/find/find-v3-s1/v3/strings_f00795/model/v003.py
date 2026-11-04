def predict(probe):
    # Rule: insert "2" at index len(s)//2 [E1-E6 all]
    # Rule: last char, if letter, shift +2 within case (wrap) [E1-E6 all]
    # Rule: non-letter last char unchanged [E1 "test case ", E2 "hello1","7","a b", E3 "test case  ", E5 "racecar "]
    outputs = []
    for s in probe["inputs"]:
        mid = len(s) // 2
        result = s[:mid] + "2" + s[mid:]
        if result:
            last = result[-1]
            if 'a' <= last <= 'z':
                last = chr((ord(last) - ord('a') + 2) % 26 + ord('a'))
                result = result[:-1] + last
            elif 'A' <= last <= 'Z':
                last = chr((ord(last) - ord('A') + 2) % 26 + ord('A'))
                result = result[:-1] + last
        outputs.append(result)
    return {"outputs": outputs}
