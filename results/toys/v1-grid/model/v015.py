def predict(probe):
    try:
        x, y = probe["start"]
        presses = probe.get("presses", "")
        walls = {(5, 6), (2, 4)}
        c_reverse = {(6, 5), (5, 5), (4, 5), (3, 5), (2, 5)}
        path = []
        for ch in presses:
            if ch == "A":
                dx, dy = 0, 1
            elif ch == "B":
                dx, dy = 2, 0
            elif ch == "C":
                if (x, y) in c_reverse:
                    dx, dy = -1, 0
                else:
                    dx, dy = 1, 0
            elif ch == "D":
                dx, dy = 0, -2
            elif ch == "E":
                if (x, y) == (5, 5):
                    dx, dy = 0, 0
                elif (x, y) == (6, 5):
                    dx, dy = 0, 0
                elif (x, y) == (5, 4):
                    dx, dy = -1, 1
                elif (x, y) == (4, 4):
                    dx, dy = 0, 0
                elif (x, y) == (7, 5):
                    dx, dy = -2, 2
                elif (x, y) == (4, 5):
                    dx, dy = 1, -1
                elif (x, y) == (5, 3):
                    dx, dy = -2, 2
                elif (x, y) == (3, 5):
                    dx, dy = 2, -2
                else:
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
