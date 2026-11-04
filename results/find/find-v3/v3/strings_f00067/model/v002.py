def predict(probe):
    # Model: split input into words (whitespace), reverse each word, keep order, join with single space.
    # Then prepend the last character of the original last word to the reversed last word,
    # UNLESS that last character is an uppercase letter. [E1, E2]
    # Evidence:
    #  "hello world" -> "olleh ddlrow": last word "world" ends 'd' -> dup 'd' [E2]
    #  "hello WORLD" -> "olleh DDLROW": last word "WORLD" ends 'D' uppercase -> no dup [E2]
    #  "hello world 123" -> "olleh dlrow 3321": last word "123" ends '3' -> dup '3' [E2]
    #  "hello World" -> "olleh ddlroW": ends 'd' -> dup [E2]
    #  "two  spaces" -> "owt ssecaps": multiple spaces collapse; last word "spaces" ends 's' -> dup [E2]
    #  "  leading and trailing  " -> "gnidael dna gniliart": strip; last word "trailing" ends 'g' -> dup [E2]
    #  "a b c" -> "a b cc": last word "c" ends 'c' -> dup [E2]
    #  "abc def GHI" -> "cba fed IIHG": last word "GHI" ends 'I' uppercase -> no dup [E2]
    #  "one two three!" -> "eno owt !!eerht": last word "three!" ends '!' -> dup '!' [E2]
    #  "Hello, World!" -> ",olleH !!dlroW": last word "World!" ends '!' -> dup '!' [E2]
    #  "abc123" -> "3321cba": ends '3' -> dup [E1]
    #  "bananaUPPER" -> "RREPPUananab": ends 'R' uppercase -> no dup [E1]
    #  "Zebra" -> "aarbeZ": ends 'a' -> dup [E1]
    #  "level" -> "llevel": ends 'l' -> dup [E1]
    #  " Zebralower" -> "rrewolarbeZ": strip, ends 'r' -> dup [E1]
    #  "Hello World function lazy" -> "olleH dlroW noitcnuf yyzal": last word "lazy" ends 'y' -> dup [E1]
    # Empty input -> "" (guess, marked ?)
    outs = []
    for s in probe.get("inputs", []):
        t = s.strip()
        if t == "":
            outs.append("")
            continue
        words = t.split()
        rev = [w[::-1] for w in words]
        last = words[-1]
        if last and not last[-1].isupper():
            rev[-1] = last[-1] + rev[-1]
        outs.append(" ".join(rev))
    return {"outputs": outs}
