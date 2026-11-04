import math

def predict(probe):
    # Observations: y appears to be round(x) - 39? Let's check E1.
    # x=88.2 -> 49 ; 88.2-39.2=49. Hmm.
    # x=66.0 -> 27 ; 66-39=27
    # x=-20.3 -> -60 ; -20.3-39.7=-60
    # x=-61.7 -> -101 ; -61.7-39.3=-101
    # x=2.9 -> -37 ; 2.9-39.9=-37
    # x=-24.3 -> -64 ; -24.3-39.7=-64
    # x=72.7 -> 33 ; 72.7-39.7=33
    # x=-50.4 -> -90 ; -50.4-39.6=-90
    # x=-6.0 -> -45 ; -6-39=-45
    # x=21.3 -> -18 ; 21.3-39.3=-18
    # Looks like y = round(x) - 39? Check: round(88.2)=88, 88-39=49 ✓
    # round(66)=66-39=27 ✓
    # round(-20.3)=-20, -20-39=-59 ✗ (observed -60)
    # Try floor(x)-39: floor(88.2)=88-39=49 ✓; floor(66)=27 ✓; floor(-20.3)=-21-39=-60 ✓
    # floor(-61.7)=-62-39=-101 ✓; floor(2.9)=2-39=-37 ✓; floor(-24.3)=-25-39=-64 ✓
    # floor(72.7)=72-39=33 ✓; floor(-50.4)=-51-39=-90 ✓; floor(-6)=-6-39=-45 ✓
    # floor(21.3)=21-39=-18 ✓
    # So y = floor(x) - 39.
    # ? No evidence of a special interval yet; assume uniform.
    out = []
    for v in probe.get("x", []):
        try:
            out.append(math.floor(v) - 39)
        except Exception:
            out.append(None)
    return {"y": out}
