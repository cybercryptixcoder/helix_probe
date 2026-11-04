def predict(probe):
    # Identity for most inputs [E1]
    # "HELLO" -> "HEO": uppercase-only word drops every other letter? [E2]
    #   H E L L O -> H E O : kept positions 0,1,4? or removed repeated L's?
    #   "Hello" unchanged (mixed case), "hello" unchanged (lowercase)
    # Hypothesis: if the string is all uppercase letters, remove consecutive duplicates
    #   H E L L O -> H E L O ... but observed HEO, so also drop one more?
    # Alternative: all-uppercase -> keep letters at even indices: H(0) L(2) O(4) = HLO, no.
    #   keep indices 0,1,4 = H,E,O. Odd.
    # Simplest fit: all-uppercase word -> remove duplicate letters (LL->L) then... HEO?
    #   H E L L O dedupe consecutive = H E L O (4 chars), not HEO.
    # Try: all-uppercase -> keep first, second, last: H,E,O = HEO. Matches.
    # Uncertain; mark with ?. Only one data point.
    def f(s):
        if len(s) > 1 and s.isalpha() and s.isupper():
            return s[0] + s[1] + s[-1] if len(s) > 2 else s
        return s
    return {"outputs": [f(x) for x in probe["inputs"]]}
