def predict(probe):
    # Observations from E1:
    # - "abc123" -> "321Wcba": reversed, and '1' became 'W'? Wait: reversed is "321cba".
    #   Observed "321Wcba": position of '1' became 'W'? Let's check: input abc123 reversed = 321cba.
    #   Observed = 321Wcba. So '1' -> 'W'? Hmm, actually input has '1','2','3'; reversed "321cba".
    #   Observed "321Wcba": chars: 3,2,1,W,c,b,a. So the '1' became 'W'? No wait reversed is 3,2,1,c,b,a.
    #   Observed is 3,2,1,W,c,b,a — an extra W inserted? Or '1'->'W'? Let's compare lengths:
    #   input len 6, output len 7. So a 'W' was inserted.
    # - "level" -> "leWvel": len 5 -> 6. Inserted 'W' after "le". So insert 'W' at position 2.
    # - " Zebralower" -> "rewolWarbeZ ": reversed = "rewol arbeZ " ... let's reverse: input " Zebralower"
    #   reversed = "rewol arbeZ " (with leading space becoming trailing). Observed "rewolWarbeZ ".
    #   So space between "rewol" and "arbeZ" became 'W'. So space -> 'W'? But then length same.
    #   Actually reversed of " Zebralower" = "rewolarbeZ " (no space in middle). Let me recount:
    #   " Zebralower" chars: ' ','Z','e','b','r','a','l','o','w','e','r'. reversed: 'r','e','w','o','l','a','r','b','e','Z',' '.
    #   = "rewolarbeZ ". Observed "rewolWarbeZ ". So 'a' at position 5 became 'W'. Hmm.
    # - "Hello World function lazy" reversed = "yzal noitcnuf dlroW olleH". Observed "yzal noitcnuWf dlroW olleH".
    #   So 'f' in "function" (which after reversal is "noitcnuf") became 'W': "noitcnuWf". So 'f' -> 'W'? 
    #   Wait "noitcnuf" -> "noitcnuWf": the 'f' at end became... let's see: n,o,i,t,c,n,u,f -> n,o,i,t,c,n,u,W,f. Inserted W before f.
    # - "bananaUPPER" -> "REPPUWananab": reversed = "REPPUananab". Observed "REPPUWananab": inserted 'W' between "REPPU" and "ananab".
    # - "Zebra" -> "arWbeZ": reversed = "arbeZ". Observed "arWbeZ": inserted 'W' after "ar".
    
    # Pattern: reverse the string, then insert 'W' at some position.
    # Positions of W insertion (in reversed string):
    # abc123: reversed "321cba", output "321Wcba" -> insert at index 3.
    # level: reversed "level", output "leWvel" -> insert at index 2.
    # " Zebralower": reversed "rewolarbeZ ", output "rewolWarbeZ " -> insert at index 5.
    # "Hello World function lazy": reversed "yzal noitcnuf dlroW olleH", output "yzal noitcnuWf dlroW olleH" -> insert at index 10.
    # bananaUPPER: reversed "REPPUananab", output "REPPUWananab" -> insert at index 5.
    # Zebra: reversed "arbeZ", output "arWbeZ" -> insert at index 2.
    
    # Insertion index vs original length:
    # len 6 -> idx 3
    # len 5 -> idx 2
    # len 11 -> idx 5
    # len 26 -> idx 10
    # len 11 -> idx 5
    # len 5 -> idx 2
    # So idx = len // 2. Check: 6//2=3 ✓, 5//2=2 ✓, 11//2=5 ✓, 26//2=13 ✗ (got 10).
    # Hmm 26//2=13 but observed 10. Let me recount "Hello World function lazy": 
    # H-e-l-l-o(5) space(6) W-o-r-l-d(11) space(12) f-u-n-c-t-i-o-n(20) space(21) l-a-z-y(25). len=25.
    # 25//2=12, but observed idx 10. Hmm.
    # Let me recount reversed: "yzal noitcnuf dlroW olleH" len 25.
    # Observed "yzal noitcnuWf dlroW olleH". Position of W: y(0)z(1)a(2)l(3) (4)n(5)o(6)i(7)t(8)c(9)n(10)u(11)W(12)f(13)...
    # So W at index 12. 25//2=12 ✓. I miscounted before.
    # Great: insert 'W' at index len//2 of the reversed string.
    
    def transform(s):
        r = s[::-1]
        i = len(r) // 2
        return r[:i] + 'W' + r[i:]
    
    return {"outputs": [transform(x) for x in probe["inputs"]]}
