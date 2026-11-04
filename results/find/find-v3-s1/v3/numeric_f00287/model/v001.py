import math

def predict(probe):
    # Observations:
    # E1/E2: f is deterministic in x (repeats give same value, up to tiny noise ~1e-4).
    # E1/E2: For |x| large, output is negative and grows in magnitude: looks like -x^2-ish.
    #   x=88.9 -> -1478.4 ; 88.9^2=7903.2 -> not x^2. Try -x*|x|? 88.9^2=7903 no.
    #   Check: -1478.4/88.9 = -16.63 ; 67.5 -> -1125.6/67.5=-16.68 ; 73.9 -> -1226.4/73.9=-16.59
    #   So for large |x|, y ≈ -16.6 * x. Hmm, but 38.8 -> -638.4/38.8=-16.45. Consistent linear!
    #   -62.7 -> 44.1 (positive!) ; -93.6 -> 65.8 ; -104 -> 72.8 ; -120.7 -> 84.7
    #   For negative x: 65.8/-93.6=-0.703 ; 44.1/-62.7=-0.703 ; 72.8/-104=-0.700 ; 84.7/-120.7=-0.702
    #   So negative x: y ≈ -0.70*x (positive). Positive large x: y ≈ -16.6*x (negative).
    #   -12.9 -> 9.1 ; 9.1/-12.9=-0.705 consistent.
    #   -1.2 -> -402.4 (!!) huge negative. So there's a special region near 0.
    #   Small |x| gives huge negative ~ -402. Looks like a pole/asymptote near 0.
    #   -1.2 -> -402.4 ; -402.4 * 1.2 = 482.9 ; 1/1.2=0.833. Try -c/x^2? 
    #   -402.4 * 1.44 = 579.5. Hmm. Try -c/x: -402.4*1.2=-482.9.
    #   Maybe a rational: something like a/(x+b) + linear.
    #   Let's hypothesize: y = A*x + B/x + C? For x=-1.2: A*(-1.2)+B/(-1.2)+C = -402.4
    #   For x=-12.9: -0.705*... wait that's the linear part.
    #   Actually for |x|>=~10, y ≈ -0.70*x for x<0, and -16.6*x for x>0.
    #   That's asymmetric. Suggests maybe y = -x * g(x) where g is a function.
    #   x>0: g≈16.6 ; x<0: g≈0.70. 
    #   Near 0: huge negative. -402 at x=-1.2.
    #   Guess: y = -x*(a + b/x^2)?? = -a*x - b/x. At x=-1.2: -a*(-1.2) - b/(-1.2)=1.2a+0.833b=-402.4
    #   At x=-12.9: 12.9a + b/12.9 = 9.1 -> 12.9a+0.0775b=9.1
    #   At x=88.9: -88.9a - b/88.9 = -1478.4 -> 88.9a + 0.01125b=1478.4
    #   From x=88.9 and x=-12.9: 
    #     12.9a+0.0775b=9.1
    #     88.9a+0.01125b=1478.4
    #   Solve: from first a=(9.1-0.0775b)/12.9=0.7054-0.006008b
    #   88.9*(0.7054-0.006008b)+0.01125b=1478.4 -> 62.71-0.5341b+0.01125b=1478.4 -> -0.5229b=1415.7 -> b=-2707
    #   a=0.7054-0.006008*(-2707)=0.7054+16.26=16.97
    #   Check x=-1.2: 1.2*16.97+0.833*(-2707)=20.36-2255=-2235. Not -402. So -b/x form wrong.
    #   Try y = -a*x - b/x^2? At x=-1.2: 1.2a + b/1.44 = -402.4
    #   At x=-12.9: 12.9a + b/166.4 = 9.1
    #   At x=88.9: -88.9a - b/7903 = -1478.4 -> 88.9a+b/7903=1478.4
    #   From x=88.9: a=(1478.4-b/7903)/88.9=16.63-0.00000142b
    #   x=-12.9: 12.9*(16.63-1.42e-6 b)+b/166.4=9.1 -> 214.5-1.83e-5 b+0.00601b=9.1 -> 0.00599b=-205.4 -> b=-34290
    #   a=16.63+0.0487=16.68
    #   x=-1.2: 1.2*16.68+(-34290)/1.44=20.0-23812=-23792. No.
    #   So the near-zero behavior is not a simple pole in this form. 
    #   Maybe there's a separate region: |x|<some threshold behaves differently.
    #   Only data point in small region: x=-1.2 -> -402.4. And x=-12.9 -> 9.1 (linear regime).
    #   So threshold between 1.2 and 12.9. 
    #   Could be: for |x| < T, y = something like -k/x^2 or -k/|x|.
    #   -402.4 at x=-1.2. If -k/x^2: k=402.4*1.44=579.5. If -k/|x|: k=482.9.
    #   Need more data. Best guess: piecewise.
    #   Let me fit linear parts precisely.
    #   x>0: points (88.9,-1478.4),(67.5,-1125.6),(73.9,-1226.4),(38.8,-638.4)
    #     slopes: -16.63,-16.68,-16.60,-16.45. Slight variation -> maybe not pure linear, or noise.
    #     Actually 38.8 gives -16.45, off. Could be y=-a*x with a~16.6 plus small term.
    #   x<0 (|x|>=10): (-93.6,65.8),(-62.7,44.1),(-104,72.8),(-120.7,84.7),(-12.9,9.1)
    #     slopes: -0.703,-0.703,-0.700,-0.702,-0.705. Very consistent ~ -0.703.
    #   So negative side: y ≈ -0.703*x for x <= -10ish.
    #   Positive side: y ≈ -16.6*x for x >= 10ish.
    #   Asymmetric slopes suggest maybe y = -x * (something depending on sign) OR
    #   maybe y = -x*(a + b*sign(x))? 
    #   Hmm, or maybe it's y = -x * (c + d*tanh(x))? For large +x: c+d; large -x: c-d.
    #   c+d=16.6, c-d=0.703 -> c=8.65, d=7.95. 
    #   Then near 0: y≈-x*c = -8.65x, small. But we see -402 at x=-1.2. So there's an extra term.
    #   Extra term near 0: at x=-1.2, linear part gives -8.65*(-1.2)=10.4. Observed -402.4. Extra=-412.8.
    #   Could be -k/x^2 with k=412.8*1.44=594. Or -k/|x| with k=495.
    #   Or maybe a Gaussian-like dip? -A*exp(-x^2/(2s^2))? At x=-1.2 dip=-412.8.
    #   Without more data, I'll guess a narrow region near 0 with a large negative value.
    #   Let me just model: base linear-ish + a sharp negative spike near 0.
    #   Actually, maybe it's -x*(c+d*tanh(x)) - k/x^2? Let's just encode best guess.
    #   Given uncertainty, use: 
    #     if |x| < 5 (guess): y = -0.703*x - 580/x^2  (tuned so x=-1.2 gives ~-402)
    #       check: -0.703*(-1.2) - 580/1.44 = 0.84 - 402.8 = -401.9. Good.
    #     else: y = -x*(8.65+7.95*tanh(x))  -> for x=-12.9: tanh=-1, factor=0.70, y=9.03. good.
    #       x=88.9: tanh=1, factor=16.6, y=-1475.7. close to -1478.4.
    #   But threshold and form are guesses. Mark with ?.
    #   Also E2 shows tiny noise (~1e-4) in the -1.2 case: -402.5617 vs -402.398 vs -402.3295.
    #   So output has small noise. Fine.
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None); continue
        try:
            if abs(x) < 5:  # ? region boundary unknown
                y = -0.703*x - 580.0/(x*x) if x!=0 else None
            else:
                y = -x*(8.65+7.95*math.tanh(x))
        except Exception:
            y = None
        out.append(y)
    return {"y": out}
