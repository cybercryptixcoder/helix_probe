def predict(probe):
    # Capitalize first letter of each whitespace-separated word, lowercase the rest [E1, E2]
    # "abc123"->"Abc123", "level"->"Level", "bananaUPPER"->"Bananaupper", "Zebra"->"Zebra" [E1]
    # "hello, world"->"Hello, world", "don't stop"->"Don't stop", "MiXeD case"->"Mixed case" [E2]
    # "foo-bar"->"Foo-bar", "a1b2C3"->"A1b2c3", "ends."->"Ends.", "(paren)"->"(paren)" [E2]
    # "123abc"->"123abc" (leading digit: first char upper is same, rest lower) [E2]
    # "tab\there"->"Tab\there" (tab is whitespace separator) [E2]
    # Anomaly: some strings lose a letter. "  multiple   spaces  "->"  ultiple   spaces  " [E2]
    #   "Example123"->"Exaple123" [E3] -- drops the 'm' (2nd char of first word)
    #   " Zebralower"->" zebralower" [E1] -- drops 'Z' (1st char of first word after leading space)
    #   Hypothesis (?): the box deletes the character at index 1 of the whole string
    #   when the first word has length >= 2? Check: "Example123" idx1='x'? no, dropped 'm' (idx2).
    #   Reconsider: "Example123" -> "Exaple123": removed 'm' at index 2.
    #   "  multiple..." -> removed 'm' at index 2 (after two spaces).
    #   " Zebralower" -> removed 'Z' at index 1.
    #   Pattern (?): remove the character at index = (number of leading spaces) + 1?
    #     "Example123": 0 leading spaces -> remove idx1 = 'x'? but 'x' kept. No.
    #   Alternative (?): remove the 2nd letter of the first word.
    #     "Example123": first word "Example123", 2nd letter 'x'? but dropped 'm'. No.
    #   Alternative (?): remove the 3rd character of the first word.
    #     "Example123": 'a'? dropped 'm'. No.
    #   Look again: "Example123"->"Exaple123": E x a m p l e -> E x a p l e. 'm' removed (idx3).
    #     "  multiple"->"  ultiple": m u l t -> u l t. 'm' removed (idx0 of word).
    #     " Zebralower"->" zebralower": Z e b r a -> e b r a (after lowercasing). 'Z' removed (idx0 of word).
    #   Hmm inconsistent. Maybe it's about the letter 'm'? "Example" has 'm', "multiple" has 'm',
    #     "Zebralower" has no 'm' but lost 'Z'. 
    #   Wait " Zebralower" output " zebralower": input " Zebralower", output " zebralower".
    #     Compare char by char: " Zebralower" vs " zebralower". Same length? 
    #     " Zebralower" = space,Z,e,b,r,a,l,o,w,e,r (12)
    #     " zebralower" = space,z,e,b,r,a,l,o,w,e,r (12). Same length! Just lowercased Z.
    #     So NOT dropped -- 'Z' became 'z' because... it's not first letter of a word?
    #     " Zebralower": leading space, then "Zebralower" is first word -> should be "Zebralower".
    #     But got "zebralower". So leading-space word is NOT capitalized. [E1]
    #   Recheck "  multiple   spaces  " -> "  ultiple   spaces  ": 
    #     "  multiple" = 2 spaces + "multiple". Output "  ultiple" = 2 spaces + "ultiple". 'm' dropped!
    #     Length differs by 1. So 'm' really dropped here.
    #   And "Example123"->"Exaple123": 'm' dropped, length 10->9.
    #   So: 'm' is dropped in "Example123" and "multiple". Both have 'm' as... 
    #     "Example123": 'm' is 4th char (idx3). "multiple": 'm' is 1st char of word (idx0).
    #   Maybe rule: drop the letter 'm' when it's the... hmm.
    #   "banana data banana " -> "Banana data banana " no 'm'. "lazy" no m. "banana" no m. "level" no m.
    #   "Hello World function lazy" -> "Hello world function lazy" no drop (no 'm').
    #   "MiXeD case" -> "Mixed case": has 'M'! Not dropped. But it's uppercase M.
    #   "bananaUPPER" -> "Bananaupper" no m.
    #   Hypothesis (?): lowercase 'm' is deleted from the string, then capitalize words.
    #     "Example123": remove 'm' -> "Exaple123", capitalize -> "Exaple123". ✓
    #     "  multiple   spaces  ": remove 'm' -> "  ultiple   spaces  ", capitalize words -> 
    #        "  Ultiple   Spaces  "? But observed "  ultiple   spaces  " (lowercase, no cap).
    #     Hmm. So after removing 'm', capitalization differs.
    #   Maybe capitalization happens first, then 'm' removed? 
    #     "  multiple   spaces  " cap -> "  Multiple   Spaces  ", remove 'm' -> "  Multiple..."? 
    #        'M' uppercase not removed. Doesn't work.
    #   Let's reconsider: maybe the box removes the SECOND character of the string if...
    #     "Example123" remove idx? 'm' is idx3. No.
    #   Try: remove the character that is 'm' only in specific position? 
    #     "Example123": 'm' at idx3. "multiple": 'm' at idx2 (after 2 spaces). 
    #     "MiXeD": 'M' at idx0 uppercase, kept.
    #   Simplest consistent rule (?): delete every lowercase 'm' from the input, then apply
    #     word-capitalization to the RESULT, but... "  ultiple" wasn't capitalized.
    #     Unless: capitalization only applies to words that originally started with a letter
    #     and weren't broken? "multiple"->"ultiple" now starts with 'u', a letter, should cap to "Ultiple".
    #   This is getting complex. Let me look for a cleaner pattern.
    #   "Example123"->"Exaple123": E-x-a-[m]-p-l-e. Removed 4th char.
    #   "  multiple   spaces  "->"  ultiple   spaces  ": removed 'm' = 3rd char (idx2).
    #   " Zebralower"->" zebralower": no removal, just lowercased (leading space word not capped).
    #   Maybe: the box removes a character at a position related to something, AND
    #     leading-whitespace words are not capitalized.
    #   Given uncertainty, best guess (?): 
    #     - Words after leading whitespace are NOT capitalized (stay lowercase). [E1 " Zebralower"]
    #     - The letter 'm' (lowercase) is deleted from the whole string. [E2, E3]
    #     - Then capitalize first letter of each word that is at start or after whitespace,
    #       EXCEPT words preceded by leading whitespace at string start? 
    #   Actually "  ultiple" - after deleting 'm', "ultiple" is a word at start (after spaces).
    #     It wasn't capitalized. But "Hello world" second word "world" wasn't capitalized either
    #     (only first word of string gets capitalized? No: "Hello World function lazy"->"Hello world function lazy"
    #      only "Hello" capped, rest lowercase!). 
    #   Wait E1: "Hello World function lazy" -> "Hello world function lazy". Only FIRST word capped!
    #   E2: "hello, world" -> "Hello, world" only first word. "don't stop"->"Don't stop" only first.
    #   "MiXeD case"->"Mixed case" only first word.
    #   So rule: capitalize ONLY the first word of the whole string (first letter), lowercase everything else!
    #   Check "banana data banana "->"Banana data banana " ✓ (only first word capped)
    #   "test case"->"Test case" ✓
    #   "  multiple   spaces  "->"  ultiple   spaces  ": first word after spaces "ultiple" NOT capped.
    #     So if string starts with whitespace, first word not capitalized. [E1 " Zebralower"->" zebralower"]
    #   "Example123"->"Exaple123": first word "Example123" should cap to "Example123", but 'm' dropped.
    #   So: lowercase everything, capitalize first letter IF string doesn't start with whitespace,
    #     and delete lowercase 'm'? Let's test:
    #     "Example123": lower->"example123", cap first->"Example123", delete 'm'->"Exaple123" ✓
    #     "  multiple   spaces  ": lower->"  multiple   spaces  ", starts with space so no cap,
    #        delete 'm'->"  ultiple   spaces  " ✓
    #     " Zebralower": lower->" zebralower", starts with space no cap, no 'm' -> " zebralower" ✓
    #     "MiXeD case": lower->"mixed case", cap first->"Mixed case", delete 'm'->"ixed case"? 
    #        But observed "Mixed case"! 'M' kept. Contradiction with deleting 'm'.
    #   Hmm. "MiXeD case"->"Mixed case" keeps 'M'. So not all 'm' deleted.
    #   Difference: in "MiXeD", 'm' is the FIRST letter (capitalized to 'M'). In "Example", 'm' is interior.
    #   In "multiple", 'm' is first letter of word but not capitalized (leading space), and it was deleted.
    #   So maybe: delete lowercase 'm' that is NOT the first character of the string?
    #     "Example123": 'm' at idx3, not first -> delete ✓
    #     "  multiple": 'm' at idx2, not first -> delete ✓
    #     "MiXeD": 'm' at idx0, first -> keep, cap to 'M' ✓
    #     " Zebralower": no 'm' ✓
    #   This works for all! Rule (?): delete every lowercase 'm' except at index 0.
    #   But wait, what about uppercase 'M' elsewhere? "MiXeD" has 'M' at 0 only. No other data.
    #   Let's also verify "bananaUPPER"->"Bananaupper": lower->"bananaupper", cap first->"Bananaupper" ✓
    #   "a1b2C3"->"A1b2c3": lower->"a1b2c3", cap first->"A1b2c3" ✓
    #   "123abc"->"123abc": lower same, cap first '1'->'1' ✓
    #   "tab\there"->"Tab\there": lower->"tab\there", cap first->"Tab\there" ✓
    #   "ends."->"Ends." ✓, "(paren)"->"(paren)" cap '(' stays ✓
    #   "foo-bar"->"Foo-bar" ✓, "don't stop"->"Don't stop" ✓
    #   "abc123"->"Abc123" ✓, "level"->"Level" ✓, "Zebra"->"Zebra" ✓
    #   "Hello World function lazy"->"Hello world function lazy" ✓
    #   "banana data banana "->"Banana data banana " ✓
    #   All consistent! 
    # Final rules:
    # 1. Lowercase the whole string.
    # 2. Delete every 'm' that is not at index 0 (of the lowercased string). (?)
    # 3. If the (original) string does not start with whitespace, capitalize the first character.
    #    (If it starts with whitespace, leave as is.)
    # Note: order matters. Let's do: lower, then delete 'm' (except idx0), then cap first char if no leading ws.
    #   But "MiXeD": lower "mixed case", delete 'm' except idx0 -> 'm' at 0 kept -> "mixed case",
    #     cap first (no leading ws) -> "Mixed case" ✓
    #   "Example123": lower "example123", delete 'm' (idx3) -> "exaple123", cap -> "Exaple123" ✓
    #   "  multiple": lower "  multiple   spaces  ", delete 'm' (idx2) -> "  ultiple   spaces  ",
    #     starts with ws so no cap -> "  ultiple   spaces  " ✓
    # Good.
    out = []
    for s in probe["inputs"]:
        t = s.lower()
        # delete lowercase 'm' except at index 0
        chars = []
        for i, c in enumerate(t):
            if c == 'm' and i != 0:
                continue
            chars.append(c)
        t = "".join(chars)
        if t and not s[:1].isspace():
            t = t[0].upper() + t[1:]
        out.append(t)
    return {"outputs": out}
