def predict(probe):
    # f(s): split s on whitespace into tokens t1..tn.
    # Output = rev(t1) + " " + rev(t2 + t3 + ... + tn)  [E2,E3,E4,E5,E6]
    # First word reversed, remaining words concatenated (spaces removed) then reversed.
    # Single word: just rev(word). [E1]
    # Leading/trailing/multiple spaces collapsed by split(). [E1,E2]
    # Consecutive duplicate chars are collapsed AFTER reversing, per segment. [E7]
    #   "aabb"->rev="bbaa"->collapse="ba" [E7]; "abba"->rev="abba"->collapse="aba"?
    #   BUT observed "abba"->"ba". So collapse happens BEFORE reversing!
    #   Check: "abba" collapse="aba" rev="aba"? no. collapse before rev of "abba" = "aba",
    #   rev="aba" != "ba". Hmm.
    #   Reconsider: "abba"->"ba". rev("abba")="abba". Collapse consecutive dups in
    #   reversed = "aba". Not "ba". 
    #   What gives "ba"? Maybe collapse dups in ORIGINAL then reverse: "abba"->"aba"->"aba". No.
    #   Maybe collapse ALL duplicate letters (not just consecutive)? "abba"->"ab"->rev="ba" ✓
    #   Check "aabb"->dedup all="ab"->rev="ba" ✓
    #   "bbaacc"->dedup="bac"->rev="cab" ✓
    #   "hello"->dedup="helo"->rev="oleh" ✓
    #   "helloo"->dedup="helo"->rev="oleh" ✓
    #   "xxyyzz"->dedup="xyz"->rev="zyx" ✓
    #   "bookkeeper"->dedup="bokeper"->rev="repekob"? observed "rpekob". 
    #     "bookkeeper" letters: b,o,o,k,k,e,e,p,e,r -> dedup keeping first: b,o,k,e,p,r = "bokepr"
    #     rev="rpekob" ✓ (I miscounted; only one 'e' kept after p? "bookkeeper"=b o o k k e e p e r,
    #     dedup: b,o,k,e,p,r -> "bokepr", rev="rpekob" ✓)
    #   So: remove duplicate letters (keep first occurrence), then reverse. [E7]
    #   Check first-word vs rest-block: "aabb cc"->first "aabb"->"ab"->rev "ba"; rest "cc"->"c"->rev "c" ✓
    #   "aabb cc dd"->"ba"+" "+rev("cd")="dc" -> "ba dc" ✓
    #   "abba cd"->first "abba"->"ab"->rev "ba"; rest "cd"->rev "dc" -> "ba dc" ✓
    #   E1 "hello"->"oleh" ✓; "world"->"dlrow" ✓; "two words"->"owt"+" "+rev("words")="sdrow" ✓
    #   E1 "spaces"->dedup "spaces"(s,p,a,c,e,s -> s,p,a,c,e)="space"->rev="ecaps" ✓
    #   E1 "The quick brown fox"->first "The"->"The"->rev "ehT"; rest "quickbrownfox"
    #     dedup: q,u,i,c,k,b,r,o,w,n,f,x (no dups) -> rev "xfnworbkciuq" -> "ehT xfnworbkciuq" ✓
    #   E1 "test"->"test"->rev "tset"? observed "set". dedup "test"->t,e,s="tes"->rev="set" ✓
    #   E2 "one two three"->first "one"->rev "eno"; rest "twothree"->dedup t,w,o,h,r,e="twohre"
    #     rev="erhwot"? observed "rhwt". Hmm mismatch. 
    #     "twothree" letters t,w,o,t,h,r,e,e -> dedup: t,w,o,h,r,e = "twohre" rev="erhwot".
    #     Observed "rhwt". Doesn't match. Truncation? "rhwt" is rev of "twhr"? 
    #     Maybe dedup is applied to reversed? rev("twothree")="eerhtowt" dedup="erhtow" no.
    #     Uncertain — mark "?" and use dedup-then-reverse as best guess.
    #   E3 "sun moon star"->first "sun"->rev "nus"; rest "moonstar"->dedup m,o,n,s,t,a,r="monstar"
    #     rev="ratsnom"? observed "ratom". Mismatch — truncation "?".
    #   E5 "big red dog"->first "big"->rev "gib"; rest "reddog"->dedup r,e,d,o,g="redog"
    #     rev="goder"? observed "oder". Mismatch.
    #   These multi-word "rest" cases are inconsistent; many look truncated. Best guess:
    #   dedup-then-reverse on the concatenated rest. Mark "?".
    out = []
    for s in probe.get("inputs", []):
        try:
            toks = s.split()
            if not toks:
                out.append("")
                continue
            def dedup(x):
                seen = set()
                r = []
                for c in x:
                    if c not in seen:
                        seen.add(c)
                        r.append(c)
                return "".join(r)
            first = dedup(toks[0])[::-1]
            if len(toks) == 1:
                out.append(first)
            else:
                rest = dedup("".join(toks[1:]))[::-1]
                out.append(first + " " + rest)
        except Exception:
            out.append("")
    return {"outputs": out}
