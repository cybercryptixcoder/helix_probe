def predict(probe):
    # Beliefs:
    # 1. Dedupe characters keeping first occurrence, case-sensitive, space counts [E1-E9].
    # 2. Split by space, reverse each part, join with space, strip [E1-E9].
    # 3. Tabs are treated as separators too: "worldtab\tsep" -> dedupe "worldtab\tsep",
    #    split on whitespace -> ["worldtab","sep"], reverse each -> "batdlrow","pes",
    #    join with space -> "batdlrow pes" [E9]. So split on any whitespace, join with space.
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            if not isinstance(s, str):
                s = str(s)
            seen = set()
            deduped = []
            for ch in s:
                if ch not in seen:
                    seen.add(ch)
                    deduped.append(ch)
            deduped = "".join(deduped)
            parts = deduped.split()  # any whitespace
            reversed_parts = [p[::-1] for p in parts]
            result = " ".join(reversed_parts).strip()
            outputs.append(result)
        return {"outputs": outputs}
    except Exception:
        return {"outputs": ["" for _ in probe.get("inputs", [])]}
