def predict(probe):
    # Only "HELLO" (all-caps) changed: "HELLO" -> "HEO", dropping the two L's [E1]
    # All other inputs returned unchanged: lowercase, mixed case, phrases, digits, punctuation [E1]
    # Hypothesis: for all-uppercase strings, remove consecutive duplicate letters (collapse runs) [E1?]
    #   "HELLO" has "LL" -> "L", giving "HELO"? But observed "HEO" (both L's gone).
    # Alternative: remove all repeated letters entirely (keep only first occurrence of each letter) [E1?]
    #   "HELLO": H,E,L,L,O -> keep first H,E,L,O = "HELO", not "HEO". Doesn't fit.
    # Alternative: remove letters that appear more than once, entirely [E1?]
    #   "HELLO": L appears twice -> remove both L's -> "HEO". Fits!
    # Rule: if input is all uppercase, delete every character whose letter occurs more than once [E1?]
    #   Non-uppercase inputs pass through unchanged [E1]
    def transform(s):
        if s and s == s.upper() and any(c.isalpha() for c in s):
            from collections import Counter
            cnt = Counter(s)
            return ''.join(c for c in s if cnt[c] == 1)
        return s
    return {"outputs": [transform(x) for x in probe["inputs"]]}
