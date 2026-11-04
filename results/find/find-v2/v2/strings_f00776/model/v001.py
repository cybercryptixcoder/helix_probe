def predict(probe):
    # Reverse the string [E1: all outputs are reversed inputs]
    # Insert 'W' after the first character [E1: "abc123"->"321Wcba", "level"->"leWvel", "Zebra"->"arWbeZ"]
    # The 'W' is inserted at position 1 of the reversed string [E1]
    # Check: "abc123" reversed = "321cba", insert W at pos1 = "3W21cba"? No...
    # Actual: "321Wcba" = reverse("abc123")="321cba" with W inserted after "321"? 
    # Let's recheck: "abc123" -> "321Wcba". reverse = "321cba". Insert W after 3 chars -> "321Wcba". 
    # "level" -> "leWvel". reverse="level". Insert W after 2 chars -> "leWvel". 
    # "Zebra" -> "arWbeZ". reverse="arbeZ". Insert W after 2 chars -> "arWbeZ". 
    # " Zebralower" -> "rewolWarbeZ ". reverse="rewol arbeZ" (with space). = "rewol arbeZ"? 
    #   " Zebralower" reversed = "rewol arbeZ". Insert W after 5 chars -> "rewolWarbeZ ". Yes!
    # "Hello World function lazy" -> "yzal noitcnuWf dlroW olleH". reverse="yzal noitcnuf dlroW olleH". Insert W after 10 -> "yzal noitcnuWf dlroW olleH". Yes!
    # "bananaUPPER" -> "REPPUWananab". reverse="REPPUananab". Insert W after 5 -> "REPPUWananab". Yes!
    # So: reverse, then insert 'W' at position len(s)//2 (integer division).
    # Check: len 6 -> pos 3. len 5 -> pos 2. len 11 -> pos 5. len 26 -> pos 13? 
    #   "Hello World function lazy" len=26, pos=13. But we inserted after 10. Hmm.
    # Let's recount: "yzal noitcnuWf dlroW olleH". Before W: "yzal noitcnu" = 11 chars. So pos 11.
    # len=26, 26//2=13. Not 11. Hmm.
    # "bananaUPPER" len=11, pos=5. 11//2=5. Yes.
    # "Hello World function lazy" len=26, pos should be 13 by //2, but actual is 11.
    # Wait let me recount "yzal noitcnuWf": y-z-a-l-space-n-o-i-t-c-n-u = 12 chars before W? 
    # "yzal noitcnu" = y,z,a,l,space,n,o,i,t,c,n,u = 12. Then W. So pos 12.
    # 26//2=13. Still off by 1.
    # Hmm, maybe insert at position len//2 but... let me recount the original.
    # "Hello World function lazy" = H,e,l,l,o,space,W,o,r,l,d,space,f,u,n,c,t,i,o,n,space,l,a,z,y = 26.
    # reversed = "yzal noitcnuf dlroW olleH". 
    # "yzal noitcnuWf dlroW olleH": before W = "yzal noitcnu" = 12 chars.
    # 26//2 = 13. Off by one. Maybe it's (len-1)//2? 25//2=12. Yes!
    # Check others: len 6: 5//2=2? But we said pos 3. Hmm no.
    # "abc123" len 6, pos 3. (6-1)//2=2. No.
    # Let me recount "321Wcba": before W = "321" = 3 chars. len 6, pos 3 = 6//2.
    # "leWvel": before W = "le" = 2. len 5, pos 2 = 5//2.
    # "arWbeZ": before W = "ar" = 2. len 5, pos 2 = 5//2.
    # "rewolWarbeZ ": before W = "rewol" = 5. len 11, pos 5 = 11//2.
    # "REPPUWananab": before W = "REPPU" = 5. len 11, pos 5 = 11//2.
    # "yzal noitcnuWf...": before W = 12. len 26, 26//2=13. Off by 1.
    # Let me recount the string "Hello World function lazy" carefully.
    # H(1)e(2)l(3)l(4)o(5) (6)W(7)o(8)r(9)l(10)d(11) (12)f(13)u(14)n(15)c(16)t(17)i(18)o(19)n(20) (21)l(22)a(23)z(24)y(25) = 25 chars!
    # I miscounted. 25//2 = 12. Yes! Matches.
    # So rule: reverse string, insert 'W' at index len//2.
    def f(s):
        r = s[::-1]
        p = len(s) // 2
        return r[:p] + 'W' + r[p:]
    return {"outputs": [f(x) for x in probe["inputs"]]}
