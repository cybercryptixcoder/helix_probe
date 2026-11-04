def predict(probe):
    # First char uppercased, rest lowercased [E1,E2,E3]
    # Leading whitespace: no capitalization [E2]
    # BUT: a letter that is the 2nd char of a word gets deleted in some cases [E4,E5]
    #   "quote me" -> "quote e"  (the 'm' deleted)
    #   "9lives matter" -> "9lives atter" (the 'm' deleted)
    #   "Example" -> "Exaple" (the 'm' deleted)
    # So: lowercase 'm' is deleted when it is the first letter of a non-initial word? 
    #   Actually: 'm' at start of a word after a space, or... "Example" has 'm' mid-word deleted.
    # Pattern: delete lowercase 'm' that follows a vowel? "Example": 'a' then 'm' -> deleted. 
    #   "quote me": 'e' then space then 'm' -> deleted. "matter": 'm' at word start after space -> deleted.
    #   "Mississippi" kept (capital M). "racecar" no m. "function" no m.
    # Hypothesis: delete lowercase 'm' when preceded by a vowel or space? 
    #   "Example" -> "Exaple": 'a'+'m' deleted. "quote me"->"quote e": space+'m' deleted.
    #   "matter"->"atter": space+'m' deleted. 
    #   But "test caseMiXeD"->"Test casemixed": 'e'+'m'? "casemixed" has 'e','m' -> but m kept!
    #   Hmm "casemixed": after lowercase, "casemixed", 'e' then 'm' kept. Contradiction.
    # Let me reconsider: maybe delete 'm' only when it's the 2nd char of a word (after first letter)?
    #   "Example": E-x-a-m -> m is 4th char, not 2nd. 
    #   "quote me": m is 1st char of word "me". deleted -> "e". 
    #   "matter": m 1st char of word. deleted.
    #   "casemixed": m is 5th char of word "casemixed". kept.
    #   "Example": m is 4th char. deleted. Inconsistent with casemixed.
    # Difference: "Example" is a single word (whole string). "casemixed" is 2nd word.
    # Maybe: delete 'm' in the FIRST word only? "Example"->"Exaple" yes. "Mississippi" capital M kept.
    #   "matter" is 2nd word in "9lives matter" -> deleted though. Hmm.
    # Let me look: "9lives matter"->"9lives atter". m deleted at start of 2nd word.
    #   "quote me"->"quote e". m deleted at start of 2nd word.
    #   "casemixed" m not at start of word. kept.
    #   "Example" m not at start of word but deleted. 
    # Maybe delete 'm' when preceded by 'a' or when at word start?
    #   "Example": 'a'+'m' -> deleted. "casemixed": 'e'+'m' -> kept. 
    #   "matter": word start -> deleted. "me": word start -> deleted.
    # Rule: delete lowercase 'm' if preceded by 'a' or if at start of a word (after space).
    #   Check "Mississippi": capital M, not lowercase, kept. Good.
    #   "test caseMiXeD"->"Test casemixed": m preceded by 'e', not word start -> kept. Good.
    #   "banana": no m. 
    # This fits all evidence. Mark uncertain.
    out = []
    for s in probe["inputs"]:
        if not s:
            out.append(s)
            continue
        first = s[0]
        if first.isspace():
            t = first + s[1:].lower()
        else:
            t = first.upper() + s[1:].lower()
        # delete lowercase 'm' preceded by 'a' or at word start (after space)
        res = []
        for i, ch in enumerate(t):
            if ch == 'm':
                prev = t[i-1] if i > 0 else ''
                if prev == 'a' or prev == ' ':
                    continue
            res.append(ch)
        out.append(''.join(res))
    return {"outputs": out}
