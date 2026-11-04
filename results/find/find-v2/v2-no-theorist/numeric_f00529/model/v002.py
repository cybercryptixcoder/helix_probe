def predict(probe):
    # Output is ~-6.9 or ~-7.9 depending on x [E1]
    # Sign rule: x>0 -> -6.9, x<0 -> -7.9, x=0 -> -7.8991 (negative side) [E2]
    # Small |x| on positive side shows smooth correction: -6.9 - small term [E1,E2]
    #   x=2.9 -> -6.9015, x=2.0 -> -6.9889, x=1.0 -> -7.8111, x=0.5 -> -7.8906 [E1,E2]
    #   This looks like -6.9 - 0.1/x? check: x=2 -> -6.9-0.05=-6.95 (obs -6.9889) no
    #   Try -6.9 - 0.1/(x-?): x=2 -> -6.9889 => delta -0.0889; x=1 -> -0.9111; x=0.5 -> -0.9906
    #   delta ~ -1 + something? x=1: -0.9111, x=0.5: -0.9906, x=2: -0.0889
    #   Looks like delta = -1 + x*something? x=1 -> -0.9111, x=2 -> -0.0889, x=0.5 -> -0.9906
    #   delta+1: 0.0889, 0.9111, 0.0094 -> not linear
    #   Try delta = -1/(1+?): x=1: 0.9111, x=2: 0.0889, x=0.5: 0.9906
    #   Hmm 0.9111 ~ 1-0.0889, 0.0889 ~ ... maybe delta = -1 + x^2/(1+x^2)? x=1: -0.5 no
    #   Try delta = -1 + 1/(1+x^2)*something: x=1: 0.9111, x=2: 0.0889, x=0.5: 0.9906
    #   1-delta: 0.0889, 0.9111, 0.0094. x=1->0.0889, x=2->0.9111? no x=2 gives 0.0889
    #   Actually x=2: -6.9889 delta=-0.0889; x=1: -7.8111 delta=-0.9111; x=0.5: -7.8906 delta=-0.9906
    #   delta ~ -1 + 1/(1+x)? x=1: -0.5 no. delta ~ -1 + x/(1+x)? x=1: -0.5 no
    #   delta ~ -1 + 1/(1+x^2)? x=1: -0.5 no
    #   delta ~ -1 + 1/(1+x)^2? x=1: -0.75 no
    #   Try delta = -1 + (x/(1+x))^2? x=1: -0.75 no
    #   Look: 1+delta: x=2->0.9111, x=1->0.0889, x=0.5->0.0094
    #   x=2: 0.9111, x=1: 0.0889 -> these look like 1/(1+x)? x=2:0.333 no
    #   Maybe delta = -1/(1+x^2)? x=1: -0.5 no
    #   Try delta = -1 + x^2/(1+x^2)? x=1: -0.5 no
    #   Hmm x=2: 0.9111, x=1: 0.0889. Sum=1.0! x=0.5: 0.0094, x=1: 0.0889 sum=0.0983
    #   Maybe 1+delta = x/(1+x)? x=2: 0.667 no. = (x-1)/x? x=2:0.5 no
    #   Try 1+delta = 1 - 1/x^k? x=2: 0.9111 => 1/x^k=0.0889 => x^k=11.25, k~3.5
    #   x=1: 1/x^k=0.9111 => x^k=1.097, k~0.13. inconsistent
    #   Reconsider: maybe it's -6.9 - 1/(1+something)
    #   x=2: -6.9889, x=1: -7.8111, x=0.5: -7.8906, x=0.1: -7.8985, x=0.01: -7.899
    #   As x->0+, approaches -7.9. As x grows, approaches -6.9.
    #   x=0.01: -7.899 (delta -0.999), x=0.1: -7.8985 (delta -0.9985), x=0.5: -7.8906 (delta -0.9906)
    #   x=1: -7.8111 (delta -0.9111), x=2: -6.9889 (delta -0.0889)
    #   Looks like delta = -1/(1+x^a)? x=1: -0.5 no
    #   Try delta = -1 + x^a/(1+x^a)? same
    #   Try delta = -(1 - x^a/(1+x^a))... 
    #   Actually: 1+delta = x^a/(1+x^a)? x=2: 0.9111 => x^a/(1+x^a)=0.9111 => x^a=10.25 => a~3.36
    #   x=1: 0.0889 => x^a/(1+x^a)=0.0889 => x^a=0.0976 => a~ -3.36 (since 1^a=1 always) contradiction
    #   So not that form. x=1 gives 0.0889 which is small.
    #   Maybe 1+delta = 1/(1+x^a)? x=2: 0.9111 => 1+x^a=1.0976 => x^a=0.0976 => a~-3.36
    #   x=1: 0.0889 => 1+x^a=11.25 => x^a=10.25 => a~3.36. Contradiction (1^a=1).
    #   Hmm. x=1 is special? At x=1, 1+delta=0.0889. At x=2, 0.9111. At x=0.5, 0.0094.
    #   x=0.5: 0.0094, x=1: 0.0889, x=2: 0.9111. Ratios: 0.0889/0.0094=9.46, 0.9111/0.0889=10.25
    #   Roughly x10 per doubling -> x^3.3. So 1+delta ~ c*x^3.3? x=1: c=0.0889, x=2: 0.0889*2^3.3=0.0889*9.85=0.876 close to 0.9111
    #   x=0.5: 0.0889*0.5^3.3=0.0889*0.101=0.009 close to 0.0094. 
    #   So 1+delta ~ 0.0889 * x^3.3. Hmm but as x->0, 1+delta->0, delta->-1, y->-7.9. Good.
    #   As x grows, 1+delta grows, delta->0, y->-6.9. Good.
    #   But x=5: -6.9 (delta 0), x=10: -6.9. So saturates at -6.9.
    #   Maybe delta = -1/(1+x^a) with a~3.3? x=1: -0.5 no (obs -0.9111)
    #   Maybe delta = -1 + x^a/(1+x^a) with a~3.3? x=1: -0.5 no
    #   Wait x=1: delta=-0.9111, so 1+delta=0.0889. If 1+delta = x^a/(1+x^a), x=1 gives 0.5. No.
    #   If 1+delta = 1/(1+x^a), x=1 gives 0.5. No.
    #   So x=1 is not on the smooth curve? Or my reading is off.
    #   Let me reconsider: maybe it's -6.9 - 1/(1+exp(k(x-x0)))? sigmoid.
    #   x=0.01: -7.899, x=0.1: -7.8985, x=0.5: -7.8906, x=1: -7.8111, x=2: -6.9889, x=5: -6.9
    #   Sigmoid from -7.9 to -6.9 centered around x~1.5? 
    #   At x=1: -7.8111, x=2: -6.9889. Midpoint -7.4 would be around x~1.5.
    #   Sigmoid: y = -7.9 + 1/(1+exp(-k(x-x0)))
    #   x=1: 0.0889 = 1/(1+exp(-k(1-x0)))
    #   x=2: 0.9111 = 1/(1+exp(-k(2-x0)))
    #   x=0.5: 0.0094 = 1/(1+exp(-k(0.5-x0)))
    #   From x=1: 1+exp(-k(1-x0))=11.25 => exp(-k(1-x0))=10.25 => -k(1-x0)=2.327
    #   From x=2: 1+exp(-k(2-x0))=1.0976 => exp(-k(2-x0))=0.0976 => -k(2-x0)=-2.327
    #   Adding: -k(3-2x0)=0 => x0=1.5. Then -k(1-1.5)=2.327 => 0.5k=2.327 => k=4.654
    #   Check x=0.5: -k(0.5-1.5)=4.654 => exp(4.654)=105 => 1/(1+105)=0.0094. YES!
    #   Check x=0.1: -k(0.1-1.5)=6.516 => exp=675 => 1/676=0.00148 => y=-7.8985. YES!
    #   Check x=0.01: -k(0.01-1.5)=6.936 => exp=1029 => 1/1030=0.00097 => y=-7.899. YES!
    #   Check x=5: -k(5-1.5)=-16.3 => exp(-16.3)~8e-8 => 1/(1+8e-8)~1 => y=-6.9. YES!
    #   So positive side: y = -7.9 + 1/(1+exp(-4.654*(x-1.5))) for x>0
    #   But wait, at x=2.9 (E1): -k(2.9-1.5)=-6.516 => exp=675 => 1/676=0.00148 => y=-7.8985. But obs is -6.9015!
    #   Contradiction! E1 x=2.9 gives -6.9015, not -7.8985.
    #   Hmm. So E1 and E2 disagree? Let me recheck E1: x=2.9 -> -6.9015. E2: x=2.0 -> -6.9889, x=5.0 -> -6.9.
    #   At x=2.9, sigmoid predicts ~-7.8985 but E1 says -6.9015. 
    #   Wait, maybe I misread. E1: 2.9 -> -6.9015. That's close to -6.9, delta -0.0015.
    #   E2: x=2.0 -> -6.9889 (delta -0.0889), x=5.0 -> -6.9 (delta 0).
    #   So at x=2.9, delta should be between -0.0889 and 0, ~-0.0015. Consistent with sigmoid!
    #   Let me recompute sigmoid at x=2.9: -k(2.9-1.5)=-4.654*1.4=-6.516. exp(-6.516)=0.00148. 1/(1+0.00148)=0.9985. y=-7.9+0.9985=-6.9015. YES! I made arithmetic error before.
    #   Great, sigmoid fits E1 and E2 positive side.
    # Negative side: all -7.9 (x=-0.001: -7.8991, x=-0.5: -7.8999, x=-1: -7.9, x=-5: -7.9, etc.)
    #   x=-0.001: -7.8991, x=-0.01: -7.8991, x=-0.1: -7.8994, x=-0.5: -7.8999
    #   These are all ~-7.899 to -7.9, essentially -7.9. Small variations maybe noise or tiny effect.
    #   x=0.0: -7.8991 (same as -0.001). So x=0 behaves like negative side.
    # So rule: x>0 -> sigmoid from -7.9 to -6.9; x<=0 -> -7.9 (approximately)
    # Actually negative side shows -7.8991 to -7.9, tiny variation. Could be noise. Treat as -7.9.
    # But x=0 gives -7.8991, not exactly -7.9. And x=-0.001 gives -7.8991. Small offset.
    # Maybe negative side is -7.9 + tiny. Let's just use -7.9 for x<=0, with maybe -7.8991 for very small?
    # Simpler: x<=0 -> -7.9. The -7.8991 is close enough (0.0009 off).
    import math
    out = []
    for x in probe.get("x", []):
        if x > 0:
            y = -7.9 + 1.0/(1.0 + math.exp(-4.654*(x-1.5)))
        else:
            y = -7.9
        out.append(y)
    return {"y": out}
