def predict(probe):
    # Strip leading/trailing whitespace [E1, E2]
    # Split on whitespace, reverse each word [E1, E2, E3]
    # Prepend last char of stripped string to the LAST word only [E1, E2, E3]
    #   - E3 "banana data banana " -> "ananab atad ananab" (no prepend! trailing space)
    #   - E2 "trailing  " -> "gniliart" (prepend 'g' = last char of stripped)
    #   - E1 "bananaUPPER" -> "RREPPUananab" (prepend 'R')
    # So: prepend happens only when input has NO trailing whitespace? Check:
    #   E3 "banana data banana " has trailing space -> no prepend
    #   E2 "trailing  " has trailing space -> prepend 'g' (last char of stripped "trailing")
    #   Contradiction. Re-examine: E3 last word "banana" reversed "ananab", no prepend.
    #   E2 "trailing  " stripped "trailing", last char 'g', reversed "gniliart" -> prepend 'g'.
    #   E1 "bananaUPPER" -> prepend 'R' (last char).
    # Hypothesis: prepend last char of stripped string to last word ONLY IF
    #   the last word (after strip) ends with a non-space char... both do.
    # Alternative: prepend last char of ORIGINAL input (unstripped) to last word.
    #   E3 "banana data banana " last char ' ' -> prepend ' '? output "ananab" no space.
    #   E2 "trailing  " last char ' ' -> would prepend ' ', but got 'g'. No.
    # Alternative: prepend last char of stripped string, but only if stripped != original
    #   (i.e., input had surrounding whitespace)? E2 "trailing  " stripped differs -> prepend 'g' yes.
    #   E2 "  leading" stripped differs -> prepend 'g' yes ("ggnidael").
    #   E3 "banana data banana " stripped differs -> would prepend 'a', but got "ananab". No.
    # Look again E3: "banana data banana " -> "ananab atad ananab". No prepend.
    #   vs E2 "trailing  " -> "gniliart" prepend 'g'.
    # Difference: E3 has multiple words, E2 single word. But E1 multi-word "Hello World function lazy"
    #   -> "olleH dlroW noitcnuf yyzal" prepend 'y' (last char of "lazy"). Multi-word DOES prepend.
    # So why E3 no prepend? Input "banana data banana " - last word "banana", last char 'a'.
    #   Output last word "ananab" = reverse of "banana", no prepend.
    # Maybe prepend is last char of stripped string, but only if that char is NOT already
    #   the first char of the reversed last word? "banana" reversed "ananab", last char 'a',
    #   first char of reversed is 'a' -> skip? E1 "lazy" reversed "yzal", last char 'y',
    #   first char 'y' -> but output "yyzal" has prepend! Contradiction.
    # Recheck E1: "lazy" -> "yyzal". reversed "yzal", prepend 'y' -> "yyzal". Yes prepend.
    # E3 "banana" -> "ananab". reversed "ananab", prepend 'a' -> "aananab". But got "ananab".
    # Hmm E3 "banana" (standalone, 5th input) -> "aananab" (prepend 'a'). Yes!
    # So standalone "banana" prepends. But "banana data banana " last word doesn't.
    # Difference: trailing space in "banana data banana ".
    # E2 "trailing  " trailing spaces -> prepend 'g'. Contradiction again.
    # Wait: "trailing  " stripped "trailing", last char 'g'. Output "gniliart" = 'g'+reverse("trailing").
    #   Actually reverse("trailing")="gniliart". So 'g' is just first char of reversed! No prepend needed!
    # Recheck: reverse("trailing") = g n i l i a r t = "gniliart". Yes! No prepend.
    # So E2 "trailing  " -> "gniliart" is just reversal, NO prepend.
    # E2 "  leading" -> "ggnidael". reverse("leading")="gnidael". Output has extra 'g' -> prepend 'g'.
    #   last char of stripped "leading" is 'g'. Prepend 'g'. Yes.
    # So: prepend last char of stripped string to last word, EXCEPT when input has trailing whitespace?
    #   "trailing  " has trailing ws -> no prepend (correct, "gniliart").
    #   "  leading" has leading ws only -> prepend (correct).
    #   "banana data banana " trailing ws -> no prepend (correct).
    #   E1 "bananaUPPER" no ws -> prepend 'R' (correct).
    #   E3 "banana" no ws -> prepend 'a' (correct).
    #   E2 "a  b" no trailing ws -> "a bb": last word "b" reversed "b", prepend last char 'b' -> "bb". Correct!
    #   E2 "x y z" -> "x y zz": last char 'z', prepend -> "zz". Correct!
    # Rule: prepend last char of stripped string to last reversed word, UNLESS original input
    #   ends with whitespace.
    outs = []
    for x in probe.get("inputs", []):
        if not isinstance(x, str):
            outs.append("")
            continue
        s = x.strip()
        if not s:
            outs.append("")
            continue
        words = s.split()
        rev = [w[::-1] for w in words]
        if not x.endswith((" ", "\t", "\n", "\r", "\f", "\v")):
            rev[-1] = s[-1] + rev[-1]
        outs.append(" ".join(rev))
    return {"outputs": outs}
