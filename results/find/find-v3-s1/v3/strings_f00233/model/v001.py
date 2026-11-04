def predict(probe):
    # Mechanism inferred from all evidence:
    # 1) The entire input string is reversed character-by-character [E1, E2].
    #    "apple" -> "elppa" -> output "Elppa": reversal plus capitalization.
    # 2) After reversal, the string is title-cased in a specific way:
    #    the first character is uppercased, and every character that follows
    #    a space is uppercased; all other letters are lowercased [E1, E2].
    #    This matches "test case " -> reversed " esac tset" -> " esac tset"
    #    (leading space, then 'e' stays lower because it's not at start or
    #    after a space; 't' after space becomes 'T'? wait check).
    #
    # Let's verify the capitalization rule precisely.
    # E1: "test case " -> " esac tset"
    #   reversed: " esac tset"
    #   output:   " esac tset"
    #   Positions: 0=' ',1='e',2='s',3='a',4='c',5=' ',6='t',7='s',8='e',9='t'
    #   Output:    ' ','e','s','a','c',' ','t','s','e','t' -> no uppercase at all!
    #   So it's NOT "uppercase after space". The 't' after space stayed lower.
    #
    # E1: "data a Python " -> " nohtyp a atad"
    #   reversed: " nohtyp a atad"
    #   output:   " nohtyp a atad" -> all lowercase, no uppercase.
    #
    # E1: "test caseMiXeD" -> "Deximesac tset"
    #   reversed: "DeX iMesac tset"? Let's reverse "test caseMiXeD":
    #   t e s t   c a s e M i X e D
    #   reversed: D e X i M e s a c   t s e t
    #   = "DeXiMesac tset"
    #   output: "Deximesac tset"
    #   So 'D' stays upper, 'X' -> 'x', 'M' -> 'm', rest lower.
    #   Only the first character is uppercased; everything else lowercased?
    #   "DeXiMesac tset" -> first char 'D' upper, rest lower -> "Deximesac tset". Yes!
    #
    # E1: "Mississippi Hello World data" -> "Atad dlrow olleh ippississim"
    #   reversed: "atad dlrow olleh ippississiM"
    #   output:   "Atad dlrow olleh ippississim"
    #   First char 'a' -> 'A', rest lower. Yes!
    #
    # E2: "hello world" -> reversed "dlrow olleh" -> "Dlrow olleh". First char upper, rest lower. Yes.
    # E2: "Hello World" -> reversed "dlroW olleH" -> "Dlrow olleh". Yes.
    # E2: "one two three" -> reversed "eerht owt eno" -> "Eerht owt eno". Yes.
    # E2: "ab cd ef" -> reversed "fe dc ba" -> "Fe dc ba". Yes.
    # E2: "a b c" -> reversed "c b a" -> "C b a". Yes.
    # E2: "ABC def" -> reversed "fed CBA" -> "Fed cba". Yes.
    # E2: "  spaced  out  " -> reversed "  tuo  decaps  " -> output "  tuo  decaps  "
    #   First char is space, so no uppercase; rest lowercased. "  tuo  decaps  " already lower. Yes.
    # E2: "MiXeD CaSe" -> reversed "eSaC DeXiM" -> output "Esac dexim"
    #   First char 'e' -> 'E', rest lower: "Esac dexim". Yes!
    # E2: "123 abc" -> reversed "cba 321" -> "Cba 321". Yes.
    # E2: "xy" -> reversed "yx" -> "Yx". Yes.
    #
    # So the rule is: reverse the string, then capitalize the first character
    # (if it's a letter) and lowercase all remaining characters.
    # This is exactly Python's str.capitalize() applied to the reversed string.
    #
    # Check: "test case " reversed = " esac tset", capitalize() -> " esac tset" (first char is space, so no change; rest lower). Yes.
    # "data a Python " reversed = " nohtyp a atad", capitalize() -> " nohtyp a atad". Yes.
    #
    # So f(x) = x[::-1].capitalize()

    outputs = []
    for s in probe.get("inputs", []):
        try:
            outputs.append(s[::-1].capitalize())
        except Exception:
            outputs.append("")
    return {"outputs": outputs}
