def predict(probe):
    # Rule: split input at the midpoint (floor), reverse each half, join with "2" [E1]
    # "apple" (5) -> "ap"+"ple" -> "pa"+"elp" -> "pa2elp"? No: observed "elp2pa"
    # Let's check: "apple" -> halves "ap","ple" reversed: "pa","elp" -> "pa2elp" != "elp2pa"
    # Try: reverse whole string then insert "2" at midpoint? "apple"->"elppa", mid=2 -> "el"+"p"+"pa"? no
    # Observed "elp2pa": left="elp", right="pa". "apple" reversed = "elppa". split at 3: "elp","pa". yes!
    # "test case " (10) reversed = " esac tset", split at 5: " esac"," tset" -> " esac2 tset" ✓
    # So: reverse string, insert "2" at position floor(len/2)? For len 10 -> 5. " esac tset" split at 5 = " esac"," tset" ✓
    # "apple" len 5, reversed "elppa", split at 3? floor(5/2)=2 gives "el","ppa". But observed split at 3.
    # ceil(5/2)=3. len10 ceil=5. So split at ceil(len/2).
    # "test caseMiXeD" len 14 reversed "DeXiMes2ac tset"? wait that has 2 already... 
    # reversed of "test caseMiXeD" = "DeXiMesac tset". ceil(14/2)=7 -> "DeXiMes","ac tset" -> "DeXiMes2ac tset" ✓
    # "data a Python " len 14 reversed " nohtyP a atad", ceil=7 -> " nohtyP"," a atad" -> " nohtyP2 a atad" ✓
    # "test case Zebra" len 15 reversed "arbeZ esac tset", ceil(15/2)=8 -> "arbeZ es","ac tset" -> "arbeZ es2ac tset" ✓
    # "Mississippi Hello World data" len 28 reversed "atad dlroW olleH ippississiM", ceil=14 -> "atad dlroW oll","eH ippississiM"? 
    #   observed "atad dlroW oll2eH ippississiM" ✓ (split at 14)
    import math
    out = []
    for s in probe["inputs"]:
        r = s[::-1]
        k = (len(r) + 1) // 2
        out.append(r[:k] + "2" + r[k:])
    return {"outputs": out}
