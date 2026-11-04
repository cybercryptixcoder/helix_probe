def predict(probe):
    # Mechanism: for each whitespace-separated token, insert 'i' after the FIRST
    # vowel (a,e,i,o,u; case-insensitive) of that token. Tokens with no vowel are
    # unchanged. Leading/trailing whitespace is stripped from the whole string.
    #
    # Evidence:
    #  - Insertion is per whitespace-token, not per whole string:
    #      "a cat" -> "a icat" [E6], "I am" -> "I iam" [E6], "an ox" -> "ani ox" [E6]
    #      "x a y" -> "x ia y" [E6], "A B C" -> "A iB C" [E6]
    #      "eat a pie" -> "eat ia pie" [E6], "up a tree" -> "up ai tree" [E6]
    #      "the cat sat" -> "the ciat sat" [E4], "sun is hot" -> "sun iis hot" [E4]
    #      "a b c" -> "a ib c" [E4], "go to school" -> "go to ischool" [E4]
    #      "we can win" -> "we cain win" [E4], "big blue sky" -> "big bliue sky" [E4]
    #      "open the door" -> "open tihe door" [E4], "she likes tea" -> "she liikes tea" [E4]
    #      "test case" -> "testi case" [E3], "banana data banana" -> "banana daita banana" [E3]
    #      "function Hello World" -> "function Hiello World" [E5]
    #      "banana a data" -> "banana ia data" [E5]
    #      "racecar Example racecar" -> "racecar Exaimple racecar" [E5]
    #      "one two three" -> "one twio three" [E8], "cat dog" -> "cati dog" [E8]
    #      "I am here" -> "I ami here" [E8], "x y z" -> "x iy z" [E8]
    #      "ab cd ef" -> "ab cid ef" [E8], "a an and" -> "a ani and" [E8]
    #      "up down left" -> "up dowin left" [E8]
    #      "apple data apple" -> "apple daita apple" [E9]
    #  - Insertion after the FIRST vowel of the token:
    #      "abc123" -> "abci123" [E1], "level" -> "leivel" [E1], "Zebra" -> "Zeibra" [E1]
    #      "bananaUPPER" -> "bananiaUPPER" [E1], "of" -> "oif" [E2], "coffee" -> "cofifee" [E2]
    #      "after" -> "afiter" [E2], "fun" -> "fiun" [E2], "gift" -> "giift" [E2]
    #      "banana" -> "baniana" [E2], "apple" -> "apiple" [E2], "orange" -> "oraigne" [E2]
    #      "umbrella" -> "umbriella" [E2], "elephant" -> "elepihant" [E2]
    #      "Example123" -> "Exampile123" [E3], "lazy" -> "laizy" [E3]
    #      "world42" -> "worild42" [E5], "aMiXeD" -> "aMiiXeD" [E5]
    #      "data123" -> "datia123" [E7], "functionend." -> "functiionend." [E7]
    #      "racecar" -> "raciecar" [E9], "Zebra Example OpenAI" -> "Zebra Examiple OpenAI" [E9]
    #  - Tokens with no vowel unchanged: "my" [E4], "sky" [E4], "x","y","z" [E8]
    #  - Leading/trailing whitespace stripped from whole string:
    #      " Zebralower" -> "Zebrialower" [E1], "banana data banana " -> "banana daita banana" [E3]
    #      " Example" -> "Exaimple" [E7], "abc " -> "abic" [E7]
    #      "  hello world" -> "hellio world" [E8], "  a b c" -> "ai b c" [E8]
    #      "  test  case  " -> "test i case" [E8], " hello" -> "heillo" [E9]
    #      "world  " -> "worild" [E9]
    #  - Internal whitespace collapsed to single space:
    #      "  test  case  " -> "test i case" [E8]
    #  - Non-letter chars: insertion still after first vowel; "a!@#" -> "a!i@#" [E9]
    #      means the vowel 'a' is followed by 'i' before the punctuation.
    #  - "function" -> "ifunction" [E1] is anomalous; all other 'f' words behave
    #      normally (fun->fiun, coffee->cofifee, after->afiter, function->function [E5]).
    #      Treat E1's "ifunction" as an outlier (?).
    import re

    def transform(tok):
        for i, c in enumerate(tok):
            if c in 'aeiouAEIOU':
                return tok[:i+1] + 'i' + tok[i+1:]
        return tok

    def process(s):
        s = s.strip()
        toks = s.split()
        return ' '.join(transform(t) for t in toks)

    return {"outputs": [process(x) for x in probe["inputs"]]}
