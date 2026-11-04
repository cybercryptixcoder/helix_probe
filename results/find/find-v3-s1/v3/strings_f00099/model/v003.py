def predict(probe):
    # The box reverses each input string, then strips leading whitespace only
    # (not trailing). [E2: "trail " -> "liart" (trailing space stripped after
    # reversal becomes leading); " lead" -> "dael " (leading space becomes
    # trailing, preserved). E4: "  x  " -> "x  " (leading stripped, trailing
    # kept). E3: "test case  " -> "esac tset" (trailing spaces become leading
    # after reversal, stripped).]
    return {"outputs": [s[::-1].lstrip() for s in probe["inputs"]]}
