def predict(probe):
    # Observations from E1:
    # - "a" -> "yJTQL": first char 'a' became 'y' (a->y, shift? a is 1st letter, y is 25th: -2 or +24)
    # - "A" -> "YJTQL": 'A'->'Y' (same shift, uppercase preserved)
    # - "1" -> "1JTQL": digit unchanged, suffix "JTQL" appended
    # - "!" -> "!JTQL": symbol unchanged, suffix appended
    # - " " -> " JTQL": space unchanged, suffix appended
    # - "" -> "HTQL": empty gives "HTQL" (suffix without leading J? Actually "JTQL" vs "HTQL")
    # - "hello" -> "felloJTQL": first char 'h'->'f' (h=8, f=6: -2), rest unchanged, suffix appended
    # - "Hello" -> "FelloJTQL": 'H'->'F' (-2), rest unchanged
    # - "abc123" -> "ybc123JTQL": 'a'->'y' (-2 mod 26), rest unchanged
    # - "a b" -> "y bJTQL": 'a'->'y', rest unchanged
    #
    # Rule hypothesis: 
    #   - If input is empty: return "HTQL"
    #   - Else: shift first char back by 2 in alphabet (case preserved, non-letters unchanged),
    #           keep rest of string unchanged, append "JTQL"
    #
    # Check empty case: "" -> "HTQL". But non-empty all end with "JTQL". 
    # Maybe the suffix is always "JTQL" but empty string is special, OR
    # the transformation is: shift first char by -2, then append "JTQL", but for empty
    # there's no first char... "HTQL" = "JTQL" with J->H? Hmm.
    # Alternative: maybe it's "shift first char -2, append JTQL" and empty string 
    # gets treated as... Actually "HTQL" could be "JTQL" with first char shifted -2 (J->H).
    # So maybe: the whole thing is: take input, shift its first char -2, append "JTQL",
    # but if input empty, the "first char" is the J of JTQL itself? That's weird.
    # 
    # Simpler: empty -> "HTQL" is a special case. Or: the rule is "shift first char -2 
    # (if exists), append JTQL", and empty -> "HTQL" is separate.
    # Actually maybe: result = shift_first(s) + "JTQL", and for empty, shift_first("")="H"? 
    # No. Let's just special-case empty -> "HTQL".
    #
    # Wait — maybe it's: prepend nothing, but the suffix depends. Let me reconsider:
    # "a"->"yJTQL". If we shift 'a' by -2 we get 'y'. Then + "JTQL". Good.
    # "" -> "HTQL". If we shift nothing and append "JTQL" we'd get "JTQL", not "HTQL".
    # So empty is special: "HTQL".
    #
    # Could it be that the suffix is "JTQL" and empty input produces "HTQL" because
    # it's "shift first char of JTQL by -2"? Unlikely. Special case it.
    
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') - 2) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') - 2) % 26 + ord('A'))
        return c
    
    out = []
    for s in probe["inputs"]:
        if s == "":
            out.append("HTQL")
        else:
            out.append(shift(s[0]) + s[1:] + "JTQL")
    return {"outputs": out}
