def predict(probe):
    def transform(s):
        try:
            # Try removing one duplicate adjacent character (first occurrence)
            out = s
            for i in range(len(s) - 1):
                if s[i] == s[i + 1]:
                    out = s[:i] + s[i + 1:]
                    break
            # Append 'h' unless already ends with 'h'
            if not out.endswith('h'):
                out = out + 'h'
            return out
        except Exception:
            return s
    try:
        return {"outputs": [transform(x) for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
