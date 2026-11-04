def predict(probe):
    try:
        x, y = probe["start"]
        presses = probe.get("presses", "")
        walls = {(5, 6), (2, 4), (4, 1)}
        c_reverse = {(6, 5), (5, 5), (4, 5), (3, 5), (2, 5),
                     (5, 7), (4, 7), (3, 7),
                     (2, 8), (1, 8)}
        c_blocked = {(4, 3), (4, 2), (2, 7)}
        d_blocked = {(4, 1), (5, 7)}
        e_blocked = {(5, 5), (6, 5), (4, 4), (4, 3)}
        e_diag = {
            (5, 4): (-1, 1),
            (4, 5): (1, -1),
            (5, 3): (-2, 2),
            (3, 5): (2, -2),
            (6, 3): (-3, 3),
            (7, 3): (-4, 4),
            (8, 3): (-5, 5),
            (7, 4): (-3, 3),
            (6, 4): (-2, 2),
            (7, 5): (-2, 2),
            (2, 5): (3, -3),
            (5, 7): (2, -2),
        }
        path = []
        for ch in presses:
            if ch == "A":
                dx, dy = 0, 1
            elif ch == "B":
                if x == 0:
                    dx, dy = 0, 0
                else:
                    dx, dy = 2, 0
            elif ch == "C":
                if (x, y) in c_blocked or x == 0:
                    dx, dy = 0, 0
                elif (x, y) in c_reverse:
                    dx, dy = -1, 0
                else:
                    dx, dy = 1, 0
            elif ch == "D":
                if (x, y) in d_blocked:
                    dx, dy = 0, 0
                else:
                    dx, dy = 0, -2
            elif ch == "E":
                if (x, y) in e_blocked:
                    dx, dy = 0, 0
                elif (x, y) in e_diag:
                    dx, dy = e_diag[(x, y)]
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
