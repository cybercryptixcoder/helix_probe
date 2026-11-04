def predict(probe):
    try:
        out = []
        for s in probe.get("inputs", []):
            words = s.split()
            if not words:
                out.append("")
                continue
            reversed_words = [w[::-1] for w in words]
            joined = " ".join(reversed_words)
            # Remove duplicate characters (keep first occurrence), preserving spaces
            seen = set()
            deduped = []
            for ch in joined:
                if ch == " ":
                    deduped.append(ch)
                elif ch not in seen:
                    seen.add(ch)
                    deduped.append(ch)
            out.append("".join(deduped))
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
