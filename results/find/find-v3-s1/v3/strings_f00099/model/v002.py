def predict(probe):
    # The box reverses each input string, then strips leading/trailing whitespace
    # from the result. [E1, E2, E3]
    # Evidence: "trail " -> "liart" (not " liart"); "test case  " -> "esac tset"
    # (not "  esac tset"); " lead" -> "dael " (leading space moved to end by
    # reversal, then stripped).
    return {"outputs": [s[::-1].strip() for s in probe["inputs"]]}
