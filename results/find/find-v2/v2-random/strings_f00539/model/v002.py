def predict(probe):
    # Output = input with certain characters removed, then 'h' appended [E1, E2]
    # "abc123"->"abc123h", "Zebra"->"Zebrah", "lazy"->"lazyh", "Example123"->"Example123h": nothing removed [E1,E2]
    # "level"->"levh": removed the 2nd 'e' and last 'l' [E1,E2]
    # "banana"->"banh": removed a,n,a,n,a -> kept "ban" [E2]
    # "bananaUPPER"->"banUPERh": kept b,a,n,U,P,E,R (removed a,n,a,P) [E1]
    # "banana data banana "->"ban dth": kept b,a,n,space,d,t (removed a,n,a,space,d,a,t,a,space,b,a,n,a,space) [E2]
    # "test case"->"tes cah": kept t,e,s,space,c,a (removed t,space,c,s,e) [E2]
    # "Hello World function lazy"->"Helo Wrdfunctiazyh" [E1]
    # " Zebralower"->" Zebralowh" [E1]
    # Hypothesis (?): remove characters that already appeared earlier in the string
    #   (keep only first occurrence of each character). Check:
    #   "level": l,e,v,(e dup),(l dup) -> "lev" ✓
    #   "banana": b,a,n,(a dup),(n dup),(a dup) -> "ban" ✓
    #   "bananaUPPER": b,a,n,(a),(n),(a),U,P,(P dup),E,R -> "banUPER" ✓
    #   "test case": t,e,s,(t dup),space,c,a,(s dup),(e dup) -> "tes ca" ✗ (observed "tes cah")
    #   Hmm "tes cah" vs "tes ca"+"h" = "tes cah"! Wait output is "tes cah" which is "tes ca"+"h" ✓
    #   "banana data banana ": b,a,n,(a),(n),(a),space,d,(a),(t),(a),space,(b),(a),(n),(a),space
    #     -> "ban dt" + h = "ban dth" ✓
    #   "Hello World function lazy": H,e,l,(l),o,space,W,(o),r,(l),d,space,f,(u),n,c,(t),(i),o,(n),space,(l),a,z,y
    #     -> "Helo Wrdfunc tio..." let's be careful:
    #     H,e,l,l,o,' ',W,o,r,l,d,' ',f,u,n,c,t,i,o,n,' ',l,a,z,y
    #     keep first: H,e,l,(l dup),o,' ',W,(o dup),r,(l dup),d,' ',f,u,n,c,t,i,(o dup),(n dup),' ',(l dup),a,z,y
    #     -> "Helo Wrdfuncti azy" = "Helo Wrdfunctiazy" ✓
    #   " Zebralower": ' ',Z,e,b,r,a,l,o,w,(e dup),r dup -> " Zebralow" ✓
    #   "Example123": E,x,a,m,p,l,e dup,1,2,3 -> "Exampl123"? but observed "Example123h" (nothing removed)
    #     Wait "Example" = E,x,a,m,p,l,e. 'e' at end vs 'E' at start - case differs! So no dup. ✓
    #   "lazy": l,a,z,y all distinct ✓
    #   "abc123": all distinct ✓
    #   "Zebra": Z,e,b,r,a all distinct ✓
    # Rule: keep only first occurrence of each character (case-sensitive), append 'h' [E1,E2]
    def f(s):
        seen = set()
        out = []
        for ch in s:
            if ch not in seen:
                seen.add(ch)
                out.append(ch)
        return "".join(out) + "h"
    return {"outputs": [f(x) for x in probe["inputs"]]}
