def predict(probe):
    # x = a + b - 5 [E1, E3, E5, E6]
    #   E1: a=5,b=5 -> x=5
    #   E3: a=5,b=8 -> x=2  => b contributes -1 per unit? wait: 5+8-5=8, not 2.
    # Let's recheck: E3 x=2 with a=5,b=8 => x = a - b + 5 = 2. E5 a=8,b=5 -> x=8? observed 10.
    # E5: a=8,b=5 -> x=10 => x = a + b - 3? 8+5-3=10. E3: 5+8-3=10 no.
    # Try x = a + b - 5: E1 5, E3 8 no.
    # E3: x=2, E5: x=10, E6: x=10. E1: x=5.
    # E3 (a5,b8)->2 ; E5 (a8,b5)->10 ; E6 (a8,b5)->10 ; E1 (a5,b5)->5
    # a coefficient: from E1->E5 a+3 gives x+5 => a coeff 5/3? unlikely.
    # Maybe x = a + b - 5? E3: 5+8-5=8 no.
    # Try x = a - b + 5: E3 2 ok, E5 8 no.
    # Try x = a + b - 5: no.
    # x = a*? Let's solve linear: x = p*a + q*b + r
    # E1: 5p+5q+r=5
    # E3: 5p+8q+r=2 => 3q=-3 => q=-1
    # E5: 8p+5q+r=10 => 3p=5 => p=5/3
    # r = 5-5*(5/3)-5*(-1)=5-25/3+5=10-25/3=5/3
    # Check E6: 8*(5/3)+5*(-1)+5/3=40/3-5+5/3=45/3-5=15-5=10 ok!
    # So x = (5/3)a - b + 5/3. Hmm odd but fits.
    # y: E1 y=5 (c=5), E2 y=8 (c=8), E3 y=5 (c=5), E5 y=6 (c=5!), E6 y=9 (c=8)
    # E5: a=8,b=5,c=5 -> y=6. E1 a=5,b=5,c=5 -> y=5. So a affects y!
    # y = c + (a-5)/3? E5: 5+1=6 ok. E6: 8+1=9 ok. E2: 8+0=8 ok. E3: 5+0=5 ok.
    # size: E1 1.0 (c=5), E2 2.5 (c=8), E3 1.0 (c=5), E5 2.5 (a=8,c=5), E6 1.0 (a=8,c=8)
    # E5 size 2.5 with c=5,a=8. E1 size 1.0 c=5,a=5. So a affects size too.
    # size = 0.5*c - 1.5 + (a-5)/2? E5: 1.0+1.5=2.5 ok. E6: 2.5+1.5=4.0 no (obs 1.0).
    # Hmm E6 size 1.0 with a=8,c=8. E2 size 2.5 with a=5,c=8.
    # size depends on c and a: E1(5,5)=1, E2(5,8)=2.5, E5(8,5)=2.5, E6(8,8)=1
    # size = 1 + 0.5*|c-5|? E2: 1+1.5=2.5 ok, E5: 1+0=1 no.
    # size = 1 + 0.5*|a-5|? E5: 1+1.5=2.5 ok, E2: 1+0=1 no.
    # size = 1 + 0.5*|a-c|? E1:1, E2:1+1.5=2.5 ok, E5:1+1.5=2.5 ok, E6:1 ok!
    # y = c + (a-5)/3? check E5: 5+1=6 ok. But maybe y = c + (a-c)/3? E5:5+1=6, E6:8+0=8 no(obs9).
    # y = c + (a-5)/3 fits all: E1 5, E2 8, E3 5, E5 6, E6 9. Good.
    # x = (5/3)a - b + 5/3. Check E1: 25/3-5+5/3=30/3-5=10-5=5 ok.
    # switch: E4 on at all 5 -> same as off. Assume no effect [?]
    a = probe.get("a", 5)
    b = probe.get("b", 5)
    c = probe.get("c", 5)
    x = (5.0/3.0)*a - b + 5.0/3.0
    y = c + (a - 5)/3.0
    size = 1 + 0.5*abs(a - c)
    return {"x": round(x, 2), "y": round(y, 2), "size": round(size, 2)}
