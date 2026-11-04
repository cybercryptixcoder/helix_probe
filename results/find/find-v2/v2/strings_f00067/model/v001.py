def predict(probe):
    # Observations from E1:
    # "abc123" -> "3321cba": reversed
    # "level" -> "llevel": first char prepended to reversed? "level" reversed = "level", prepend 'l' -> "llevel"
    # " Zebralower" -> "rrewolarbeZ": reversed
    # "Hello World function lazy" -> "olleH dlroW noitcnuf yyzal": words reversed in place, but "lazy"->"yyzal" (first char prepended)
    # "bananaUPPER" -> "RREPPUananab": reversed
    # "Zebra" -> "aarbeZ": reversed
    #
    # Hypothesis: reverse the string. But "level" -> "llevel" and "lazy" -> "yyzal" don't fit plain reverse.
    # Wait: "level" reversed is "level". Output "llevel" = 'l' + "level". 
    # "lazy" reversed is "yzal". Output "yyzal" = 'y' + "yzal"? No, "yyzal" = 'y' + "yzal" = "yyzal". Yes!
    # So rule: reverse string, then prepend the first character of the reversed string? 
    # reversed("level")="level", first char 'l', prepend -> "llevel". ✓
    # reversed("lazy")="yzal", first char 'y', prepend -> "yyzal". ✓
    # But "abc123" reversed = "321cba", output "3321cba" = '3' + "321cba". ✓ first char of reversed is '3'.
    # " Zebralower" reversed = "rewolarbeZ", first char 'r', prepend -> "rrewolarbeZ". ✓
    # "bananaUPPER" reversed = "RREPPUananab", first char 'R', prepend -> "RREPPUananab". ✓
    # "Zebra" reversed = "arbeZ", first char 'a', prepend -> "aarbeZ". ✓
    # "Hello World function lazy" reversed = "yzal noitcnuf dlroW olleH". Output is "olleH dlroW noitcnuf yyzal".
    # That's word-order reversed AND each word reversed, with first char of each reversed word prepended? Let's check:
    # words: Hello World function lazy -> reversed order: lazy function World Hello
    # each reversed: yzal noitcnuf dlroW olleH
    # prepend first char of each reversed word: y+yzal=yyzal, n+noitcnuf=nnoitcnuf... but output is "noitcnuf" not "nnoitcnuf".
    # Hmm. Output: "olleH dlroW noitcnuf yyzal". That's words in original order, each word reversed, and only "lazy" got doubled.
    # Actually "olleH"=reverse(Hello), "dlroW"=reverse(World), "noitcnuf"=reverse(function), "yyzal"=reverse(lazy) with 'y' prepended.
    # So it's per-word: reverse each word, and prepend first char of reversed word IF...? 
    # For "Hello" reversed "olleH", first char 'o', would give "oolleH" but output is "olleH". So not all words.
    # Maybe only the LAST word gets the prepend? "lazy" is last word. ✓
    # Check single-word cases: "level" is the whole (last) word -> prepend. ✓ "abc123" last word -> prepend. ✓
    # " Zebralower": has leading space. Words: ["", "Zebralower"]? reversed "rewolarbeZ", prepend 'r' -> "rrewolarbeZ". ✓
    # So rule: split into words preserving spaces? Reverse each word, prepend first char of reversed word to the LAST word only.
    # Actually simpler: reverse each word in place, then prepend first char of the last reversed word.
    # "Hello World function lazy": reverse each -> "olleH dlroW noitcnuf yzal", prepend 'y' to last -> "yyzal". ✓
    # "bananaUPPER": single word, reverse "RREPPUananab", prepend 'R' -> "RREPPUananab". ✓
    # "Zebra": reverse "arbeZ", prepend 'a' -> "aarbeZ". ✓
    # "abc123": reverse "321cba", prepend '3' -> "3321cba". ✓
    # "level": reverse "level", prepend 'l' -> "llevel". ✓
    # " Zebralower": reverse "rewolarbeZ", prepend 'r' -> "rrewolarbeZ". ✓
    #
    # Rule: reverse each whitespace-separated word in place; then prepend the first character of the reversed last word.
    # Edge: empty string? No last word. Handle gracefully.
    import re
    try:
        s = probe["inputs"]
        outs = []
        for x in s:
            if not isinstance(x, str):
                x = str(x)
            parts = re.split(r'(\s+)', x)
            words = [p for p in parts if p and not p.isspace()]
            rev_words = [w[::-1] for w in words]
            # rebuild preserving whitespace
            result_parts = []
            wi = 0
            for p in parts:
                if p and not p.isspace():
                    result_parts.append(rev_words[wi])
                    wi += 1
                else:
                    result_parts.append(p)
            res = "".join(result_parts)
            if rev_words:
                res = rev_words[-1][0] + res
            outs.append(res)
        return {"outputs": outs}
    except Exception:
        return {"outputs": ["" for _ in probe.get("inputs", [])]}
