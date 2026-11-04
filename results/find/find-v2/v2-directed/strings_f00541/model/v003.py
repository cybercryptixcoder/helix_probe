def predict(probe):
    # Strip outer whitespace [E1: "  spaced  "->"spaced"]
    # Remove ALL uppercase 'H' characters (not just leading) [E2,E4,E5]
    #   "Hello"->"ello", "HELLO"->"ELLO", "HH"->"", "AH"->"A", "aH"->"a",
    #   "HHello"->"ello", "hello H"->"hello ", "H H"->" ", "H"->""
    # Lowercase 'h' untouched [E1: "hello"->"hello"]
    # Other uppercase letters untouched [E3: "Bello"->"Bello", ...]
    out = []
    for s in probe.get("inputs", []):
        try:
            t = s.strip().replace("H", "")
            out.append(t)
        except Exception:
            out.append(s)
    return {"outputs": out}
