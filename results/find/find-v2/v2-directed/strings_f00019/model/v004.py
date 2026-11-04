def predict(probe):
    # Rule: increment the last character if it's a letter [E1,E2,E4,E5,E7,E11]
    #   - 'z' wraps to 'a', 'Z' wraps to 'A' [E2,E5,E7]
    #   - non-ASCII letters get +1 code point [E4]
    #   - non-letters (digits, punctuation, spaces) leave string unchanged [E1,E2,E3,E6,E8,E9,E10]
    #   - only the last character is modified [all]
    outputs = []
    for s in probe["inputs"]:
        if not s:
            outputs.append(s)
            continue
        last = s[-1]
        if last == 'z':
            outputs.append(s[:-1] + 'a')
        elif last == 'Z':
            outputs.append(s[:-1] + 'A')
        elif last.isalpha():
            outputs.append(s[:-1] + chr(ord(last) + 1))
        else:
            outputs.append(s)
    return {"outputs": outputs}
