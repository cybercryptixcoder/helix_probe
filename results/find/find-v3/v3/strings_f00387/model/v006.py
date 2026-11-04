def predict(probe):
    # Model of the black box.
    #
    # Main idea: the box seems to do a sequence of string-level edits:
    #  - It lowercases the whole string first (so "HELLO WORLD" -> "hello world",
    #    "Zebralower" -> "zebralower"), then capitalizes the first character.
    #    Evidence: E1 "abc123" -> "Abc123"; E1 "Zebra" -> "Zebra";
    #    E2 "HELLO WORLD" -> "Hello world"; E2 "hELLo wORLd" -> "Hello world";
    #    E5 "aMiXeD" -> "Amixed"; E6 "MOM" -> "Mom".
    #  - BUT there is a special deletion rule: the substring "m" (case-insensitive)
    #    is removed in some contexts, and this interacts with the lowercasing.
    #    Evidence: E4 "mango" -> "Ango" (leading m removed, then capitalize);
    #    E4 "mom" -> "O" (all m's removed -> "o" -> "O");
    #    E4 "summer" -> "Suer" (both m's removed);
    #    E4 "m" -> "" ; "am" -> "A" ; "ma" -> "A" ; "m m" -> " " ;
    #    E4 "banana m banana" -> "Banana  banana" (m removed, leaving two spaces);
    #    E6 "mMango" -> "Mango" (leading m removed, then "Mango" capitalized?);
    #    E6 "MangoM" -> "Mangom" (trailing M lowercased, not removed?).
    #
    # The tricky part: deletion of 'm' is not global. Look at E6:
    #  "MOM" -> "Mom"  (no deletion)
    #  "aM"  -> "Am"   (no deletion)
    #  "aMa" -> "Ama"  (no deletion)
    #  "MOMa"-> "Moma" (no deletion)
    #  "mM"  -> "M"    (one m removed)
    #  "Mm"  -> "M"    (one m removed)
    #  "M"   -> "M"
    #  "MM"  -> "Mm"
    #  "mMango" -> "Mango" (leading m removed)
    #  "MangoM" -> "Mangom" (no deletion)
    #
    # Compare E4 "mango" -> "Ango" (m removed) vs E6 "mMango" -> "Mango" (m removed).
    # Compare E4 "mom" -> "O" (both removed) vs E6 "MOM" -> "Mom" (none removed).
    #
    # Hypothesis: the box lowercases the string, then removes all 'm' characters,
    # then capitalizes the first character. Let's test:
    #  "MOM" -> lower "mom" -> remove m -> "o" -> "O". But observed "Mom". FAIL.
    #
    # So the order must be different. Maybe: capitalize first char, then lowercase rest?
    #  "MOM" -> "Mom" (capitalize M, lowercase OM -> "Mom"). Then remove m? Would give "Mo".
    #  Observed "Mom", so no removal.
    #
    # Look again: maybe the removal of 'm' happens BEFORE any case change, and only
    # applies to lowercase 'm' in the ORIGINAL string? Check:
    #  "mango": original has lowercase m at start -> remove -> "ango" -> capitalize -> "Ango". OK.
    #  "mom": original lowercase m's -> remove both -> "o" -> "O". OK.
    #  "summer": remove both m's -> "suer" -> "Suer". OK.
    #  "m": remove -> "" -> "". OK.
    #  "am": remove m -> "a" -> "A". OK.
    #  "ma": remove m -> "a" -> "A". OK.
    #  "m m": remove both m's -> " " -> " ". OK.
    #  "banana m banana": remove m -> "banana  banana" -> capitalize -> "Banana  banana". OK.
    #  "MOM": no lowercase m -> "MOM" -> lowercase+capitalize -> "Mom". OK!
    #  "aM": no lowercase m -> "aM" -> "Am". OK!
    #  "aMa": no lowercase m -> "aMa" -> "Ama". OK!
    #  "MOMa": no lowercase m -> "MOMa" -> "Moma". OK!
    #  "mM": remove lowercase m -> "M" -> "M". OK!
    #  "Mm": remove lowercase m -> "M" -> "M". OK!
    #  "M": no lowercase m -> "M" -> "M". OK!
    #  "MM": no lowercase m -> "MM" -> lowercase rest -> "Mm". OK!
    #  "mMango": remove lowercase m -> "Mango" -> capitalize first, lowercase rest -> "Mango". OK!
    #  "MangoM": no lowercase m -> "MangoM" -> capitalize first, lowercase rest -> "Mangom". OK!
    #
    # This works for all E6 and E4 cases! So the rule is:
    #  1. Remove all lowercase 'm' characters from the ORIGINAL string.
    #  2. Then apply the case transform: first char uppercase, rest lowercase.
    #
    # Check E1 "Zebralower" -> no lowercase m -> "Zebralower" -> "Zebralower". OK.
    # E1 "bananaUPPER" -> no lowercase m -> "bananaUPPER" -> "Bananaupper". OK.
    # E3 "Example123" -> no lowercase m -> "Example123" -> "Exaple123"? Wait, "Example" has no m... 
    #   "Example123" -> capitalize first, lowercase rest -> "Example123". But observed "Exaple123"!
    #   There's an 'm' in "Example"? E-x-a-m-p-l-e. Yes! lowercase 'm' at index 3.
    #   Remove it -> "Exaple123" -> "Exaple123". OK!
    # E3 "banana data banana " -> no lowercase m -> "Banana data banana ". OK.
    # E3 "lazy" -> "Lazy". OK.
    # E3 "banana" -> "Banana". OK.
    # E3 "level" -> "Level". OK.
    # E5 "function Hello World" -> no lowercase m -> "Function hello world". OK.
    # E5 "banana a data " -> "Banana a data ". OK.
    # E5 "Example " -> remove m -> "Exaple " -> "Exaple ". OK.
    # E5 "world42" -> "World42". OK.
    # E5 "racecar Example racecar" -> remove m in Example -> "racecar Exaple racecar" -> "Racecar exaple racecar". OK.
    # E5 "aMiXeD" -> no lowercase m (M is uppercase) -> "aMiXeD" -> "Amixed". OK.
    # E2 "hello world" -> "Hello world". OK.
    # E2 "hello  world" -> "Hello  world". OK.
    # E2 "hello-world" -> "Hello-world". OK.
    # E2 "hello.world" -> "Hello.world". OK.
    # E2 "hello, world" -> "Hello, world". OK.
    # E2 "hello123world" -> "Hello123world". OK.
    # E2 "HELLO WORLD" -> no lowercase m -> "HELLO WORLD" -> "Hello world". OK.
    # E2 "hELLo wORLd" -> "Hello world". OK.
    # E2 "123 hello" -> "123 hello". OK.
    # E2 " hello" -> " hello". OK.
    # E1 "abc123" -> "Abc123". OK.
    # E1 "level" -> "Level". OK.
    # E1 " Zebralower" -> " zebralower". OK.
    # E1 "Hello World function lazy" -> "Hello world function lazy". OK.
    #
    # Great, the rule is consistent across all evidence.

    def transform(s):
        # Step 1: remove all lowercase 'm' characters from the original string.
        s = s.replace('m', '')
        # Step 2: capitalize first character, lowercase the rest.
        if not s:
            return s
        return s[0].upper() + s[1:].lower()

    inputs = probe.get("inputs", [])
    outputs = [transform(x) for x in inputs]
    return {"outputs": outputs}
