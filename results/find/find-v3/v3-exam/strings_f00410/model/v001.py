def predict(probe):
    # Reverses the string, but then swaps case? Let's check E1.
    # "abc123" -> "321cba" : reversed, digits unchanged
    # "level" -> "jevel" : reversed is "level", but output "jevel"?? 
    #   Wait "level" reversed = "level". Output "jevel". Hmm.
    #   Actually "level" -> "jevel": first char 'l'->'j'? No...
    #   Let's look: reversed("level") = "level". Output "jevel". 
    #   Difference: position 0 'l'->'j'. That's odd.
    # " Zebralower" -> "pewolarbeZ " : reversed = "rewolarbeZ " ... 
    #   reversed(" Zebralower") = "rewolarbeZ ". Output "pewolarbeZ ".
    #   Compare: "rewolarbeZ " vs "pewolarbeZ ": position 0 'r'->'p'.
    # "Hello World function lazy" -> "wzal noitcnuf dlroW olleH"
    #   reversed = "yzal noitcnuf dlroW olleH". Output "wzal ...". 
    #   position 0 'y'->'w'.
    # "bananaUPPER" -> "PEPPUananab"
    #   reversed = "REPPUananab". Output "PEPPUananab".
    #   position 0 'R'->'P', position 1 'E'->'E'? wait "REPPU" vs "PEPPU": 
    #   R->P, E->E, P->P, P->P, U->U. Only first char changed R->P.
    # "Zebra" -> "yrbeZ"
    #   reversed = "arbeZ". Output "yrbeZ". 
    #   position 0 'a'->'y'.
    #
    # So: reverse the string, then change the FIRST character somehow.
    # First char of reversed = last char of original.
    # original last chars: '3','l','r','y','R','a'
    # after reverse first chars: '3','l','r','y','R','a'
    # output first chars: '3','j','p','w','P','y'
    # mapping: '3'->'3', 'l'->'j', 'r'->'p', 'y'->'w', 'R'->'P', 'a'->'y'
    # Hmm 'l'->'j' (-2), 'r'->'p' (-2), 'y'->'w' (-2), 'R'->'P' (-2), 
    #   'a'->'y' (-2 mod 26). '3'->'3' (digit unchanged).
    # So: reverse, then shift first char back by 2 (letters only, wrap).
    # Wait but that's weird. Let me reconsider: maybe shift ALL chars? 
    # "abc123" reversed "321cba", output "321cba" - no shift on others.
    # Only first char shifted. Hmm, but why?
    #
    # Alternative: maybe it's reverse then Caesar -2 on the whole string?
    # "321cba" -> shift -2 letters: "321" stay, 'c'->'a','b'->'z','a'->'y' 
    #   = "321azy" not "321cba". No.
    #
    # So only first char of reversed is shifted -2. Odd but fits.
    # Actually wait - maybe it's: reverse, then the LAST char of original 
    #   (now first) gets shifted. But why only that one?
    #
    # Let me reconsider. Maybe the operation isn't "reverse then shift first".
    # Maybe: shift last char of original by -2, then reverse? 
    #   "abc123": last '3'->'3' (digit), reverse "321cba" ✓
    #   "level": last 'l'->'j', then reverse "jevel" ✓ (reverse of "jevel" is "level"? no)
    #   Wait: shift last char then reverse: "levej" reversed = "jevel" ✓
    #   " Zebralower": last 'r'->'p', " Zebralowep" reversed = "pewolarbeZ " ✓
    #   "Hello World function lazy": last 'y'->'w', "...lawz" reversed = "wzal ..." ✓
    #   "bananaUPPER": last 'R'->'P', "bananaUPPEP" reversed = "PEPPUananab" ✓
    #   "Zebra": last 'a'->'y', "Zebry" reversed = "yrbeZ" ✓
    #
    # So: shift the LAST character back by 2 (letters, wrapping, case-preserving),
    #   then reverse the whole string.
    # Digits/symbols: '3'->'3' unchanged (only letters shift).
    # Case preserved: 'R'->'P' (upper), 'a'->'y' (lower).
    # Wrap: 'a'->'y' (a-2 wraps to y), 'b'->'z'.
    import string
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c)-ord('a')-2) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c)-ord('A')-2) % 26 + ord('A'))
        return c
    def f(s):
        if not s:
            return s
        s = s[:-1] + shift(s[-1])
        return s[::-1]
    return {"outputs": [f(x) for x in probe["inputs"]]}
