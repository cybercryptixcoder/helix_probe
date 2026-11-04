def predict(probe):
    # Rule: insert '5' at index ceil(len/2) = (len+1)//2 [E1-E11]
    # Rule: duplicate the final character [E1-E11]
    # Exception: single-character input "a" -> "a5a" (no duplication) [E11]
    #   For len==1, inserting '5' at index 1 gives "a5"; observed "a5a" means
    #   the '5' is inserted at index 1 and then... "a5a" = "a"+"5"+"a". So for
    #   len 1, midpoint (len+1)//2 = 1 -> "a"+"5"+"" = "a5", then duplicate last
    #   would give "a55". Observed "a5a": the char after insertion point is 'a'.
    #   So the rule is: insert '5' at index (len+1)//2, then duplicate the last
    #   character of the ORIGINAL string appended? No — check others.
    #   Simplest consistent rule: t = s[:mid] + "5" + s[mid:], then append s[-1]
    #   only if len(s) > 1. For "a": "a5" + nothing = "a5"? But observed "a5a".
    #   Actually "a5a" = insert '5' at index 1 into "a" gives "a5", then append
    #   the char at mid-1? For len 1, mid=1, s[mid-1]='a' -> "a5"+"a"="a5a". ✓
    #   For len>1, appending s[-1] matches all evidence. For len 1, s[-1]==s[mid-1].
    #   So: append s[-1] always, but for len 1 that gives "a55". Contradiction.
    #   Resolve: for len 1, output "a5a" — treat as insert '5' at index 1 then
    #   append original char. General rule: t = s[:mid]+"5"+s[mid:]; append s[-1]
    #   if len>1 else append s[0]. Since s[-1]==s[0] for len 1, that's "a5a". ✓
    def transform(s):
        if not s:
            return s
        mid = (len(s) + 1) // 2
        t = s[:mid] + "5" + s[mid:]
        if len(s) == 1:
            return t + s
        return t + t[-1]

    try:
        return {"outputs": [transform(x) for x in probe["inputs"]]}
    except Exception:
        return {"outputs": []}
