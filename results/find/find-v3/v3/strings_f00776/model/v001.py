def predict(probe):
    # Observations from E1:
    # "abc123" -> "321Wcba"  : reversed, and a 'W' inserted in the middle
    # "level" -> "leWvel"    : reversed is "level"; 'W' inserted in middle
    # " Zebralower" -> "rewolWarbeZ " : reversed, 'W' inserted in middle
    # "Hello World function lazy" -> "yzal noitcnuWf dlroW olleH" : reversed, 'W' inserted mid
    # "bananaUPPER" -> "REPPUWananab" : reversed, 'W' inserted mid
    # "Zebra" -> "arWbeZ" : reversed, 'W' inserted mid
    # Rule: reverse the string, then insert 'W' at the middle position.
    # For even length n, middle index = n//2. For odd length n, middle index = n//2.
    # Check: "abc123" len 6 -> reversed "321cba", insert at 3 -> "321Wcba" ✓
    # "level" len 5 -> reversed "level", insert at 2 -> "leWvel" ✓
    # " Zebralower" len 11 -> reversed "rewol arbeZ" wait let's check:
    #   " Zebralower" reversed = "rewol arbeZ "? Let's compute: chars: ' ','Z','e','b','r','a','l','o','w','e','r'
    #   reversed: 'r','e','w','o','l','a','r','b','e','Z',' ' = "rewolarbeZ "
    #   insert at 11//2=5 -> "rewol"+"W"+"arbeZ " = "rewolWarbeZ " ✓
    # "Hello World function lazy" len 25 -> reversed, insert at 12
    #   reversed = "yzal noitcnu f dlroW olleH"? let's trust: insert at 12 gives "yzal noitcnuWf dlroW olleH" ✓
    # "bananaUPPER" len 11 -> reversed "REPPUananab", insert at 5 -> "REPPUWananab" ✓
    # "Zebra" len 5 -> reversed "arbeZ", insert at 2 -> "arWbeZ" ✓
    def f(s):
        r = s[::-1]
        m = len(r) // 2
        return r[:m] + "W" + r[m:]
    return {"outputs": [f(x) for x in probe["inputs"]]}
