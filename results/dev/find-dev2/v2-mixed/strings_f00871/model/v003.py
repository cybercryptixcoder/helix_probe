def predict(probe):
    # Reverse the whole string, then append "I" [E1, E2, E3]
    # "a b c" -> "a b cI" is consistent with full reversal? No: reversed is "c b a".
    # But note "a b c" reversed = "c b a", observed "a b cI". So NOT full reversal there.
    # However "test case" -> "tset esacI": that IS full reversal ("esac tset" reversed).
    # Wait: "test case" reversed = "esac tset". Observed "tset esac". That's word-order kept, each word reversed!
    # Recheck E2: "dog house" -> "god esuohI": each word reversed, order kept. Yes!
    # "OpenAI" -> "IAnepOI": single word reversed. Yes.
    # "test 123" -> "tset 321I": each word reversed. Yes.
    # "a b c" -> "a b cI": each word reversed (single chars unchanged). Yes!
    # E1: "Hello World function lazy" -> "olleH dlroW noitcnuf yzalI": each word reversed. Yes!
    # " Zebralower" -> "rewolarbeZI": leading space preserved, word reversed. Yes!
    # E3: "banana data banana " -> "ananab atad ananabI": trailing space dropped? 
    #   Observed "ananab atad ananabI" — trailing space gone. Hmm, or split/join drops it.
    #   "test case" -> "tset esacI" no trailing space issue.
    # So: reverse each word individually, keep word order, join with single spaces, append "I".
    # Trailing/leading spaces: " Zebralower" kept leading space -> "rewolarbeZI" (space + reversed).
    #   So leading space preserved. "banana data banana " trailing space dropped.
    #   Likely: split on spaces, reverse each token, rejoin with " ". split(" ") keeps empties though.
    #   " Zebralower".split(" ") = ["", "Zebralower"] -> join "" + " " + "rewolarbeZ" = " rewolarbeZ". Matches!
    #   "banana data banana ".split(" ") = ["banana","data","banana",""] -> "ananab atad ananab " -> trailing space.
    #   But observed no trailing space. So maybe rstrip or split() default.
    #   " Zebralower" with split() default = ["Zebralower"] -> "rewolarbeZ", loses leading space. Contradicts.
    #   So leading space kept, trailing dropped. Use split(" ") then rstrip trailing empty? 
    #   Or: reverse each word, join with " ", then rstrip? "ananab atad ananab " rstrip -> "ananab atad ananab". Yes.
    #   But " rewolarbeZ" rstrip keeps leading. Good.
    # Rule: split on " ", reverse each token, join with " ", rstrip, append "I".
    out = []
    for s in probe.get("inputs", []):
        try:
            parts = s.split(" ")
            rev = " ".join(p[::-1] for p in parts)
            rev = rev.rstrip()
            out.append(rev + "I")
        except Exception:
            out.append("I")
    return {"outputs": out}
