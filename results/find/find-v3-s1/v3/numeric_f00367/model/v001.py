def predict(probe):
    # Linear through origin: y = 2.3 * x [E1]
    # Check: -93.6*2.3=-215.28 vs -212.94 (close); 88.9*2.3=204.47 vs 215.16
    # Ratios: -212.94/-93.6=2.275, 215.16/88.9=2.420, 163.8/67.5=2.427,
    # -138.78/-62.7=2.213, 8.82/-1.2=-7.35, -19.26/-12.9=1.493,
    # 94.92/38.8=2.446, 179.16/73.9=2.424, -237.9/-104=2.287, -277.98/-120.7=2.303
    # Not constant ratio -> not pure linear. Try y = 2.3x + c? 
    # Fit: slope ~2.3, but small-x points deviate. Maybe y = 2.3x + small offset.
    # Actually -1.2 -> 8.82 and -12.9 -> -19.26 suggest something else near 0.
    # Try y = 2.3*x + 10*sin? Let's just fit linear a*x+b.
    # Using two points: (88.9,215.16),(67.5,163.8): slope=2.404, b=-0.6
    # (-104,-237.9),(-120.7,-277.98): slope=2.399, b=11.6
    # Hmm. Try y = 2.4x + b with b varying... 
    # -1.2->8.82: 2.4*-1.2=-2.88, need +11.7
    # -12.9->-19.26: 2.4*-12.9=-30.96, need +11.7
    # 38.8->94.92: 2.4*38.8=93.12, need +1.8
    # 67.5->163.8: 2.4*67.5=162, need +1.8
    # 73.9->179.16: 2.4*73.9=177.36, need +1.8
    # 88.9->215.16: 2.4*88.9=213.36, need +1.8
    # -62.7->-138.78: 2.4*-62.7=-150.48, need +11.7
    # -93.6->-212.94: 2.4*-93.6=-224.64, need +11.7
    # -104->-237.9: 2.4*-104=-249.6, need +11.7
    # -120.7->-277.98: 2.4*-120.7=-289.68, need +11.7
    # So offset is 1.8 for x>=~38, 11.7 for x<=~-62. Middle region?
    # -1.2 and -12.9 give 11.7. So offset 11.7 for x<~0, 1.8 for x>~38.
    # Transition somewhere. Try y = 2.4x + 1.8 + 9.9*(x<0)? 
    # -1.2: -2.88+1.8+9.9=8.82 ✓
    # -12.9: -30.96+1.8+9.9=-19.26 ✓
    # 38.8: 93.12+1.8=94.92 ✓
    # -62.7: -150.48+1.8+9.9=-138.78 ✓
    # All fit! So y = 2.4x + 1.8 + 9.9 if x<0 else 2.4x+1.8
    # Boundary: need to check where. -1.2 uses +9.9, 38.8 doesn't. 
    # Guess boundary at 0.
    out = []
    for x in probe["x"]:
        y = 2.4 * x + 1.8 + (9.9 if x < 0 else 0.0)
        out.append(y)
    return {"y": out}
