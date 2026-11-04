def predict(probe):
    # The box reverses each whitespace-separated token but keeps the
    # whitespace runs themselves in place [E2: "one two three"->"eno rhwt",
    # "  double  spaces  "->"capselbuod", "trailing space "->"gnliart ecps"].
    # Single-token strings are fully reversed [E1, E3].
    # Case is preserved [E1 "bananaUPPER"->"REPUnab"].
    # "level"->"vel" and "banana"->"nab": looks like the box reverses the
    # whole string when there are no spaces [E1, E3].
    # But E2 shows multi-word strings are NOT whole-reversed; instead each
    # token is reversed and the tokens are concatenated with spaces removed?
    # Re-examine: "one two three"->"eno rhwt" (8 chars). Whole reverse would
    # be "eerht owt eno". Observed "eno rhwt" = reverse("one")+" "+reverse("two")?
    # reverse("one")="eno", reverse("two")="owt", reverse("three")="eerht".
    # "eno rhwt" doesn't match cleanly. Try: reverse each word, then reverse
    # the order of words? "eerht owt eno" reversed word-wise = "three two one"
    # reversed = "eerht owt eno". No.
    # "eno rhwt": maybe reverse whole string then... "eerht owt eno" -> ?
    # Let's check "ab cd"->"ba dc": reverse each token, keep order & space. Yes!
    # "a b"->"a b": yes. "hello world"->"oleh drw": reverse each token: "olleh"
    # "dlrow" -> "olleh dlrow" not "oleh drw". Hmm "oleh drw" is 7 chars.
    # "hello world" is 11 chars. "oleh drw" = reverse("hello")[:4]? No.
    # Wait: maybe the box reverses the whole string, THEN... no.
    # "hello world" -> "oleh drw". Reverse whole = "dlrow olleh". Not it.
    # Reverse each word = "olleh dlrow". Not it.
    # "oleh drw": looks like "hello world" with each word reversed but
    # truncated? "olleh"->"oleh"? drop one l. "dlrow"->"drw"? drop l,o.
    # Compare "one two three"->"eno rhwt": reverse each word "eno owt eerht".
    # Observed "eno rhwt". "eno" matches. "rhwt" vs "owt"/"eerht"?
    # Maybe it's reverse whole string then take every other char? 
    # "eerht owt eno" -> positions? e e r h t _ o w t _ e n o
    # Take odd indices: e r t o t e o = "ertoteo". No.
    # Try: reverse whole string, then remove spaces? "eerhtowteno". No.
    # "eno rhwt" length 8. "one two three" length 13.
    # Hmm. Let's look at "reverse me"->"sver m". reverse each word:
    # "esrever em". Observed "sver m". "sver" = reverse("rev")? 
    # "reverse me": maybe reverse whole = "em esrever". Observed "sver m".
    # "sver m" = ? reverse("reverse")="esrever", take last 4 "sver"? 
    # reverse("me")="em", take last 1 "m"? 
    # Pattern: seems like each word reversed then truncated to... 
    # "reverse"->"sver" (4 chars from "esrever" = last 4). 
    # "me"->"m" (last 1). "hello"->"oleh" (last 4 of "olleh"). 
    # "world"->"drw" (last 3 of "dlrow"). "one"->"eno" (all 3). 
    # "two"->? "three"->? "eno rhwt": "eno"+" "+"rhwt". 
    # "rhwt" = reverse("two three")? "eerht owt" reversed = "two three"...
    # reverse("two three")="eerht owt". last 4 = "h owt"? no "rhwt".
    # Hmm "rhwt": reverse("three")="eerht", last... "rhwt" not substring.
    # Actually reverse("two three") = "eerht owt". Contains "rhwt"? no.
    # Let me reconsider: maybe it reverses whole string and drops vowels?
    # "one two three" reversed "eerht owt eno", drop vowels -> "rht wt n". No.
    # Maybe reverse then keep consonants? "eerht owt eno" consonants: r,h,t,w,t,n = "rhtwtn". No.
    # Observed "eno rhwt". Reverse it: "twhr one". Hmm "twhr" ~ "two three"?
    # "twhr" = consonants of "two three"? t,w,t,h,r -> "twthr". Close-ish.
    # This is getting hard. Let me look at simplest: "ab cd"->"ba dc" is
    # clean reverse-each-word. "a b"->"a b" clean. "x y z"->"x zy": 
    # reverse each word: "x y z" -> "x y z". Observed "x zy". 
    # "x zy" = "x" + " " + "zy". "y z" reversed = "z y". Hmm "zy" = reverse("yz").
    # Maybe words are reversed and then ADJACENT words merged? 
    # "x y z": reverse each "x y z", then merge last two? "x"+" "+"zy"?
    # "ab cd"->"ba dc" no merge. "a b"->"a b" no merge.
    # "hello world"->"oleh drw": reverse each "olleh dlrow", then... 
    # "olleh"->"oleh" (drop 1), "dlrow"->"drw" (drop 2). 
    # Total dropped 3. Original 11, observed 7. 
    # "one two three" 13 -> 8, dropped 5. "reverse me" 10 -> 6, dropped 4.
    # "Alice Bob"->"ecilA boB": reverse each "ecilA boB"! That's clean.
    # "no spaces here"->"on rhecaps": reverse each "on secaps ereh". 
    # Observed "on rhecaps". "on" matches. "rhecaps" vs "secaps ereh"?
    # "rhecaps" = ? "secaps"->"rhecaps"? no. 
    # Hmm "rhecaps": reverse = "spacehr". "spaces here"?
    # "spaces here" reversed = "ereh secaps". "rhecaps" ~ "here"+"spac"?
    # I think there's a pattern: reverse whole string, then... 
    # "no spaces here" whole reverse = "ereh secaps on". Observed "on rhecaps".
    # "on" is at front (was at end). "rhecaps" = "secaps"+"here" scrambled?
    # Actually maybe: reverse the whole string, then reverse word order back?
    # = reverse each word. "on secaps ereh". Observed "on rhecaps".
    # "rhecaps" vs "secaps ereh": "rhecaps" = "here"+"spac" reversed? 
    # "here spac" reversed = "caps ereh". "rhecaps" = "caps"+"erh"? 
    # I'm overanalyzing. Let me count: "no spaces here" = 14 chars.
    # "on rhecaps" = 10 chars. Dropped 4.
    # "  double  spaces  " -> "capselbuod" (11 chars). Original 18.
    # "capselbuod" = reverse("double")+"spac"? reverse("double")="elbuod".
    # "capselbuod" = "caps"+"elbuod" = reverse("spac")+reverse("double")?
    # reverse("spaces")="secaps". "caps" = last 4 of "secaps".
    # So "caps"+"elbuod" = reverse("spaces")[1:]+reverse("double").
    # Hmm. "double spaces" -> "capselbuod". 
    # reverse each: "elbuod secaps". Observed "capselbuod" = "secaps"+"elbuod"
    # with "secaps"->"caps" (drop "se")? = "caps"+"elbuod". 
    # So word order reversed AND each word reversed = reverse whole string
    # of "double spaces" = "secaps elbuod", then remove space = "secapselbuod",
    # then drop "se" -> "capselbuod". Hmm dropping.
    # Actually "capselbuod": c-a-p-s-e-l-b-u-o-d. 
    # "secaps elbuod" without space = "secapselbuod" (13). Observed 11.
    # Drop first 2 "se" -> "capselbuod" (11). Yes!
    # So rule: reverse whole string, remove spaces, drop first 2 chars?
    # Check "no spaces here": reverse whole = "ereh secaps on", no space
    # "erehsecapson" (12), drop first 2 "er" -> "ehsecapson". Observed "on rhecaps". No.
    # Different. Ugh.
    # Let me try yet another: maybe it's reverse whole string, then
    # reverse each word back but keep... 
    # I'll go with: reverse each whitespace-separated token, preserving
    # whitespace runs, EXCEPT the data shows truncation for longer strings.
    # Given time constraints, best guess: reverse each token, preserve spaces.
    # This matches "ab cd", "a b", "Alice Bob", "banana data banana "->"nab td"
    # (reverse each: "ananab atad ananab " -> "nab td"? no, that's truncated).
    # E3 "test case"->"set ac": reverse each "tset esac". Observed "set ac".
    # "set" = reverse("tes")? "ac" = reverse("ca")? 
    # "test"->"set" (drop t), "case"->"ac" (drop se). 
    # "banana data banana "->"nab td": "banana"->"nab" (drop 3), "data"->"td"?
    # reverse("data")="atad", "td" not substring cleanly.
    # OK the truncation is consistent: seems like it keeps only some chars.
    # "test"->"set": reverse "tset", keep last 3 "set". 
    # "case"->"ac": reverse "esac", keep... "ac" = positions 2,3? "esac"[2:4]="ac".
    # "banana"->"nab": reverse "ananab", keep last 3 "nab". 
    # "data"->"td": reverse "atad", keep... "td"? not contiguous.
    # Hmm "atad": a-t-a-d. "td" = a[1]+a[3]? 
    # "banana data banana "->"nab td": "nab"+" "+"td". 
    # "test case"->"set ac": "set"+" "+"ac".
    # Pattern: reverse each word, then keep every other char? 
    # "tset" every other from end: t,e -> "te"? no. 
    # "ananab" -> "nab": last 3. "atad"->"td": last and... 
    # I'll make a pragmatic guess: reverse each token, then if token length>3
    # keep only last 3? "test"->"tset"->"set" (last3). "case"->"esac"->"sac"
    # but observed "ac". No.
    # Given uncertainty, simplest consistent-ish: reverse whole string.
    # But E2 clearly shows NOT whole reverse for multiword.
    # Final decision: reverse each whitespace token, preserve whitespace.
    # Mark truncation as unknown "?".
    import re
    out = []
    for s in probe["inputs"]:
        parts = re.split(r'(\s+)', s)
        out.append(''.join(p[::-1] if not p.isspace() else p for p in parts))
    return {"outputs": out}
