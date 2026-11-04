def predict(probe):
    # Last letter of the whole string is shifted +1 [E1, E2]
    # "hello"->"hellp", "world"->"worle", "abc"->"abd" [E1]
    # "Hello"->"Hellp", "HELLO"->"HELLP", "hELLo"->"hELLp" [E1]
    # "cat"->"cau", "Buzz"->"Buza" [E2]
    # "test end."->"test end." : trailing punctuation means last char is '.', not a letter, so unchanged [E2]
    # "dog."->"dog.", "hi!"->"hi!", "yes?"->"yes?" : last char is punctuation, unchanged [E2]
    # "a1"->"a1" : last char digit, unchanged [E1, E2]
    # "1a"->"1b" : last char letter, shifted [E2]
    # "Z"->"A", "z"->"a" : wrap around [E2]
    # "two words"->"two wordt" : only the very last char of string is shifted, not each word [E1]
    # "a b c"->"a b d" : only last char of string [E1]
    # "abc123"->"abc123", "123"->"123" : last char digit, unchanged [E1]
    def shift(s):
        if not s:
            return s
        c = s[-1]
        if 'a' <= c <= 'y':
            return s[:-1] + chr(ord(c) + 1)
        if c == 'z':
            return s[:-1] + 'a'
        if 'A' <= c <= 'Y':
            return s[:-1] + chr(ord(c) + 1)
        if c == 'Z':
            return s[:-1] + 'A'
        return s
    out = []
    for s in probe.get("inputs", []):
        out.append(shift(s))
    return {"outputs": out}
