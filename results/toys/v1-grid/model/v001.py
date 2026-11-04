def predict(probe):
    try:
        x, y = probe["start"]
        presses = probe.get("presses", "")
        offsets = {
            "A": (0, 1),
            "B": (2, 0),
            "C": (1, 0),
            "D": (0, -2),
            "E": (-2, 0),
        }
        path = []
        for ch in presses:
            dx, dy = offsets.get(ch, (0, 0))
            nx, ny = x + dx, y + dy
            # Assume no walls known yet; move if in bounds, else stay
            if 0 <= nx <= 8 and 0 <= ny <= 8:
                x, y = nx, ny
            path.append([x, y])
        return {"start": list(probe["start"]), "path": path}
    except Exception:
        return {"start": probe.get("start", [0, 0]), "path": []}
