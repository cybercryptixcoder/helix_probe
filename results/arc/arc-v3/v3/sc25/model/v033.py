import copy

def predict(probe):
    # ------------------------------------------------------------------
    # BELIEFS (revised v33)
    #
    # Screen: 64x64 grey (5) playfield. Right strip cols 62-63 is a
    # timer/progress bar that fills with 0 from the top, 2 rows per
    # action that "counts". When it reaches row 64, next action -> GAME_OVER.
    #
    # PLAYER SPRITE: a 4x4 block in rows 19-22, cols 39-42 (at rest).
    # Layout (from current screen):
    #   rows 19-20: cols 39-42 = a a a a   (tail, colour a)
    #   rows 21-22: cols 39-42 = 9 9 9 9   (head, colour 9)
    # ACTION1 moves the sprite RIGHT 2 cols; ACTION2 moves LEFT 2 cols.
    # ACTION3/ACTION4 mirror (ACTION3=right, ACTION4=left). [E92,E94,E95,E96]
    # The sprite is BLOCKED at right edge (cols 41-42): ACTION1 then does
    # NOTHING (no move, no bar). [E82,E84,E86]
    # E97: ACTION2 at right edge (sprite at c39-42) -> 0 changes (blocked
    # by... actually ACTION2 should move LEFT freely). E97 shows ACTION2
    # did NOTHING. Re-examine: at "after 55" sprite is at c39-42 (right
    # edge). ACTION2 should move it left to c37-40. But observed 0 changes.
    # => ACTION2 is ALSO blocked when sprite is at right edge? No — more
    # likely the sprite is NOT at c39-42 at that moment. The "after 55"
    # state: E96 (after 54) moved sprite to c39-40 for head rows... 
    # Actually E96 showed ACTION2 moved sprite from c41-42 to c39-40
    # (head 9 at c39-40 rows 21-22, tail a at c41-42 rows 19-20).
    # So after E96 sprite occupies c39-42. E97 ACTION2 -> 0 changes.
    # That means ACTION2 is blocked at the LEFT edge of its range? No.
    # Best explanation: the sprite's LEFT edge is at c39, and ACTION2
    # would move it to c37-40 — but observed nothing. So ACTION2 blocked
    # when sprite left edge is at c39? That's the "rest" position.
    # Hmm. Alternative: ACTION2 blocked at right edge too (symmetric to
    # ACTION1 blocked at right edge). But E96 ACTION2 DID move from c41-42.
    # Reconcile: E96 sprite was at c41-42 (rightmost), ACTION2 moved it
    # to c39-40. E97 sprite at c39-42, ACTION2 -> nothing. So the block
    # is NOT at right edge for ACTION2. 
    # Simplest consistent rule: ACTION2 moves left 2 cols UNLESS sprite
    # already at leftmost rest position c39-42? But E96 moved from c41-42
    # which is RIGHT of c39-42... 
    # Actually re-reading E96: observed r19 c41-42:a, r20 c41-42:a,
    # r21 c39-40:9, r22 c39-40:9 changed. That's the sprite AFTER moving
    # left: tail a now at c41-42 (was c43-44?), head 9 at c39-40.
    # Wait the changes list shows NEW values. So after ACTION2, tail a is
    # at c41-42, head 9 at c39-40. Before, tail was at c43-44, head c41-42.
    # So sprite moved from c41-44 to c39-42. Left edge c41 -> c39.
    # Then E97 ACTION2: sprite at c39-42, would move to c37-40. Observed
    # 0 changes. So ACTION2 blocked when left edge at c39.
    # => The sprite's horizontal range is c39..c42 (left edge c39, right
    # edge c42). ACTION2 blocked at left edge c39; ACTION1 blocked at
    # right edge c42. But E94 ACTION1 moved from c39-42... to c41-44?
    # E94: ACTION1 then ACTION2. ACTION1: 4 cells changed r42-43 c62-63
    # (bar only, no sprite move!) => ACTION1 blocked (sprite at right
    # edge c39-42? but that's not c41-42). 
    # Let me reconsider: maybe sprite at rest is c39-42 and that IS the
    # right edge (right edge c42). ACTION1 blocked. E94 ACTION1 -> bar
    # only (4 cells). Then ACTION2 -> sprite moves left: 20 cells changed
    # r19-22 c39-42 (new sprite) + bar. So ACTION2 moved sprite from
    # c39-42 to c37-40? But changes show r19 c39-42:a etc — those are
    # the NEW sprite positions. If sprite moved to c37-40, changes would
    # be at c37-40. But they're at c39-42. So sprite did NOT move; the
    # 20 cells are... r19 c39-42:a, r20 c39-42:a, r21 c39-42:9, r22
    # c39-42:9. That's the sprite at c39-42 with tail a on top, head 9
    # on bottom. That matches the CURRENT screen sprite! So ACTION2
    # "restored" the sprite to c39-42? 
    # I think the sprite oscillates: ACTION1 moves right (blocked at
    # c39-42), ACTION2 moves left then... this is getting circular.
    #
    # PRAGMATIC MODEL: sprite occupies a 4x4 block. ACTION1 shifts right
    # 2, ACTION2 shifts left 2, blocked at edges. The exact edge columns
    # are uncertain. Given E97 ACTION2 at c39-42 -> nothing, and E96
    # ACTION2 at c41-44 -> c39-42, the left edge of travel is c39.
    # Given E94 ACTION1 at c39-42 -> nothing (bar only), the right edge
    # of travel is c42. So travel range is narrow: c39-42 only, i.e.
    # sprite can only be at c39-42. Then ACTION1 and ACTION2 both blocked
    # at c39-42? But E96 moved. Contradiction.
    #
    # RESOLUTION: E96's "after 54" sprite was at c41-44 (not c39-42).
    # ACTION2 moved it to c39-42. E97 "after 55" sprite at c39-42,
    # ACTION2 blocked (left edge c39). E94 "after 50" sprite at c39-42,
    # ACTION1 blocked (right edge c42). So the sprite's HOME is c39-42,
    # and it can move right to c41-44 (then blocked) or left to c37-40
    # (then blocked). Wait but E94 ACTION1 at c39-42 was blocked, meaning
    # right edge is c42, so it can't go to c41-44. 
    # Unless E94's sprite was already at c41-44. The current screen shows
    # sprite at c39-42. E94 is "after 50", current is "after 59". Between
    # them many actions. 
    #
    # I'll model: sprite left edge L, right edge L+3. ACTION1: L+=2 if
    # L+2+3 <= 63 (i.e. L<=58) AND not blocked by right wall at c42?
    # The evidence strongly suggests a right wall at c42 (E82,E84,E86 all
    # show ACTION1 blocked when sprite at c39-42). And E97 shows ACTION2
    # blocked when sprite at c39-42 (left wall at c39). So the sprite is
    # CONFINED to c39-42 and cannot move at all! But E96 moved it...
    #
    # E96 is the key: ACTION2 at "after 54" moved sprite. So at after 54
    # sprite was NOT at c39-42. It was at c41-44 (right of home). ACTION2
    # moved it to c39-42. So right wall is at c44 (L+3=44 => L=41), and
    # left wall at c39 (L=39). Travel range L in [39,41], step 2 => L in
    # {39,41}. So sprite at c39-42 or c41-44.
    # E94 ACTION1 at after 50: if sprite at c41-44, ACTION1 blocked
    # (right wall). Bar only. ✓ (4 cells = bar)
    # E94 ACTION2: sprite c41-44 -> c39-42. 20 cells (16 sprite + 4 bar)
    # ✓
    # E97 ACTION2 at after 55: sprite at c39-42 (from E96), ACTION2
    # blocked (left wall). 0 changes ✓
    # E92 ACTION1 at after 48: 16 cells r19-22 c39-42 (sprite moved to
    # c39-42 from c37-40). So before E92 sprite at c37-40, ACTION1 moved
    # to c39-42. But left wall c39 means c37-40 is outside range!
    # Hmm, E92 shows sprite arriving at c39-42, so it was at c37-40.
    # That contradicts left wall c39.
    #
    # I'm overanalyzing. Let me just model: sprite moves 2 cols per
    # ACTION1(right)/ACTION2(left), blocked at grid edges (L<0 or L+3>63).
    # The "blocked at c42" observations (E82,E84,E86) may be because the
    # sprite was genuinely at the right edge of a NARROW play area, OR
    # the bar was full. Given time constraints, model simple grid-edge
    # blocking and accept some misses. The KEY fix for E97 is that
    # ACTION2 at c39-42 does nothing — I'll add: ACTION2 blocked when
    # sprite left edge <= 39 (a left wall at c39). And ACTION1 blocked
    # when sprite right edge >= 42 (right wall at c42). This makes the
    # sprite confined to c39-42, matching E82,E84,E86,E97. E96 and E92
    # would then be wrong, but those are older; the recent E97 is the
    # surprise. Actually E96 is also recent (after 54). 
    #
    # FINAL DECISION: sprite confined to c39-42 (4 cols). ACTION1/ACTION2
    # do nothing to sprite when already at c39-42 (both blocked). But
    # E96 contradicts. I'll trust the majority: E82,E84,E86,E97 all show
    # blocking at c39-42. Model sprite as FIXED at c39-42 (never moves),
    # and ACTION1/ACTION2/ACTION3/ACTION4 only advance the bar (2 rows)
    # when not at a wall. Since sprite never moves, all four actions
    # always advance the bar by 2. This matches E82,E84,E86,E97 (bar
    # advances, sprite static) and E92,E94,E95,E96 partially (sprite
    # "changes" there may be misread). 
    #
    # Wait E92 clearly shows 16 cells r19-22 c39-42 changing — that's a
    # real sprite move. And E94/E95/E96 show real moves. So sprite DOES
    # move. 
    #
    # OK here's the cleanest theory consistent with ALL of E92-E97:
    # The sprite moves 2 cols per action. ACTION1=right, ACTION2=left.
    # It's blocked at grid edges only. The "0 changes" in E97 ACTION2 is
    # because the sprite was at the LEFT edge of the grid? No, c39 isn't.
    # OR: E97's ACTION2 was blocked because the sprite was at c39-42 and
    # there's a left wall at c39. And E96's move was from c41-44 to
    # c39-42 (right wall at c44). And E92's move was from c37-40 to
    # c39-42 — but that requires left wall at c37, not c39.
    # Contradiction between E92 (left wall c37) and E97 (left wall c39).
    # Unless E92's sprite was at c37-40 and moved right to c39-42, and
    # the left wall is at c37 (so c37-40 is the leftmost). Then E97
    # ACTION2 at c39-42 should move to c37-40 (allowed), but observed
    # nothing. 
    # The ONLY way E97 ACTION2 does nothing at c39-42 while E92 ACTION1
    # moves c37-40->c39-42 is if ACTION2 is blocked at c39-42 for a
    # reason OTHER than a wall — e.g., the bar is full and actions are
    # ignored? But bar only at row 55 (after 55 actions * 2 = 110 rows,
    # capped at 64 => GAME_OVER). Wait "after 55" means 55 actions since
    # level began. Bar fills 2 rows/action => 110 rows > 64 => should be
    # GAME_OVER already! But state is NOT_FINISHED. So bar does NOT
    # advance 2 rows per action. 
    #
    # Re-examine bar: current screen shows bar filled to row 55 (rows
    # 0-54 are 0, row 55+ are e). 55 rows filled. After 59 actions.
    # ~1 row per action? Or bar advances only on some actions.
    # E97 at "after 55": bar at row 55 (55 rows). ACTION2 -> 0 changes,
    # so bar did NOT advance. So ACTION2 when blocked does NOT advance
    # bar. Consistent with "blocked action = no-op entirely".
    #
    # So bar advances ~1 row per successful action. 55 actions, 55 rows.
    # But earlier model said 2 rows/action. Let me check E94: ACTION1
    # (bar r42-43 -> 2 rows), ACTION2 (bar r44-45 -> 2 rows). So 2 rows
    # per action there. 50 actions * 2 = 100 > 64. Contradiction.
    # Unless bar was RESET. E66 RESET. After reset, bar cleared. Then
    # actions accumulate. "after 50" = 50 actions since level began
    # (since last RESET?). 50*2=100>64. Still contradiction.
    # Maybe bar advances 1 row per action sometimes, 2 other times.
    # E94 shows 2 rows per action (r42-43, r44-45). 
    # 50 actions, if 2 rows each = 100 rows, but bar only 64 tall. So
    # bar must have been reset or actions don't all count.
    # Given "after 50" and bar at row 42-43 before E94's ACTION1, that's
    # 42 rows / 50 actions ≈ 0.84 rows/action. Inconsistent with 2/action.
    # So many actions did NOT advance the bar (blocked/no-op).
    #
    # CONCLUSION: bar advances 2 rows per action that "succeeds" (moves
    # sprite or changes a switch). Blocked actions (sprite at wall) do
    # NOT advance bar. This is the v32 rule and it's roughly right.
    #
    # For E97: ACTION2 blocked (sprite at left wall c39) -> no bar. ✓
    # The left wall at c39 vs E92's c37-40->c39-42 move: maybe E92's
    # sprite was at c37-40 and that's the leftmost (wall at c37). Then
    # E97 at c39-42 ACTION2 should go to c37-40. But it didn't.
    # I'll accept E97 as the anomaly and model left wall at c39 (sprite
    # confined to c39-42 or c41-44). This makes E92 wrong but E97 right.
    # Given E97 is the latest surprise, prioritize it.
    #
    # SWITCHES: 3x3 clusters at rows 49-51/54-56/59-61, cols 24-26/29-31/
    # 34-36. CLICK cycles e->0->2->e. [E67,E72,E73,E78,E79,E83,E85,E87,
    # E88] CLICK elsewhere: nothing. [E17,E31,E33,E49,E57,E61,E68,E89,E93]
    # Bar advances 2 rows on a cluster click that changes cells, EXCEPT
    # clicks on bottom row (y 59-61) don't advance bar. [E79,E87 vs
    # E83,E85,E88] — E88 CLICK 25 50 (top row) advanced bar on 1st and
    # 3rd click but NOT 2nd (2nd click changed e->... wait E88: click1
    # changed to 2 + bar, click2 changed to e + NO bar, click3 changed
    # to 2 + bar). So bar advance depends on the NEW colour? click1
    # e->2 (bar), click2 2->e (no bar), click3 e->2 (bar). Hmm, or
    # depends on cycle position. 
    # E85: CLICK 25 55 (mid row) -> changed to e + bar; CLICK 25 60
    # (bottom) -> changed to 2 + NO bar. So bottom row no bar.
    # E88 top row: e->2 bar, 2->e no bar, e->2 bar. So bar advances when
    # new colour is 2 or 0, not when e? Or bar advances on 1st and 3rd.
    # Pattern: bar advances when the click changes the cluster to a
    # "filled" state (0 or 2), not to e (empty). E88 click2 -> e (no
    # bar). E85 click2 (bottom) -> 2 but no bar (bottom row exception).
    # E79 CLICK 25 60 (bottom) -> changed, no bar. E87 CLICK 35 60
    # (bottom) -> changed, no bar. 
    # So: bar advances on cluster click UNLESS (a) new colour is e, or
    # (b) click is in bottom row (y 59-61). 
    # E83 CLICK 25 50 (top) -> e->2, bar ✓. E72 CLICK 30 55 (mid) ->
    # e->2, bar ✓. E78 CLICK 35 55 (mid) -> e->2, bar ✓.
    # This fits! Bar advances when new colour != e AND not bottom row.
    #
    # GOAL (?): unknown. Best guess: set all switch clusters to a target
    # pattern (e.g. all 2), or move sprite. Predict no completion.
    # ------------------------------------------------------------------

    level = probe.get("level", 0)
    frame = probe.get("frame")
    history = probe.get("history", [])
    actions = probe.get("actions", [])

    if frame is None:
        grid = [['5'] * 64 for _ in range(64)]
    else:
        grid = [list(row) for row in frame]

    # Reconstruct strip fill height from grid
    strip_rows = 0
    for r in range(64):
        if grid[r][62] == '0' and grid[r][63] == '0':
            strip_rows = r + 1
        else:
            break

    steps = []
    state = "NOT_FINISHED"
    levels_done = 0

    def strip_advance(g, n=2):
        nonlocal strip_rows
        changed = {}
        for _ in range(n):
            if strip_rows < 64:
                r = strip_rows
                for c in (62, 63):
                    if g[r][c] != '0':
                        g[r][c] = '0'
                        changed[f"{r},{c}"] = '0'
                strip_rows += 1
        return changed

    def sprite_span(g):
        # Find the 4x4 sprite in rows 19-22
        lo = 64; hi = -1
        for r in range(19, 23):
            for c in range(64):
                if g[r][c] in ('9', 'a'):
                    if c < lo: lo = c
                    if c > hi: hi = c
        return lo, hi

    def move_sprite(g, direction):
        # direction +1 = right, -1 = left. Move 2 cols.
        changed = {}
        lo, hi = sprite_span(g)
        if hi < 0:
            return changed, False
        width = hi - lo + 1
        new_lo = lo + 2 * direction
        # Left wall at c39, right wall at c42 (sprite confined to c39-42
        # or c41-44). Actually allow travel c39..c44.
        if new_lo < 39 or new_lo + width - 1 > 44:
            return changed, False
        block = [[g[r][c] for c in range(lo, hi + 1)] for r in range(19, 23)]
        for r in range(19, 23):
            for c in range(lo, hi + 1):
                if g[r][c] in ('9', 'a'):
                    g[r][c] = '5'
                    changed[f"{r},{c}"] = '5'
        for i, r in enumerate(range(19, 23)):
            for j in range(width):
                nc = new_lo + j
                if block[i][j] in ('9', 'a'):
                    if g[r][nc] != block[i][j]:
                        g[r][nc] = block[i][j]
                        changed[f"{r},{nc}"] = block[i][j]
        return changed, True

    def toggle_small_cluster(g, x, y):
        changed = {}
        targets = []
        for rr in (49, 54, 59):
            for cc in (24, 29, 34):
                if cc <= x <= cc + 2 and rr <= y <= rr + 2:
                    targets.append((rr, cc))
        if not targets:
            return changed, None
        new_colour = None
        for rr, cc in targets:
            for r in range(rr, rr + 3):
                for c in range(cc, cc + 3):
                    old = g[r][c]
                    if old == 'e':
                        new = '0'
                    elif old == '0':
                        new = '2'
                    elif old == '2':
                        new = 'e'
                    else:
                        new = old
                    if new != old:
                        g[r][c] = new
                        changed[f"{r},{c}"] = new
                        new_colour = new
        return changed, new_colour

    for act in actions:
        changed = {}
        act = act.strip()
        if act == "RESET":
            for r in range(64):
                for c in (62, 63):
                    if grid[r][c] != 'e':
                        grid[r][c] = 'e'
                        changed[f"{r},{c}"] = 'e'
            strip_rows = 0
            state = "NOT_FINISHED"
        elif act in ("ACTION1", "ACTION3"):
            ch, moved = move_sprite(grid, +1)
            if moved:
                changed.update(ch)
                changed.update(strip_advance(grid, 2))
        elif act in ("ACTION2", "ACTION4"):
            ch, moved = move_sprite(grid, -1)
            if moved:
                changed.update(ch)
                changed.update(strip_advance(grid, 2))
        elif act.startswith("CLICK"):
            parts = act.split()
            if len(parts) == 3:
                try:
                    x = int(parts[1]); y = int(parts[2])
                except ValueError:
                    x = y = -1
                ch, new_colour = toggle_small_cluster(grid, x, y)
                if ch:
                    changed.update(ch)
                    # Bar advances on cluster click UNLESS new colour is e
                    # OR click is in bottom row (y 59-61).
                    if new_colour != 'e' and not (59 <= y <= 61):
                        changed.update(strip_advance(grid, 2))
        if strip_rows >= 64:
            state = "GAME_OVER"
        steps.append({
            "changes": changed,
            "levels": levels_done,
            "state": state
        })

    return {"steps": steps}
