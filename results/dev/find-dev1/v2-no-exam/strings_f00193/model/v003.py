import unicodedata

def predict(probe):
    results = []
    for s in probe["inputs"]:
        combined = s + "JTQL"
        if combined:
            first = combined[0]
            cat = unicodedata.category(first)
            if cat.startswith('L'):
                o = ord(first)
                if 'a' <= first <= 'z':
                    shifted = chr((o - 2 - ord('a')) % 26 + ord('a'))
                elif 'A' <= first <= 'Z':
                    shifted = chr((o - 2 - ord('A')) % 26 + ord('A'))
                else:
                    shifted = chr(o - 2) if o >= 2 else first
                combined = shifted + combined[1:]
        results.append(combined)
    return {"outputs": results}
