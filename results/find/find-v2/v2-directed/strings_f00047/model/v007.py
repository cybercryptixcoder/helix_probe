def predict(probe):
    # Model of the black box.
    #
    # Beliefs (each line cites evidence):
    # 1. Trailing whitespace (spaces, tabs, newlines, \r) is stripped from the end [E7, E12].
    # 2. Leading whitespace is preserved exactly [E4 " hello", E5 "  hello", E7 "  hello", E9 " ABC"].
    # 3. After that, the FIRST letter of the (trimmed) string is uppercased [E1 "hello"->"Hello", E2 "123abc" stays, E9 "1ABC"->"1abc"].
    #    - "First letter" means: skip leading non-letters (digits, punctuation, spaces) and uppercase the first alphabetic char [E5 "123 hello"->"123 hello", "!hello world"->"!hello world", "'hello"->"'hello", "(hello)"->"(hello)"].
    #    - If no letter exists, nothing changes [E2 "123abc"->"123abc" (first letter 'a' already lower? no: 'a' is first letter and stays lowercase -> see below), E12 "123"->"123", "!"->"!"]
    # 4. The rest of the string is lowercased [E3 "hELLO"->"Hello", "HELLO WORLD"->"Hello world", E6 "Hello WORLD"->"Hello world", E10 "café AU LAIT"->"Café au lait"].
    #    - So the operation is: uppercase the first letter, lowercase everything else.
    # 5. BUT: if the first letter is preceded by leading non-letter characters, the whole string is lowercased (first letter NOT uppercased) [E2 "123abc"->"123abc", E5 "123 hello"->"123 hello", "!hello world"->"!hello world", "-abc"->"-abc", "'hello"->"'hello", "(hello)"->"(hello)", E9 "1ABC"->"1abc", "!ABC"->"!abc", "-XY z"->"-xy z", "(HI)"->"(hi)"].
    #    - Exception: leading whitespace does NOT block uppercasing [E4 " hello"->" hello" (no letter after space? 'h' is first letter but result stays " hello" lower... wait)]
    #    - Re-examine: " hello" -> " hello" (E4, E5, E7). So leading space also blocks uppercasing.
    #    - But "  hello" -> "  hello" [E5, E7]. And " hello world " -> " hello world" [E4].
    #    - So: uppercasing happens ONLY if the first character of the trimmed string is a letter [E1 all start with letters].
    #    - Verify: "ABC def" -> "Abc def" [E3, E6]: starts with letter -> uppercase first, lower rest. Yes.
    #    - "aB Cd" -> "Ab cd" [E6]: starts with letter. Yes.
    #    - "9Lives" -> "9lives" [E6]: starts with digit -> all lowercase. Yes.
    #    - "x Y Z" -> "X y z" [E6]: starts with letter. Yes.
    #    - "MiXeD CaSe" -> "Mixed case" [E6]: starts with letter. Yes.
    #    - "QQ" -> "Qq" [E6]: starts with letter. Yes.
    #    - "123 ABC" -> "123 abc" [E6]: starts with digit -> all lowercase. Yes.
    #    - "!FOO bar" -> "!foo bar" [E6]: starts with punct -> all lowercase. Yes.
    #    - "ABC def" appears in E3 and E6 both -> "Abc def". Consistent.
    # 6. So the rule: strip trailing whitespace; if the resulting string starts with a letter (Unicode letter), uppercase that first char and lowercase the remainder; otherwise lowercase the entire string.
    # 7. Unicode letters count as letters [E10 "ÉCOLE"->"École", "über"->"Über", "àbc"->"Àbc"].
    #    - "ÉCOLE" starts with É (letter) -> uppercase É, lower rest -> "École". Yes.
    #    - "ÜBER" -> "Über". Yes.
    #    - "ÀBC def" -> "Àbc def". Yes.
    #    - "日本" -> "日本" (no case). Yes.
    # 8. Apostrophes/hyphens don't affect: only first char matters [E11 "don't"->"Don't", "o'neil"->"O'neil", "it's a test"->"It's a test", "rock 'n' roll"->"Rock 'n' roll"].
    # 9. Trailing whitespace stripped includes spaces, tabs, \n, \r [E7 "hello\t"->"Hello", "hello\n"->"Hello", "hello\r"->"Hello", "hello  "->"Hello", E12 "hello!  "->"Hello!", "hello! \t"->"Hello!", "hello.  \n"->"Hello.", "123  "->"123", "!  "->"!", "  "->"", "hello world  "->"Hello world", "a b  "->"A b", "hello\t\t"->"Hello", "Hi!  "->"Hi!"].
    # 10. Internal whitespace preserved [E1 "hello world"->"Hello world", E4 "hello\tworld"->"Hello\tworld", "hello\nworld"->"Hello\nworld", "hello\rworld"->"Hello\rworld", "hello  world"->"Hello  world"].
    # 11. Leading whitespace preserved [E4 " hello world " -> " hello world", E5 "  hello"->"  hello", E7 " hello"->" hello", "  hello"->"  hello", "  hello  "->"  hello", E9 "  ABC def"->"  abc def"].
    #    - Note "  ABC def" -> "  abc def": starts with space -> all lowercase. Yes.
    #    - "\thello" -> "\thello" [E7]: starts with tab -> all lowercase. Yes.
    #    - "\nhello" -> "\nhello" [E7]. Yes.
    # 12. "hello \t" -> "Hello" [E7]: trailing whitespace (space+tab) stripped, then "hello" starts with letter -> "Hello". Yes.
    # 13. "hello\t " -> "Hello" [E7]. Yes.
    # 14. "hello! " -> "Hello!" [E8]: trailing space stripped, "hello!" starts with letter -> "Hello!". Yes.
    # 15. "hello. " -> "Hello." [E8]. Yes.
    # 16. "hello!  " -> "Hello!" [E12]. Yes.
    # 17. "hello.  \n" -> "Hello." [E12]. Yes.
    # 18. "hello! \t" -> "Hello!" [E12]. Yes.

    import unicodedata

    def is_letter(ch):
        return ch.isalpha()

    def process(s):
        # Strip trailing whitespace
        s = s.rstrip()
        if not s:
            return s
        if is_letter(s[0]):
            return s[0].upper() + s[1:].lower()
        else:
            return s.lower()

    try:
        inputs = probe.get("inputs", [])
        outputs = [process(x) for x in inputs]
        return {"outputs": outputs}
    except Exception:
        # Never raise
        try:
            inputs = probe.get("inputs", [])
            return {"outputs": [str(x) for x in inputs]}
        except Exception:
            return {"outputs": []}
