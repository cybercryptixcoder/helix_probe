def predict(probe):
    # Observations:
    # - Each space-separated word is reversed individually [E1,E2,E3,E4,E5,E6].
    # - Spaces are preserved in place (multiple spaces stay multiple) [E2,E4].
    # - Leading/trailing spaces are preserved [E1,E3,E4].
    # - Additionally, every character is duplicated (each char appears twice) [E1,E2,E3,E4,E5,E6].
    #   Wait: check. "apple" -> "eelppa": reversed only, not doubled.
    #   "test case " -> "tset esac": reversed only.
    #   But "test caseMiXeD" -> "tset DDeXiMesac": "MiXeD" reversed = "DeXiM",
    #     output has "DDeXiM" — the 'D' doubled? Actually "DeXiM" -> "DDeXiM": first char doubled.
    #   Hmm. Let's look at E2: "hello world" -> "olleh ddlrow". "world" reversed = "dlrow",
    #     output "ddlrow": 'd' doubled. "hello" reversed = "olleh" not doubled.
    #   "one two three" -> "eno owt eeerht": "three" reversed = "eerht", output "eeerht": 'e' doubled.
    #   "a b c" -> "a b cc": "c" -> "cc".
    #   "ab cd" -> "ba ddc": "cd" reversed = "dc", output "ddc": 'd' doubled.
    #   "hello  world" -> "olleh ddlrow": same as single space? Input has two spaces, output one space.
    #     Wait E2 "hello  world" (two spaces) -> "olleh ddlrow" (one space). Interesting.
    #   "hello world!" -> "olleh !!dlrow": "world!" reversed = "!dlrow", output "!!dlrow": '!' doubled.
    #   "Hello World" -> "olleH ddlroW": "World" reversed = "dlroW", output "ddlroW": 'd' doubled.
    #   "abc def ghi" -> "cba fed iihg": "ghi" reversed = "ihg", output "iihg": 'i' doubled.
    #   "x y z" -> "x y zz": "z" -> "zz".
    #   "test case" -> "tset eesac": "case" reversed = "esac", output "eesac": 'e' doubled.
    #
    # So: the LAST word gets its first character (after reversal) doubled.
    # First char after reversal = last char of original word.
    # Check E1 "apple" (single word) -> "eelppa": reversed "elppa", first char 'e' doubled -> "eelppa". Yes!
    # "test case " -> "tset esac": last word "case" reversed "esac", first char 'e' doubled -> "eesac"?
    #   But output is "esac" not "eesac". Hmm. Trailing space. So last word is empty?
    #   Then no doubling? Output "tset esac" — no doubling. Yes, trailing space means last token is "".
    # "test caseMiXeD" -> "tset DDeXiMesac": last word "caseMiXeD" reversed = "DeXiMesac",
    #   first char 'D' doubled -> "DDeXiMesac". Yes!
    # "data a Python " -> "atad a nohtyP": trailing space, last token empty, no doubling. Yes.
    # "test case Zebra" -> "tset esac aarbeZ": "Zebra" reversed "arbeZ", 'a' doubled -> "aarbeZ". Yes.
    # "Mississippi Hello World data" -> "... aatad": "data" reversed "atad", 'a' doubled -> "aatad". Yes.
    #
    # E3: "level123" -> "3321level": reversed "321level", '3' doubled -> "3321level". Yes.
    # "Python!@#" -> "##@!nohtyP": reversed "#@!nohtyP", '#' doubled -> "##@!nohtyP". Yes.
    # "banana" -> "aananab": reversed "ananab", 'a' doubled -> "aananab". Yes.
    # "racecar Zebra level" -> "racecar arbeZ llevel": last word "level" reversed "level",
    #   'l' doubled -> "llevel". Yes. Middle "Zebra" reversed "arbeZ" not doubled. Yes.
    # "racecar" -> "rracecar": reversed "racecar", 'r' doubled -> "rracecar". Yes.
    # "test case  " (two trailing spaces) -> "tset esac": last token empty, no doubling. Yes.
    #
    # E4: " leading space" -> "gnidael eecaps": tokens ["", "leading", "space"]. Last "space"
    #   reversed "ecaps", 'e' doubled -> "eecaps". Yes.
    # "trailing space " -> "gniliart ecaps": tokens ["trailing","space",""]. Last empty, no doubling. Yes.
    # "  two  spaces  " -> "owt secaps": Hmm. Input "  two  spaces  " (two leading, two between, two trailing).
    #   Output "owt secaps" — single spaces! That contradicts "spaces preserved".
    #   Wait E2 "hello  world" -> "olleh ddlrow" also single space. So multiple spaces collapse to one?
    #   But E4 "  padded  " -> "deddap": leading/trailing spaces gone entirely!
    #   And " leading space" -> "gnidael eecaps" leading space gone.
    #   Hmm, but E1 "test case " -> "tset esac" trailing space gone. "data a Python " -> trailing gone.
    #   E3 "test case  " -> "tset esac" trailing gone.
    #   So actually spaces are NOT preserved; they're normalized (split on whitespace, join with single space)?
    #   Check E1 "apple" -> "eelppa": single token, doubled first char. Yes.
    #   Let's re-examine: maybe the rule is: split on whitespace (any), reverse each token, double
    #   first char of LAST token, join with single space.
    #   E2 "a b c" -> "a b cc": tokens a,b,c -> a,b,cc. Yes.
    #   "hello  world" -> tokens hello, world -> olleh, ddlrow. Yes.
    #   E4 "  two  spaces  " -> tokens two, spaces -> owt, secaps (last 's'? wait).
    #     "spaces" reversed = "secaps", first char 's' doubled -> "ssecaps"? But output is "secaps".
    #     Hmm! Output "owt secaps" — no doubling on last token.
    #   Wait, "  two  spaces  " has trailing spaces. If we split on whitespace and drop empties,
    #     last token is "spaces", should be doubled. But it's not.
    #   Unless trailing whitespace matters: if input ends with whitespace, last token is empty -> no doubling.
    #   Let's check: "trailing space " ends with space -> no doubling. Yes.
    #   "  padded  " ends with space -> no doubling, output "deddap" (padded reversed). Yes.
    #   "  two  spaces  " ends with space -> no doubling. Output "owt secaps". Yes.
    #   "test case  " ends with space -> no doubling. Yes.
    #   "test case " ends with space -> no doubling. Yes.
    #   "data a Python " ends with space -> no doubling. Yes.
    #   " leading space" — starts with space but doesn't end with space. Last token "space",
    #     reversed "ecaps", 'e' doubled -> "eecaps". Output "gnidael eecaps". Yes!
    #   So: if input ends with whitespace, no doubling of last token. Otherwise double first char
    #     of last token after reversal.
    #   But also leading/multiple spaces collapse. So: split on whitespace, drop empties, reverse each,
    #     double first char of last (if input doesn't end with whitespace), join with single space.
    #   What if input is all whitespace? Then no tokens, output ""? Unknown but plausible.
    #
    # Check E4 "hello, world!" -> ",olleh !!dlrow": tokens "hello," and "world!".
    #   "hello," reversed = ",olleh". "world!" reversed = "!dlrow", '!' doubled -> "!!dlrow".
    #   Output ",olleh !!dlrow". Yes!
    # "123 456" -> "321 6654": "123"->"321", "456"->"654", '6' doubled -> "6654". Yes.
    # "abc" -> "ccba": reversed "cba", 'c' doubled -> "ccba". Yes.
    # "a b" -> "a bb": "b" -> "bb". Yes.
    # "one two  three" -> "eno owt eeerht": "three" reversed "eerht", 'e' doubled -> "eeerht". Yes.
    # "end." -> "..dne": reversed ".dne", '.' doubled -> "..dne". Yes.
    #
    # E5: " racecar" -> "rracecar": leading space, no trailing. Token "racecar" reversed "racecar",
    #   'r' doubled -> "rracecar". Yes.
    # "Mississippi" -> "iippississiM": reversed "ippississiM", 'i' doubled -> "iippississiM". Yes.
    # "function" -> "nnoitcnuf": reversed "noitcnuf", 'n' doubled -> "nnoitcnuf". Yes.
    # "racecar " -> "racecar": trailing space, no doubling. Yes.
    # "test case racecar" -> "tset esac rracecar": last "racecar" doubled 'r'. Yes.
    # "Example" -> "eelpmaxE": reversed "elpmaxE", 'e' doubled -> "eelpmaxE". Yes.
    #
    # E6: "a" -> "aa": reversed "a", 'a' doubled. Yes.
    # "ab" -> "bba": reversed "ba", 'b' doubled -> "bba". Yes.
    # "abc!" -> "!!cba": reversed "!cba", '!' doubled -> "!!cba". Yes.
    # "Hello!" -> "!!olleH": reversed "!olleH", '!' doubled -> "!!olleH". Yes.
    # "x1" -> "11x": reversed "1x", '1' doubled -> "11x". Yes.
    # "1a" -> "aa1": reversed "a1", 'a' doubled -> "aa1". Yes.
    # "a1b2" -> "22b1a": reversed "2b1a", '2' doubled -> "22b1a". Yes.
    # "Zz" -> "zzZ": reversed "zZ", 'z' doubled -> "zzZ". Yes.
    # "hi there!" -> "ih !!ereht": "there!" reversed "!ereht", '!' doubled -> "!!ereht". Yes.
    # "end?" -> "??dne": reversed "?dne", '?' doubled -> "??dne". Yes.
    #
    # Great, the model is consistent across all evidence.

    def transform(s):
        tokens = s.split()
        if not tokens:
            return ""
        rev = [t[::-1] for t in tokens]
        if not s[-1:].isspace():
            rev[-1] = rev[-1][0] + rev[-1] if rev[-1] else rev[-1]
        return " ".join(rev)

    return {"outputs": [transform(x) for x in probe["inputs"]]}
