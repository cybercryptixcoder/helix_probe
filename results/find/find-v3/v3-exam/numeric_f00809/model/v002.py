import math

def predict(probe):
    # Beliefs:
    # - Outputs look like noise in [-0.26, 0.19] with no smooth structure [E8, E10]:
    #   tiny x offsets (0.01 apart) give wildly different y, so f is not smooth.
    # - No periodicity: same residue mod 10 gives different y [E6].
    # - No clear decay/amplitude trend with |x| [E2, E9].
    # - Mean is roughly 0; distribution looks roughly uniform-ish in [-0.25,0.2].
    # Best guess: deterministic pseudo-random function of x (hash-like), not smooth.
    # Model as a hash of x -> value in [-0.25, 0.2]. Use a simple integer hash of
    # x scaled to 1e-6 to be reproducible and deterministic.
    out = []
    for x in probe["x"]:
        try:
            k = int(round(x * 1000000))
            # 64-bit mixing
            h = (k * 2654435761) & 0xFFFFFFFF
            h ^= (h >> 15)
            h = (h * 2246822519) & 0xFFFFFFFF
            h ^= (h >> 13)
            h = (h * 3266489917) & 0xFFFFFFFF
            h ^= (h >> 16)
            u = h / 0xFFFFFFFF  # in [0,1]
            y = -0.25 + 0.45 * u
        except Exception:
            y = None
        out.append(y)
    return {"y": out}
