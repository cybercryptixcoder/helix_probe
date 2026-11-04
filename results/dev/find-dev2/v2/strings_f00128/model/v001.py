def predict(probe):
    # Capitalize first letter of each word [E1: hello->He10llo, world->Wo10rld]
    # Insert "10" after the first letter of each word [E1: He10llo, Wo10rld, Te10st!]
    # "10" inserted after first char even for single char words [E1: x->10x]
    # Digits: "10" inserted after first digit of each digit-run? [E1: 12345->1210345, abc123->Abc10123]
    #   - 12345 -> 1210345: "10" after first char "1" => "1"+"10"+"2345" = "1210345" yes
    #   - abc123 -> Abc10123: after capitalize "Abc123", insert "10" after first char "A" => "A10bc123"? but observed "Abc10123"
    #   Hmm. Let's re-derive.
    # "a b c" -> "A 10b c": capitalize each word: "A B C", then insert 10 after first letter of... only "b"? 
    #   Actually "A 10b c" = "A " + "10" + "b c". So 10 inserted before "b", i.e., after the space? 
    # Let's reconsider: maybe insert "10" after the first character of the whole string, then capitalize words.
    #   hello -> "h10ello" -> capitalize -> "H10ello"? but observed "He10llo". No.
    # Try: capitalize each word, then insert "10" after the second character of each word?
    #   hello->Hello, insert after 2 chars: "He10llo" yes
    #   world->World -> "Wo10rld" yes
    #   test!->Test! -> "Te10st!" yes
    #   x->X, only 1 char, insert after 1 char: "X10"? observed "10x". Hmm.
    #   two words -> "Two Words" -> "Two 10Words"? observed "Two 10words". 
    # Let's look again: "two words" -> "Two 10words". Capitalize first word only? "Two words", then insert 10 after "Two "? 
    #   Actually "Two 10words": "Two " + "10" + "words". So 10 inserted before "words", i.e., after the space.
    # "a b c" -> "A 10b c": "A " + "10" + "b c". 10 inserted after first space.
    # So maybe: capitalize first letter of string, then insert "10" after the first space? But hello has no space.
    # Let's tabulate positions of "10":
    #   hello -> He|10|llo : after 2 chars
    #   world -> Wo|10|rld : after 2 chars
    #   Hello -> He|10|llo : after 2 chars
    #   HELLO -> He|10|llo : after 2 chars (and lowercased rest!)
    #   abc123 -> Abc|10|123 : after 3 chars
    #   a b c -> A |10|b c : after 2 chars (space is char 2)
    #   test! -> Te|10|st! : after 2 chars
    #   12345 -> 1|10|2345 : after 1 char
    #   x -> |10|x : after 0 chars
    #   two words -> Two |10|words : after 4 chars
    # Hmm inconsistent. Let's think: maybe insert "10" before the first vowel? 
    #   hello: first vowel 'e' at index 1 -> He|10|llo? insert before e gives H10ello no. After e: He10llo yes.
    #   world: first vowel 'o' at index 1 -> Wo10rld yes (after o)
    #   Hello: same
    #   HELLO: lowercased to Hello, same
    #   abc123: first vowel 'a' at 0 -> after a: A10bc123? observed Abc10123. No.
    #   Hmm abc123 -> Abc10123. "10" before "123"? after "Abc". 
    #   a b c -> A 10b c: "10" before "b". 
    #   two words -> Two 10words: "10" before "words".
    #   Maybe insert "10" before the first letter that comes after a space or digit? 
    #   abc123: after "abc" comes digit "1" -> insert before "1": "Abc"+"10"+"123" yes!
    #   a b c: after "a " comes "b" -> "A "+"10"+"b c" yes!
    #   two words: after "two " comes "w" -> "Two "+"10"+"words" yes!
    #   hello: no space/digit... hmm.
    #   Maybe insert "10" before the second letter? hello->He10llo (before 'l', 3rd char). 
    #   Let's think differently: maybe it's "insert 10 before the last consonant cluster"? too vague.
    # Try: insert "10" before the first occurrence of a "boundary": after first letter if word, ...
    # Actually maybe rule: capitalize first letter, lowercase rest (per word? "two words"->"Two words" only first word capitalized).
    #   "a b c" -> "A b c" then insert 10 after first space -> "A 10b c" yes.
    #   "two words" -> "Two words" insert 10 after first space -> "Two 10words" yes.
    #   "abc123" -> "Abc123" no space, insert 10 before first digit -> "Abc10123" yes.
    #   "12345" -> "12345" no space, insert 10 before first digit? but it's all digits. Observed "1210345": insert after first digit.
    #   "hello" -> "Hello" no space/digit. Insert 10 after 2nd char -> "He10llo".
    #   "x" -> "X" no space/digit, only 1 char. Insert 10 before? "10x" yes.
    # Hmm, for hello why after 2nd char? Maybe insert 10 after first vowel? hello: after 'e' -> He10llo yes. 
    #   world: after 'o' -> Wo10rld yes. test!: after 'e' -> Te10st! yes. 
    #   x: no vowel -> insert at start "10x" yes.
    #   abc123: vowel 'a' at 0, after 'a' -> A10bc123? but observed Abc10123. Contradiction.
    # Let's reconsider abc123. Maybe digits handled separately: split into letters and digits? "abc"+"123". 
    #   Capitalize "abc"->"Abc", then insert 10 before digits: "Abc"+"10"+"123" = "Abc10123" yes.
    #   12345: all digits, insert 10 after first digit: "1"+"10"+"2345" yes.
    # So rule: process string, capitalize first letter, lowercase rest? "HELLO"->"Hello" yes (only first cap).
    #   "two words" -> "Two words" yes.
    #   "a b c" -> "A b c" yes.
    # Then insert "10":
    #   - if there's a space: after the first space
    #   - elif there's a digit: before the first digit (if letters precede), or after first digit if starts with digit
    #   - else (pure letters): after the first vowel? or after 2nd char?
    #   hello->He10llo (after 'e', 2nd char). world->Wo10rld (after 'o', 2nd char). test!->Te10st! (after 'e', 2nd char).
    #   x->10x (before x, since 1 char).
    #   Maybe "after the first vowel" works for hello, world, test!. For x no vowel -> before.
    #   But what about a word like "sky"? no vowel. "rhythm"? 
    # Let's test "after first vowel" vs "after 2nd char": both fit hello/world/test!.
    #   For "x" (1 char, no vowel): "10x" = insert before. If "after 2nd char" but only 1 char, insert at... start? 
    #   Hmm "after first vowel" for x: no vowel, insert at start -> "10x" yes.
    # I'll go with: insert after first vowel if exists, else at start. But abc123 contradicts (vowel 'a' at start).
    #   Unless digits take priority: if digit present, handle digit rule.
    # Let me settle on priority: space > digit > vowel.
    #   abc123: has digit, no space -> digit rule: before first digit (letters before) -> Abc10123 yes.
    #   12345: digit, no space, starts with digit -> after first digit -> 1210345 yes.
    #   a b c: space -> after first space -> A 10b c yes.
    #   two words: space -> Two 10words yes.
    #   hello: no space/digit -> after first vowel -> He10llo yes.
    #   x: no space/digit/vowel -> at start -> 10x yes.
    # Good enough. Capitalization: first letter upper, rest lower (whole string).
    #   "HELLO"->"Hello" yes. "abc123"->"Abc123" yes.
    import re
    def transform(s):
        if not s:
            return s
        t = s[0].upper() + s[1:].lower()
        if ' ' in t:
            i = t.index(' ')
            return t[:i+1] + '10' + t[i+1:]
        m = re.search(r'\d', t)
        if m:
            i = m.start()
            if i == 0:
                return t[:1] + '10' + t[1:]
            return t[:i] + '10' + t[i:]
        m = re.search(r'[aeiouAEIOU]', t)
        if m:
            i = m.start()
            return t[:i+1] + '10' + t[i+1:]
        return '10' + t
    return {"outputs": [transform(x) for x in probe["inputs"]]}
