def predict(probe):
    # The last character is incremented by one in ASCII/ordinal terms [E1-E4].
    # Letters: 'a'->'b', ..., 'y'->'z', 'z'->'a' (wrap), 'Z'->'A' (wrap) [E4].
    # Digits: '3'->'4'? No — "abc123" unchanged [E1]. So digits NOT incremented.
    #   Wait: E1 "abc123"->"abc123" unchanged. But E2 "abc123 def"->"abc123 deg":
    #   last char 'f'->'g', so the digit part is untouched; only final char matters.
    # Non-letter final char (digit, space, punctuation) -> unchanged [E1,E2,E3].
    # Wrap: 'z'->'a' [E4 fizz->fiza, quiz->quia, buzz->buza, az->aa, jazz->jaza]
    #       'Z'->'A' [E4 ZZ->ZA, AZ->AA]
    # Case preserved: 'Zz'->'Za' (last 'z'->'a', case of last char kept) [E4]
    # Only the final character of the whole string is changed [E2].
    def f(s):
        if not s:
            return s
        c = s[-1]
        if 'a' <= c <= 'z':
            return s[:-1] + ('a' if c == 'z' else chr(ord(c) + 1))
        if 'A' <= c <= 'Z':
            return s[:-1] + ('A' if c == 'Z' else chr(ord(c) + 1))
        return s
    return {"outputs": [f(x) for x in probe["inputs"]]}
