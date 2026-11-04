def predict(probe):
    # Appends "ny" to every input string [E1, E2, E3]
    # Leading and trailing spaces are stripped before appending "ny" [E2, E4]
    # Internal whitespace (spaces, tabs) is preserved [E4]
    # Tabs are NOT stripped (only spaces?) — "a\tb" -> "a\tbny" [E4]
    # " " -> "ny" and "  " -> "ny" consistent with stripping spaces [E2, E4]
    # " a" -> "any", "a " -> "a ny"?? wait: "a " -> "a ny" means trailing space kept?
    # Re-check E4: "a " -> "a ny" (space kept!), " a" -> "any" (leading stripped)
    # " a " -> "a ny" (leading stripped, trailing kept)
    # "  a" -> "any" (leading stripped)
    # " hello" -> "hellony" (leading stripped)
    # "hello " -> "hello ny" (trailing kept)
    # "  " -> "ny" (all spaces stripped -> empty)
    # So: only LEADING spaces are stripped, trailing spaces preserved.
    # But " " -> "ny" and "  " -> "ny": all-space -> empty, consistent with lstrip only.
    # Tabs: "a\tb" -> "a\tbny", no leading tab to strip; unknown if lstrip removes tabs.
    # Use lstrip(" ") to strip only leading spaces (not tabs) — "?" for tabs.
    return {"outputs": [s.lstrip(" ") + "ny" for s in probe["inputs"]]}
