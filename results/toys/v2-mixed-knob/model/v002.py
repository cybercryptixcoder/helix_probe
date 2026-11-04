def predict(probe):
    # x = a - b  [E1: 8.4-7.6=0.8? no, x=9.2; E2: 0-7.6=-7.6 ✓; E3: 9.7-4.9=4.8? no]
    # E2 x=-7.6 with a=0,b=7.6 -> x = a - b = -7.6 ✓
    # E1 x=9.2 with a=8.4,b=7.6 -> a-b=0.8, not 9.2. Contradiction.
    # Try x = a + b - c? E2: 0+7.6-4.2=3.4 no.
    # E1: 9.2, E2: -7.6, E3: 10
    # E2: a=0,b=7.6,c=4.2 -> x=-7.6. Looks like a - b = -7.6.
    # E1: a=8.4,b=7.6 -> a-b=0.8, but x=9.2. Hmm.
    # Maybe x = a - b + something. E1 vs E2 differ in a (8.4 vs 0) and same b,c.
    # E1 x=9.2, E2 x=-7.6: delta a=8.4, delta x=16.8 -> slope 2 on a? 
    # x = 2a - b + k: E2: 0-7.6+k=-7.6 -> k=0. E1: 16.8-7.6=9.2 ✓!
    # E3: 2*9.7-4.9=14.5, but x=10. Clamped at 10? x max 10. ✓ (14.5->10)
    # y: E1 y=5.2, E2 y=4.2, E3 y=10.2
    # E1 vs E2: same b,c, differ a. y 5.2 vs 4.2, delta a=8.4 -> slope 1/8.4? odd.
    # E2: a=0,b=7.6,c=4.2 -> y=4.2 = c. E1: c=4.2 but y=5.2. 
    # E1 vs E2 differ only in a: y delta = 1.0 for a delta 8.4. Hmm ~ a/8.4?
    # Maybe y = c + a/8.4? E3: c=9.2, a=9.7 -> 9.2+1.15=10.35, observed 10.2. close-ish but not exact.
    # Try y = c + a/8? E1: 4.2+1.05=5.25 vs 5.2. E3: 9.2+1.21=10.41 no.
    # Try y = c + a/10? E1: 4.2+0.84=5.04 no.
    # E3 y=10.2, c=9.2 -> diff 1.0, a=9.7. E1 diff 1.0, a=8.4. E2 diff 0, a=0.
    # diff = 1.0 when a>0? Maybe y = c + 1 if a>0 else c? crude.
    # Better: diff = a/8.4? E1: 1.0 ✓, E3: 9.7/8.4=1.15 -> 10.35 vs 10.2. no.
    # diff = min(a,10)/10? E1: 0.84 no.
    # Maybe y = c + a/8.4 rounded? E3 gives 10.35 rounds 10.35 not 10.2.
    # Try y = c + a/10 + something. Hmm.
    # E3 y=10.2, c=9.2, a=9.7. E1 y=5.2,c=4.2,a=8.4. Both diff=1.0.
    # Maybe diff = 1 when a in [8,10]? E2 a=0 diff 0.
    # Guess: y = c + (1 if a>=8 else a/8.4) ? weak.
    # Simpler: y = c + a/8.4 clamped? E3: 9.2+1.15=10.35 no.
    # Let's try y = c + a/10 + 0.16? no.
    # Given uncertainty, use y = c + a/8.4 (fits E1 exactly, E2 exactly, E3 off by 0.15).
    # size: E1 3.1, E2 3.1, E3 1.25
    # E1,E2 same c=4.2 -> size 3.1. E3 c=9.2 -> 1.25.
    # size = 10 - c + something? E1: 5.8 no.
    # size = c - 1.1? E1: 3.1 ✓, E2: 3.1 ✓, E3: 8.1 ✗.
    # E3 size 1.25 with c=9.2. Maybe size = 10 - c + 0.05? 0.85 no.
    # size = (10-c)*? E3: 0.8*? =1.25 -> 1.56. E1: 5.8*?=3.1 -> 0.53. no.
    # Maybe size depends on a too. E3 a=9.7 -> small. E1 a=8.4 -> 3.1.
    # size = 10 - c + (a-8)? E3: 0.8+1.7=2.5 no.
    # Try size = 10 - c - a/10 + k? E1: 5.8-0.84=4.96 no.
    # E3: size 1.25. c=9.2. 10-c=0.8. diff 0.45.
    # E1: 10-c=5.8, size 3.1, diff -2.7.
    # Hmm. Maybe size = 10 - c - a/4 + k? E1: 5.8-2.1=3.7 no.
    # Try size = (10-c) - a/4 + 0.5? E1: 5.8-2.1+0.5=4.2 no.
    # Given difficulty, guess size = 10 - c - a/4 + 1.4? E1: 5.8-2.1+1.4=5.1 no.
    # Let's just fit two points: E1 (a=8.4,c=4.2)->3.1, E3(a=9.7,c=9.2)->1.25.
    # Assume size = p - q*c - r*a. Two eqs, underdetermined. 
    # E2 same as E1 (a=0? no a=0,c=4.2)->3.1. So a=0 and a=8.4 both give 3.1 at c=4.2!
    # So size independent of a at c=4.2. Then E3 differs by c only: c 4.2->9.2, size 3.1->1.25.
    # slope = (1.25-3.1)/(9.2-4.2) = -1.85/5 = -0.37. size = 3.1 -0.37*(c-4.2) = 4.654 -0.37c.
    # Check E3: 4.654-3.404=1.25 ✓. 
    # So size = 4.65 - 0.37*c roughly. Let's use size = 4.654 - 0.37*c.
    a = probe.get("a", 0)
    b = probe.get("b", 0)
    c = probe.get("c", 0)
    x = min(10, 2*a - b)
    y = c + a/8.4
    size = 4.654 - 0.37*c
    return {"x": round(x, 2), "y": round(y, 2), "size": round(size, 2)}
