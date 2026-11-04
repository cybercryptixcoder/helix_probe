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
            # Non-ASCII letter: shift backward by 2 in code point order,
            # wrapping within the contiguous same-case letter run.
            if ch.islower():
                pred = str.islower
            else:
                pred = str.isupper
            start = ord(ch)
            while start > 0 and pred(chr(start - 1)):
                start -= 1
            end = ord(ch)
            while pred(chr(end + 1)):
                end += 1
            size = end - start + 1
            first = chr((ord(ch) - start - 2) % size + start)
        else:
            first = ch
        return first + s[1:]
    try:
        return {"outputs": [shift_first(x) for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
