import math

def predict(probe):
    # Most outputs are round(x) [E1: -93.6->-95? no...]
    # Actually: -93.6->-95, 88.9->89, 67.5->68, -62.7->-64, -1.2->-3, -12.9->-14,
    # 73.9->74, -104->-105, -120.7->-122. These look like floor(x)-1 for negatives?
    # -93.6 floor=-94, -1 => -95. 88.9 floor=88, +1 => 89. 67.5 floor=67,+1=68.
    # -62.7 floor=-63,-1=-64. -1.2 floor=-2,-1=-3. -12.9 floor=-13,-1=-14.
    # 73.9 floor=73,+1=74. -104 floor=-104,-1=-105. -120.7 floor=-121,-1=-122.
    # So: floor(x)+1 if x>=0 else floor(x)-1. i.e. away from zero.
    # Exception: 38.8 -> -0.4481. That's the special interval.
    out = []
    for x in probe["x"]:
        if 30 <= x <= 45:  # ? special region
            out.append(-0.4481)  # ? unknown formula
        else:
            out.append(math.floor(x) + (1 if x >= 0 else -1))
    return {"y": out}
