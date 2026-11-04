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
            # Non-ASCII letter: shift backward by 2 within its case block
            if ch.islower():
                base = ord(ch) & ~0x1F  # not reliable; use explicit block scan
                # Find the contiguous lowercase block containing ch
                start = ord(ch)
                while start > 0 and chr(start - 1).islower() and (ord(chr(start - 1)) == start - 1):
                    start -= 1
                end = ord(ch)
                while chr(end + 1).islower() and (ord(chr(end + 1)) == end + 1):
                    end += 1
                size = end - start + 1
                first = chr((ord(ch) - start - 2) % size + start)
            else:
                start = ord(ch)
                while start > 0 and chr(start - 1).isupper() and (ord(chr(start - 1)) == start - 1):
                    start -= 1
                end = ord(ch)
                while chr(end + 1).isupper() and (ord(chr(end + 1)) == end + 1):
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
