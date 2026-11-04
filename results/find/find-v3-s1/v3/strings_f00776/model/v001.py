def predict(probe):
    # Rule: reverse the string, then swap case [E1]
    #   "apple" -> "elppa" -> "elWppa"? No: 'p'->'P'? Let's check.
    #   "apple" reversed = "elppa", swapcase = "ELPPA". Observed "elWppa".
    #   Hmm. Let's look again.
    # "apple" -> "elWppa". Reversed "elppa". Differences: e->e, l->l, p->W, p->p, a->a.
    # Wait maybe it's not swapcase. Let's recheck each.
    # "test case " -> " esacW tset". Reversed = " esac tset". Then 'c'->'W'? 
    # Actually " esac tset" vs " esacW tset": extra 'W' inserted? No...
    # Let's align: reversed("test case ") = " esac tset". Observed " esacW tset".
    #   Position: " esac" then "W" then " tset". So a 'W' inserted after "esac".
    # "apple" reversed = "elppa", observed "elWppa" -> 'W' inserted after "el".
    # "test caseMiXeD" reversed = "DeXiMesac tset", observed "DeXiMesWac tset" -> 'W' after "DeXiMes".
    # "data a Python " reversed = " nohtyP a atad", observed " nohtyPW a atad" -> 'W' after " nohtyP".
    # "test case Zebra" reversed = "arbeZ esac tset", observed "arbeZ eWsac tset" -> 'W' after "arbeZ e".
    # "Mississippi Hello World data" reversed = "atad dlroW olleH ippississiM", observed "atad dlroW ollWeH ippississiM" -> 'W' after "oll".
    # So: reverse the string, then insert 'W' at a specific position.
    # Where? "elppa"->"elWppa": after index 2 (0-based, before 'p' at index 2).
    # " esac tset"->" esacW tset": after index 5 (before ' ' at 5? " esac" is 5 chars, insert at 5).
    # "DeXiMesac tset"->"DeXiMesWac tset": "DeXiMes" is 7 chars, insert at 7.
    # " nohtyP a atad"->" nohtyPW a atad": " nohtyP" is 7 chars, insert at 7.
    # "arbeZ esac tset"->"arbeZ eWsac tset": "arbeZ e" is 7 chars, insert at 7.
    # "atad dlroW olleH ippississiM"->"atad dlroW ollWeH ippississiM": "atad dlroW oll" is 14 chars, insert at 14.
    # Hmm positions: 2, 5, 7, 7, 7, 14. Not constant.
    # Maybe insert 'W' before the first space? 
    #   "elppa": no space, insert at 2? 
    #   " esac tset": first space at 0, but W at 5. No.
    # Maybe insert 'W' at position = length of first word (before first space)?
    #   "elppa": first word "elppa" length 5, but W at 2. No.
    # Maybe insert before the last space?
    #   " esac tset": last space at 5, W at 5. Yes!
    #   "DeXiMesac tset": last space at 7, W at 7. Yes!
    #   " nohtyP a atad": last space at 7, W at 7. Yes!
    #   "arbeZ esac tset": last space at 7, W at 7. Yes!
    #   "atad dlroW olleH ippississiM": last space at 14, W at 14. Yes!
    #   "elppa": no space. W at 2. Hmm. Maybe insert at len//2? 5//2=2. Yes!
    # Check: if no space, insert at len//2.
    # Let's verify "elppa": len 5, 5//2=2, insert at 2 -> "elWppa". Yes!
    # So: reverse, then insert 'W' before the last space (or at len//2 if no space).
    # Wait, "before the last space" means at index of last space. Inserting at that index puts W before the space.
    # " esac tset": last space index 5, insert at 5 -> " esacW tset". Yes.
    # Actually wait, is it "before last space" or "after first word"? Let's just use last space index.
    # But what if multiple spaces? "a  b" reversed "b  a", last space at index 2, insert -> "b W a"? We don't know. Guess.
    # Also what about empty string? len 0, 0//2=0, insert at 0 -> "W". Guess.
    def transform(s):
        r = s[::-1]
        idx = r.rfind(' ')
        if idx == -1:
            idx = len(r) // 2
        return r[:idx] + 'W' + r[idx:]
    return {"outputs": [transform(x) for x in probe["inputs"]]}
