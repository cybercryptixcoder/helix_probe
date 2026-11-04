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
            # Treat ß (U+00DF) as part of the lowercase run ending at ÿ (U+00FF),
            # bridging the × (U+00D7) multiplication sign gap.
            if ch.islower():
                pred = str.islower
            else:
                pred = str.isupper

            def in_run(c):
                if pred(c):
                    return True
                # ß is lowercase but islower() is True; × is not a letter.
                # Bridge: allow ß..ÿ range for lowercase run.
                if pred is str.islower and '\u00df' <= c <= '\u00ff':
                    return True
                return False

            start = ord(ch)
            while start > 0 and in_run(chr(start - 1)):
                start -= 1
            end = ord(ch)
            while in_run(chr(end + 1)):
                end += 1
            # Build the run as a list of valid characters (skip × gap)
            run = [c for c in (chr(k) for k in range(start, end + 1)) if in_run(c)]
            idx = run.index(ch)
            first = run[(idx - 2) % len(run)]
        else:
            first = ch
        return first + s[1:]
    try:
        return {"outputs": [shift_first(x) for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
