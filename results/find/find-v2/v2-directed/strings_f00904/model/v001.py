def predict(probe):
    # The box reverses the string [E1: hello->olleh, two words->sdrow owt, 123->321]
    # Single characters are unchanged under reversal [E1: a->a, A->A, !->!]
    # Case is preserved, not transformed [E1: Hello->olleH, HELLO->OLLEH]
    return {"outputs": [s[::-1] for s in probe["inputs"]]}
