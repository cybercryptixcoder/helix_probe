def predict(probe):
    # x = 2a - b, clamped to [-10, 10] [E1: 16.8-7.6=9.2 ✓; E2: -7.6 ✓; E3: 19.4-4.9=14.5→10 ✓; E4: 10-7.6=2.4 ✓]
    # y = c + a/8.4? E4 breaks this: a=5,c=4.2 -> y=4.2, not 4.8. So y depends on a differently.
    # y: E1(a=8.4,c=4.2)->5.2; E2(a=0,c=4.2)->4.2; E3(a=9.7,c=9.2)->10.2; E4(a=5,c=4.2)->4.2
    # E2 and E4 both y=c (a=0 and a=5). E1 y=c+1 (a=8.4). E3 y=c+1 (a=9.7).
    # So y = c + 1 when a>=~8, else c? Threshold between 5 and 8.4. Guess a>=8.
    # size: E1(a=8.4,c=4.2)->3.1; E2(a=0,c=4.2)->3.1; E3(a=9.7,c=9.2)->1.25; E4(a=5,c=4.2)->1.4
    # E2 vs E4: same c=4.2, a 0 vs 5, size 3.1 vs 1.4. So size DOES depend on a.
    # E1 a=8.4 -> 3.1 again (like a=0). Non-monotonic in a? 
    # Maybe size depends on x? E1 x=9.2 size 3.1; E2 x=-7.6 size 3.1; E3 x=10 size 1.25; E4 x=2.4 size 1.4
    # Hmm E1 and E3 both x~10 but sizes differ (3.1 vs 1.25). So not x alone.
    # size vs c: E1 c=4.2->3.1, E2 c=4.2->3.1, E4 c=4.2->1.4. Same c, different size. So a matters.
    # size vs a: a=0->3.1, a=5->1.4, a=8.4->3.1, a=9.7->1.25. U-shaped? min around a=5?
    # Maybe size = |a - 5|*k + base? a=5:1.4; a=0: 5k+1.4=3.1 -> k=0.34; a=8.4: 3.4*0.34+1.4=2.56 no.
    # Try size depends on b? E1 b=7.6, E2 b=7.6, E4 b=7.6 all same b. sizes 3.1,3.1,1.4. So not b.
    # E3 b=4.9 size 1.25. 
    # Let's reconsider: maybe size = 10 - |x|? E1 |9.2|->0.8 no.
    # size = 10 - c + f(a)? E1: 5.8+f=3.1 -> f=-2.7; E2: f=-2.7; E4: f=-4.4; E3: 0.8+f=1.25->f=0.45
    # f(a): a=0->-2.7, a=5->-4.4, a=8.4->-2.7, a=9.7->0.45. Not clean.
    # Alternative: size = 10 - c - a/4 + something? E1:5.8-2.1=3.7 vs 3.1; E4:5.8-1.25=4.55 vs 1.4 no.
    # Maybe size = 10 - c - |a-?|... Let's try size = 10 - c - a/2 + 2? E1:5.8-4.2+2=3.6; E4:5.8-2.5+2=5.3 no.
    # Try size = (10-c) * g(a)? E1:5.8*g=3.1->g=0.534; E2 same; E4:5.8*g=1.4->g=0.241; E3:0.8*g=1.25->g=1.56
    # g(a): 0->0.534, 5->0.241, 8.4->0.534, 9.7->1.56. Hmm.
    # Maybe size = 10 - c - a/4 + a^2/40? E1:5.8-2.1+1.76=5.46 no.
    # Let's try size = 10 - c - a/2 + a^2/20? E1:5.8-4.2+3.53=5.13 no.
    # Try size = 10 - c - a/2 + a^2/25? E1:5.8-4.2+2.82=4.42 no.
    # Maybe size = 10 - c - a/2 + a^2/30? E1:5.8-4.2+2.35=3.95; E4:5.8-2.5+0.83=4.13 no.
    # Try size = 10 - c - a/2 + a^2/50? E1:5.8-4.2+1.41=3.01~3.1; E4:5.8-2.5+0.5=3.8 no.
    # Hmm E4 size 1.4 is small with a=5,c=4.2. E1 a=8.4,c=4.2 size 3.1.
    # Maybe size = 10 - c - a/2 + a^2/20 - ... let's fit quadratic in a at c=4.2:
    # points (0,3.1),(5,1.4),(8.4,3.1). Fit size = p + q*a + r*a^2.
    # p=3.1. 5q+25r = -1.7. 8.4q+70.56r = 0. 
    # From first: q = -0.34 - 5r. Sub: 8.4(-0.34-5r)+70.56r=0 -> -2.856-42r+70.56r=0 -> 28.56r=2.856 -> r=0.1. q=-0.34-0.5=-0.84.
    # size = 3.1 -0.84a +0.1a^2 at c=4.2. Check a=9.7: 3.1-8.148+9.409=4.36. But E3 c=9.2 not 4.2.
    # Need c dependence. E3: c=9.2, a=9.7, size 1.25. At c=4.2,a=9.7 formula gives 4.36. Delta c=5 -> delta size=-3.11 -> slope -0.62 per c.
    # Check E1 c=4.2: 3.1 ✓. So size = 3.1 -0.84a+0.1a^2 -0.62*(c-4.2)? 
    # E3: 4.36 -0.62*5 = 4.36-3.1=1.26 ✓!
    # E2: a=0,c=4.2: 3.1 ✓. E4: a=5: 3.1-4.2+2.5=1.4 ✓!
    # Great: size = 3.1 -0.84a +0.1a^2 -0.62(c-4.2)
    # Simplify: = 0.1a^2 -0.84a -0.62c + 3.1+2.604 = 0.1a^2 -0.84a -0.62c + 5.704
    # Check E1: 0.1*70.56 -7.056 -2.604 +5.704 = 7.056-7.056-2.604+5.704=3.1 ✓
    a = probe.get("a", 0)
    b = probe.get("b", 0)
    c = probe.get("c", 0)
    x = max(-10, min(10, 2*a - b))
    y = c + (1 if a >= 8 else 0)  # ? threshold between 5 and 8.4
    size = 0.1*a*a - 0.84*a - 0.62*c + 5.704
    return {"x": round(x, 2), "y": round(y, 2), "size": round(size, 2)}
