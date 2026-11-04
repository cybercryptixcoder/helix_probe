def predict(probe):
    # f(s): lowercase all, uppercase first char of left half, insert "10" at len//2.
    # Evidence:
    # Split point = len(s)//2 [E1,E2]: ""->0, "a"->0, "ab"->1, "123"->1,
    #   "abc def"->3, "a1b2"->2, "ab cd ef"->4, "Hello World"->5,
    #   "Hello, World!"->6, "x,y,z"->2, "abc,def"->3, "ABC DEF"->3.
    # Case: lowercase everything, then uppercase s[0] iff split>=1 [E1,E2]:
    #   "A"->"10a" (split 0, no upper), "ab"->"A10b", "ABC DEF"->"Abc10 def",
    #   "AbC dEf"->"Abc10 def", "a1b2"->"A110b2".
    def transform(s):
        n = len(s)
        idx = n // 2
        low = s.lower()
        left = low[:idx]
        right = low[idx:]
        if left and left[0].isalpha():
            left = left[0].upper() + left[1:]
        return left + "10" + right
    return {"outputs": [transform(x) for x in probe["inputs"]]}
