def predict(probe):
    # A moves up 1 (y+1) [E1]
    # B moves right 2 (x+2) [E1]
    # C moves right 1 (x+1) [E1]
    # D moves down 2 (y-2) [E1]
    # E moves left 1 (x-1) [E1]
    # Walls exist; movement into a wall is blocked (character stays). [library tip]
    # At least one button behaves differently in some region. [?]
    x, y = probe["start"]
    path = []
    for p in probe["presses"]:
        if p == "A":
            nx, ny = x, y + 1
        elif p == "B":
            nx, ny = x + 2, y
        elif p == "C":
            nx, ny = x + 1, y
        elif p == "D":
            nx, ny = x, y - 2
        elif p == "E":
            nx, ny = x - 1, y
        else:
            nx, ny = x, y
        # clamp to board
        nx = max(0, min(8, nx))
        ny = max(0, min(8, ny))
        x, y = nx, ny
        path.append([x, y])
    return {"start": probe["start"], "path": path}
