def predict(probe):
    # Appends "ny" to every input [E1, E2]
    # Exception: an input consisting only of spaces returns just "ny" [E2]
    #   (the spaces are stripped/ignored before appending) [E2]
    # Non-space content is preserved verbatim, then "ny" appended [E1, E2]
    return {"outputs": [("ny" if x.strip() == "" else x + "ny") for x in probe["inputs"]]}
