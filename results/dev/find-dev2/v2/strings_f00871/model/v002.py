def predict(probe):
    # The box reverses the order of WORDS, not characters [E2]
    # Within each word, characters keep their order [E2: "ab cd"->"ba dc"? no...]
    # Wait: "ab cd"->"ba dc" means each word reversed too? No: "ab"->"ba", "cd"->"dc"
    # Actually "ab cd"->"ba dc": word order kept, each word reversed? "ab"->"ba" yes, "cd"->"dc" yes
    # But "one two three"->"eno owt eerht": word order kept, each word reversed
    # And "a b c"->"a b c": each single char reversed = same
    # "hello  world"->"olleh dlrow": double space collapsed to single, each word reversed
    # " leading"->"gnidael": leading space dropped, word reversed
    # "trailing "->"gniliart": trailing space dropped, word reversed
    # "hello world!"->"olleh !dlrow": hmm, "world!"->"!dlrow" reversed, but space before !
    #   Actually "hello world!" -> reverse whole string = "!dlrow olleh", but observed "olleh !dlrow"
    #   That's word order reversed AND each word reversed? "hello"->"olleh", "world!"->"!dlrow", order: olleh !dlrow
    #   So word order reversed, each word reversed = full char reverse... but "hello  world"->"olleh dlrow" not "dlrow olleh"
    # Contradiction. Let me reconsider.
    # E1: "hello world"->"olleh dlrow": word order KEPT, each word reversed
    # E2: "hello world!"->"olleh !dlrow": word order KEPT ("hello" first->"olleh" first), each word reversed
    #   "world!"->"!dlrow" yes reversed. So "olleh !dlrow" = word order kept, each word reversed. Consistent!
    # So: split on whitespace, reverse each word's characters, join with single space, append 'I'
    # "hello  world"-> split gives ["hello","world"], join single space -> "olleh dlrow" [E2]
    # " leading"-> ["leading"] -> "gnidael" [E2]
    # "trailing "-> ["trailing"] -> "gniliart" [E2]
    # " "-> [] -> "" + "I" = "I" [E1]
    # "abc123"->"321cba" reversed word [E1]
    # "A1!"->"!1A" [E1]
    out = []
    for s in probe.get("inputs", []):
        try:
            words = s.split()
            out.append(" ".join(w[::-1] for w in words) + "I")
        except Exception:
            out.append("I")
    return {"outputs": out}
