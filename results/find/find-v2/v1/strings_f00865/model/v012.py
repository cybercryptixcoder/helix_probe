def predict(probe):
    def shift_first(s):
        if not s:
            return s
        ch = s[0]
        if 'a' <= ch <= 'z':
            first = chr((ord(ch) - ord('a') - 2) % 26 + ord('a'))
        elif 'A' <= ch <= 'Z':
            first = chr((ord(ch) - ord('A') - 2) % 26 + ord('A'))
        elif ch.isalpha():
            # Non-ASCII letter: shift backward by 2 code points.
            # Plain code-point arithmetic matches all observations
            # (é->ç, ü->ú, ñ->ï, ø->ö, æ->ä, œ->ő, ß->Ý, à->Þ, þ->ü, ÿ->ý).
            first = chr(ord(ch) - 2)
        else:
            first = ch
        return first + s[1:]
    try:
        return {"outputs": [shift_first(x) for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
