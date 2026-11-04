def predict(probe):
    # Observations: "test case"->"set ac", "banana data banana "->"nab td", "banana"->"nab", "level"->"vel"
    # So the box reverses each word individually, keeping word order and single spaces [E2]
    # "abc123"->"321cba", "Example123"->"321elpmaxE": single word reversed [E1, E2]
    # " Zebralower"->"wolarbeZ": leading space dropped, word reversed [E1]
    # "Hello World function lazy"->"oleH yzaitcnufdrW": hmm this looks like words reversed
    #   "Hello"->"oleH", "World"->"drW"? no... let's check: "oleH yzaitcnufdrW"
    #   Actually "Hello World function lazy" reversed word-by-word would be "olleH dlroW noitcnuf yzal"
    #   Observed "oleH yzaitcnufdrW" - that's "Hello"->"oleH" (reversed), then "World function lazy"?
    #   "yzaitcnufdrW" reversed = "Wrdfunction..." no. Let's reverse "yzaitcnufdrW" = "Wrdfunction"?
    #   y z a i t c n u f d r W -> reversed W r d f u n c t i a z y = "Wrdfunctiazy"? no
    #   Hmm. "World function lazy" -> maybe reverse whole then... 
    #   Let me reconsider: "Hello World function lazy" -> "oleH yzaitcnufdrW"
    #   Split: "oleH" + " " + "yzaitcnufdrW". Second part reversed = "Wrdfunction"?
    #   W-r-d-f-u-n-c-t-i-a-z-y reversed chars: y z a i t c n u f d r W
    #   So "yzaitcnufdrW" reversed = "Wrdfunction"? that's W r d f u n c t i o n? no
    #   Let me carefully reverse "yzaitcnufdrW": W,r,d,f,u,n,c,t,i,a,z,y -> "Wrdfunctiazy"
    #   Not matching. Maybe it's not full reverse.
    #   Alternative: reverse each word but only some? "Hello"->"oleH" yes reversed.
    #   "World function lazy" -> "yzaitcnufdrW"? 
    #   "lazy"->"yzal", "function"->"noitcnuf", "World"->"dlroW"
    #   "yzaitcnufdrW"... contains "yz" (lazy start), "aitcnuf" (function middle?), "drW"
    #   Hmm "yzal"+"noitcnuf"+"dlroW" concatenated = "yzalnoitcnufdlroW" no.
    #   Actually maybe words are reversed AND order reversed? "lazy function World" -> reverse each: "yzal noitcnuf dlroW"
    #   Observed "yzaitcnufdrW" - no spaces, and letters: y z a i t c n u f d r W
    #   "yzal" + "noitcnuf" + "dlroW" with spaces removed and... "yzalnoitcnufdlroW" vs "yzaitcnufdrW"
    #   Not it. Let me try: reverse whole string "Hello World function lazy" = "yzal noitcnuf dlroW olleH"
    #   Observed "oleH yzaitcnufdrW". 
    #   "oleH" = reverse of "Hello". Then " " then "yzaitcnufdrW".
    #   "yzaitcnufdrW" - if we reverse = "Wrdfunctiazy". Hmm.
    #   Maybe: split into words, reverse word order, reverse each word, but drop some?
    #   words: Hello, World, function, lazy. reversed order: lazy, function, World, Hello
    #   reverse each: yzal, noitcnuf, dlroW, olleH -> "yzal noitcnuf dlroW olleH"
    #   Observed: "oleH yzaitcnufdrW" -> "oleH" then "yzaitcnufdrW"
    #   "yzaitcnufdrW" = "yzal"+"noitcnuf"+"dlroW" merged? yzalnoitcnufdlroW vs yzaitcnufdrW
    #   yzalnoitcnufdlroW
    #   yzaitcnufdrW
    #   Compare: y z a l n o i t c n u f d l r o W
    #            y z a i t c n u f d r W
    #   Missing: l, n, o, l, o ... hmm seems like every other? 
    #   y z a [l] [n] o i t c n u f [d] [l] r o W -> no
    #   Actually: yzaitcnufdrW. Let's see "yzal"->"yza"? then "noitcnuf"->"itcnuf"? then "dlroW"->"drW"?
    #   "yzal" drop 'l' = "yza". "noitcnuf" drop "no" = "itcnuf". "dlroW" drop "lo" = "drW"? no "dlroW" drop 'l','o' = "drW". 
    #   Hmm inconsistent. This is getting complex. Let me focus on simpler evidence.
    # Simpler: E2 all words <= single word or two words. "test case"->"set ac": "test"->"set" (reversed), "case"->"ac" (reversed "esac" but only "ac"?) 
    #   "case" reversed = "esac", observed "ac". So dropped "es"? 
    #   "banana data banana "->"nab td": "banana"->"nab", "data"->"td"? "data" reversed "atad", observed "td"
    #   "banana"->"nab": reversed "ananab", observed "nab". 
    #   So it seems only first 3 chars of reversed word? "ananab"->"nab" (first 3). "esac"->"esa"? but observed "ac". Hmm.
    #   "atad"->"ata"? observed "td". no.
    #   Wait "banana"->"nab": that's reverse then take... "ananab" first 3 = "ana" no. Last 3 = "nab" yes!
    #   "esac" last 3 = "sac" no, observed "ac" (2 chars). 
    #   "atad" last 3 = "tad" no, observed "td".
    #   Hmm. "level"->"vel": reverse "level"="level", last 3 = "vel" yes!
    #   "lazy"->"yzal": reverse="yzal", last 3="zal"? observed "yzal" full. 
    #   "banana"->"nab": reverse "ananab", last 3 "nab" yes.
    #   "test"->"set": reverse "tset", last 3 "set" yes!
    #   "case"->"ac": reverse "esac", last 3 "sac" no. observed "ac". Hmm 2 chars.
    #   "data"->"td": reverse "atad", last 3 "tad" no. observed "td".
    #   "Example123"->"321elpmaxE": full reverse, 10 chars. So not always last 3.
    #   "abc123"->"321cba": full reverse 6 chars.
    #   "Zebra"->"arbeZ": full reverse 5 chars.
    #   "bananaUPPER"->"REPUnab": reverse "REPUnanab", observed "REPUnab" = first 7? "REPUnab" yes first 7 of "REPUnanab".
    #   Hmm. "bananaUPPER" reverse = "REPUnanab". observed "REPUnab". That's "REPU"+"nab". 
    #   "banana"->"nab" = last 3 of reverse "ananab". 
    #   "bananaUPPER"->"REPUnab": reverse "REPUnanab", take first 4 "REPU" + last 3 "nab"? = "REPUnab" yes!
    #   "banana data banana "->"nab td": "banana"->"nab" (last3 of reverse), "data"->"td"? reverse "atad" first? last? "td" = first+last? a...d -> "td"? no.
    #   Hmm "data" reverse "atad". "td" could be... a-t-a-d, take t and d? 
    #   This is getting too speculative. Let me reconsider entirely.
    # Maybe it's: reverse the string, then remove vowels? 
    #   "test case" reverse = "esac tset". remove vowels (a,e,i,o,u) = "sc tst". observed "set ac". no.
    # Maybe reverse each word, then remove vowels?
    #   "test"->"tset" remove e = "tst". observed "set". no.
    # Let me look: "test case"->"set ac". "test"->"set", "case"->"ac".
    #   "test" reversed "tset", remove 't'? "set". "case" reversed "esac" remove "es"? "ac".
    #   Hmm remove first char of reversed? "tset"->"set" yes. "esac"->"sac" no.
    #   remove vowels from reversed: "tset"->"tst" no.
    #   "set" = "test" with t removed from front and... "test"->"set": remove first 't'? "est"? no.
    #   "test" sorted? no.
    # OK "banana"->"nab", "level"->"vel", "lazy"->"yzal", "test"->"set", "case"->"ac", "data"->"td"
    #   "level"->"vel": remove first 2 chars "le" -> "vel". 
    #   "banana"->"nab": remove first 3 "ban" -> "ana"? no. remove last 3 "ana"->"ban"? no.
    #   Hmm "banana"->"nab" = chars at positions? b(0)a(1)n(2)a(3)n(4)a(5). "nab" = n,a,b = positions 4,3,0? 
    #   "level"->"vel": l(0)e(1)v(2)e(3)l(4). "vel"=v,e,l=positions 2,3,4.
    #   "lazy"->"yzal": y,z,a,l = positions 1,2,0,3? 
    #   "test"->"set": s,e,t = positions 2,1,0.
    #   "case"->"ac": a,c = positions 1,0.
    #   "data"->"td": t,d = positions 2,3.
    #   Inconsistent. 
    # Given complexity and time, the safest general rule that fits many: reverse each word, keep word order, single spaces. This fits E1 "abc123","level"->"vel"? no level reversed is "level" not "vel".
    # Hmm "level"->"vel" is definitely not full reverse.
    # Wait maybe it's: reverse, then remove duplicate consecutive? "level" reverse "level", remove dup consecutive: l,e,v,e,l -> "level" no dup. 
    # "banana" reverse "ananab", remove dup: a,n,a,n,a,b -> "ananab" no consecutive dup.
    # Maybe remove vowels? "level"->"lvl"? no.
    # "level"->"vel": could be reverse then take middle? "level" middle 3 = "eve"? no.
    # I'll go with: reverse each word, then remove vowels? test: "level" reverse "level" remove vowels e,e = "lvl". no.
    # Given uncertainty, best guess: reverse each word individually, keep spaces/word order. This matches "abc123","Example123","Zebra","lazy","Hello"->"oleH". Fails "level"->"vel" and others but those are odd.
    # Actually wait: maybe it reverses the whole string but the "words" evidence... "test case" full reverse = "esac tset". observed "set ac". Not full.
    # Let me try: reverse each word, then remove first and last char? "test"->"tset"->"se". no.
    # I'll commit to word-by-word reversal as best hypothesis, noting uncertainty.
    out = []
    for s in probe.get("inputs", []):
        try:
            words = s.split(" ")
            out.append(" ".join(w[::-1] for w in words))
        except Exception:
            out.append(s)
    return {"outputs": out}
