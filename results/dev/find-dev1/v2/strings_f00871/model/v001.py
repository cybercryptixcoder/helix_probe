def predict(probe):
    # f(x) = reverse(x) + "I" [E1: "hello"->"ollehI", "123"->"321I", "a b"->"a bI"]
    # Single chars: "a"->"aI", "A"->"AI", "1"->"1I", " "->"I", "!"->"!I" [E1]
    # Empty string -> "I" [E1]
    # Case preserved, reversal only [E1: "Hello"->"olleHI"]
    return {"outputs": [x[::-1] + "I" for x in probe["inputs"]]}
