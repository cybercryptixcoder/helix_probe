def predict(probe):
    # Rule: reverse each whitespace-separated word in place, preserving
    # spaces and word order. [E1: "hello"->"oolleh", "hello world"->"olleh ddlrow",
    # "one two three"->"eno owt eeerht", "a"->"aa" (single char reversed = itself),
    # case preserved: "Hello"->"oolleH", "HELLO"->"OOLLEH"]
    # Note "a"->"aa" is odd: reversing "a" gives "a", but observed "aa".
    # Hmm, "abc"->"ccba" (4 chars from 3). So it seems each word is reversed
    # AND something adds a char? "hello"(5)->"oolleh"(6), "world"(5)->"ddlrow"(6),
    # "abc"(3)->"ccba"(4), "a"(1)->"aa"(2), "cat"(3)->"ttac"(4), "dog"(3)->"ggod"(4).
    # Pattern: output = reverse(word) with the last char of reverse duplicated?
    # reverse("hello")="olleh", output "oolleh" = "o"+"olleh"? No: "oolleh" vs "olleh".
    # "olleh" -> "oolleh": extra 'o' at front. reverse("abc")="cba", output "ccba" = "c"+"cba".
    # reverse("a")="a", output "aa" = "a"+"a". reverse("cat")="tac", output "ttac"="t"+"tac".
    # So: output = first_char_of_reverse + reverse(word) = last_char_of_word + reverse(word).
    # Check "world": reverse="dlrow", last char 'd', output "ddlrow" = "d"+"dlrow". Yes!
    # "HELLO": reverse="OLLEH", last char 'O', output "OOLLEH". Yes!
    # "Hello": reverse="olleH", last char 'o', output "oolleH". Yes!
    # So each word w -> w[-1] + w[::-1].
    def fword(w):
        if not w:
            return w
        return w[-1] + w[::-1]
    import re
    out = []
    for s in probe.get("inputs", []):
        # split preserving whitespace
        parts = re.split(r'(\s+)', s)
        out.append(''.join(p if p.isspace() or p == '' else fword(p) for p in parts))
    return {"outputs": out}
