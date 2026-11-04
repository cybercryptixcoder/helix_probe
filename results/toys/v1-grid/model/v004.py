def predict(probe):
    try:
        x, y = probe["start"]
        presses = probe.get("presses", "")
        walls = {(5, 6)}
        path = []
        for ch in presses:
            if ch == "A":
                dx, dy = 0, 1
            elif ch == "B":
                dx, dy = 2, 0
            elif ch == "C":
                # C moves +x normally, but from (5,5) it moves -x (E7)
                if (x, y) == (5, 5):
                    dx, dy = -1, 0
                else:
                    dx, dy = 1, 0
            elif ch == "D":
                dx, dy = 0, -2
            elif ch == "E":
                dx, dy = -2, 0
            else:
                dx, dy = 0, 0
            nx, ny = x + dx, y + dy
            if 0 <= nx <= 8 and 0 <= ny <= 8 and (nx, ny) not in walls:
                x, y = nx, ny
            path.append([x, y])
        return {"start": list(probe["start"]), "path": path}
    except Exception:
        return {"start": probe.get("start", [0, 0]), "path": []}
