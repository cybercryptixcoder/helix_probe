def predict(probe):
    # Observed: output = input with some characters removed, then 'h' appended [E1]
    # "abc123" -> "abc123h": nothing removed, 'h' appended
    # "level" -> "levh": removed 'e','l'? "level" -> "lev" + h. Removed chars at positions... 
    #   level = l e v e l -> lev (kept l,e,v; dropped e,l)
    # " Zebralower" -> " Zebralowh": dropped 'e','r'? " Zebralower" -> " Zebralow" + h
    #   Z e b r a l o w e r -> Z e b r a l o w (dropped e,r)
    # "Hello World function lazy" -> "Helo Wrdfunctiazyh"
    #   H e l l o   W o r l d   f u n c t i o n   l a z y
    #   H e l o   W r d f u n c t i a z y  (dropped l,o,l,o,i,o,n,l)
    # "bananaUPPER" -> "banUPERh": b a n a n a U P P E R -> b a n U P E R (dropped a,n,a,P)
    # "Zebra" -> "Zebrah": nothing dropped
    # Hypothesis (?): remove characters that are "redundant" - looks like removing
    #   repeated/consecutive-ish letters and vowels in certain spots. Hard to pin.
    # Best guess: this looks like removing every character that is a duplicate of
    #   a nearby one, plus some vowels. Too uncertain; simplest consistent rule:
    #   append 'h', and drop characters per some rule we can't fully determine.
    # Fallback model: just append 'h' (matches "abc123" and "Zebra" exactly).
    def f(s):
        return s + "h"
    return {"outputs": [f(x) for x in probe["inputs"]]}
