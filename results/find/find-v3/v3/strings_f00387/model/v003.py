def predict(probe):
    # Hypothesis: lowercase everything, then capitalize the first letter of the whole string.
    # "Example123" -> "Exaple123" [E3]: note the 'm' is dropped! "Example" -> "Exaple".
    # Wait: "Example123" -> "Exaple123" drops the 'm'. That's a deletion, not capitalization.
    # Let's re-examine: "Example123" -> "Exaple123". Original: E x a m p l e. Output: E x a p l e.
    # The 'm' (index 3) is removed. Hmm.
    # Other E3: "test case"->"Test case", "banana data banana "->"Banana data banana ",
    # "lazy"->"Lazy", "banana"->"Banana", "level"->"Level". None drop letters.
    # E1: "abc123"->"Abc123", "level"->"Level", " Zebralower"->" zebralower",
    # "Hello World function lazy"->"Hello world function lazy", "bananaUPPER"->"Bananaupper",
    # "Zebra"->"Zebra". No deletions.
    # E2: no deletions.
    # So only "Example123" shows a deletion. Odd. Maybe it's not a deletion but a different rule.
    # "Example" -> "Exaple": could be removing a repeated-ish letter? m appears once.
    # Could be: remove the letter that makes a common word? Unlikely.
    # Alternative: maybe the box removes a character at a specific position for longer words?
    # "Example" length 7 -> "Exaple" length 6. "banana" length 6 -> "Banana" length 6 (no drop).
    # "Hello World function lazy" length 25 -> same length. So not length-based.
    # Maybe it's a typo-like transformation: "Example" -> "Exaple" is a known common misspelling?
    # Hmm, "Exaple" is a common typo of "Example" (m dropped). Maybe the box has a dictionary
    # of common misspellings? That seems too specific.
    # Let's reconsider: maybe the rule is capitalize first letter, lowercase rest, AND
    # remove the letter 'm'? Check: "bananaUPPER" has no m. "Hello World function lazy" no m.
    # "Example123" has m -> removed. "test case" no m. "banana data banana" no m.
    # "lazy" no m. "banana" no m. "level" no m. E2 inputs: "hello world" no m, etc.
    # "HELLO WORLD" no m. "hELLo wORLd" no m. "123 hello" no m. " hello" no m.
    # "abc123" no m. " Zebralower" no m. "Zebra" no m.
    # So "remove all 'm' characters" is consistent with ALL evidence!
    # But wait, is it plausible? Let's check "Example123" -> "Exaple123": yes, m removed.
    # Hmm but that's a weird rule. Could it be removing 'm' only? Or some class?
    # Only one data point with m. Let's hypothesize: remove letter 'm' (case-insensitive?).
    # Actually maybe it's a "leet" or specific letter removal. Without more data, guess 'm'.
    # But also could be: the box removes the 4th character? "Example" 4th char (index 3) is 'm'.
    # "banana" 4th char index 3 is 'a' -> would give "banna"? No, output "Banana" keeps all.
    # So not position-based. 'm' removal fits.
    # Let's also double check capitalization still holds: "Example123"->"Exaple123": E upper, rest lower, m gone. Yes.
    # "bananaUPPER"->"Bananaupper": B upper, rest lower. Yes.
    # So model: remove all 'm'/'M', then capitalize first alphabetic char, lowercase rest.
    # Order: does removal happen before or after capitalization? Doesn't matter for m.
    # But if first letter were 'm'? e.g. "mango" -> remove m -> "ango" -> capitalize -> "Ango".
    # Or capitalize first -> "Mango" -> remove m -> "ango". Ambiguous. Guess: remove first, then capitalize.
    # Mark with ?.
    def transform(s):
        s = s.replace("m", "").replace("M", "")
        out = []
        seen_letter = False
        for ch in s:
            if ch.isalpha():
                if not seen_letter:
                    out.append(ch.upper())
                    seen_letter = True
                else:
                    out.append(ch.lower())
            else:
                out.append(ch)
        return "".join(out)
    return {"outputs": [transform(x) for x in probe["inputs"]]}
