def predict(probe):
    # f reverses the entire string, character by character [E1]
    # Case is preserved (reversal doesn't change case) [E1: Hello->olleH, HELLO->OLLEH]
    # Spaces are preserved in place (reversal moves them) [E1: "hello world"->"dlrow olleh", "hello  world"->"dlrow  olleh"]
    # Punctuation and digits are reversed along with everything else [E1: "hello!"->"!olleh", "123"->"321"]
    # Empty string stays empty [E1]
    # Single char stays same [E1: a->a]
    try:
        return {"outputs": [s[::-1] for s in probe["inputs"]]}
    except Exception:
        return {"outputs": []}
