def predict(probe):
    # Observations from E1:
    # - "hello" -> "helo": one 'l' removed (double letters collapsed?)
    # - "Hello" -> "Heloh": no collapse, 'h' appended
    # - "HELLO" -> "HELOh": 'LL' collapsed to 'L', 'h' appended
    # - "two words" -> "two rdsh": 'wo' -> 'rds'? unclear; 'h' appended
    # - "hello world" -> "helo wrd": 'll'->'l', 'o' dropped in 'world', 'h' not appended?
    # - "123" -> "123h": 'h' appended
    # - "A1!" -> "A1!h": 'h' appended
    # - "a b c" -> "a bch": 'h' appended
    # - "test" -> "tesh": 't' dropped, 'h' appended
    # - "Test" -> "Testh": 'h' appended
    #
    # Hypothesis: box appends 'h' generally, but some transformation happens
    # to lowercase content. Hard to pin down from one experiment.
    # Best guess: append 'h' to every input. (Doesn't explain "hello"->"helo",
    # "two words"->"two rdsh", "hello world"->"helo wrd", "test"->"tesh".)
    # ? Marking uncertainty.
    out = []
    for s in probe.get("inputs", []):
        out.append(s + "h")
    return {"outputs": out}
