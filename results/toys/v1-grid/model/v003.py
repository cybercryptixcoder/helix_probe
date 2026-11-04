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
        # Known walls / cells that block movement (best guess from evidence)
        walls = {(5, 6)}
        path = []
        for ch in presses:
            dx, dy = offsets.get(ch, (0, 0))
            nx, ny = x + dx, y + dy
            if 0 <= nx <= 8 and 0 <= ny <= 8 and (nx, ny) not in walls:
                x, y = nx, ny
            path.append([x, y])
        return {"start": list(probe["start"]), "path": path}
    except Exception:
        return {"start": probe.get("start", [0, 0]), "path": []}
