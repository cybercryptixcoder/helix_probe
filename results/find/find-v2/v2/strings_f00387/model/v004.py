def predict(probe):
    # Lowercase the whole string [E1-E4]
    # Delete every 'm' (both cases) from the string [E4: "mama"->"Aa", "m"->"", "mm"->"",
    #   "am"->"A", "Ma"->"Ma"?? wait "Ma"->"Ma" keeps M!]
    # Recheck E4: "Ma"->"Ma" (M kept), "aM"->"Am" (M kept, then cap first->A, m->? )
    #   "aM": lower "am", delete m -> "a", cap first -> "A". ✓ (M was deleted)
    #   "Ma": lower "ma", delete m -> "a", cap first -> "A"? but observed "Ma". ✗
    # Hmm. "Ma"->"Ma". So 'm' at index 0 (of lowercased) is KEPT and capitalized.
    #   "mama": lower "mama", keep idx0 'm', delete others -> "ma", cap -> "Ma"? but observed "Aa". ✗
    # So "mama"->"Aa": the leading 'm' was ALSO deleted. Contradicts "Ma"->"Ma".
    # Difference: "Ma" input has uppercase M at index 0; "mama" has lowercase m at index 0.
    #   "m"->"" (lowercase m deleted). "mm"->"" (both deleted). 
    #   "Ma"->"Ma": uppercase M kept (becomes 'M' after cap? or kept as is).
    #   "aM"->"Am": uppercase M -> deleted? "aM" lower "am" delete m -> "a" cap "A". 
    #     But if uppercase M kept: "aM" -> "aM" -> cap "AM"? observed "Am". So M deleted, then 'a'->'A'? 
    #     "Am" = A + m. Hmm 'm' present! So "aM"->"Am": the M became 'm' (lowercased) and kept?
    # Let's think differently: maybe delete lowercase 'm' from ORIGINAL string, then lowercase, then cap.
    #   "mama": delete lowercase m -> "aa", lower "aa", cap "Aa" ✓
    #   "m": delete -> "", ✓
    #   "mm": delete -> "", ✓
    #   "am": delete m -> "a", cap "A" ✓
    #   "Ma": no lowercase m -> "Ma", lower "ma", cap "Ma" ✓
    #   "aM": no lowercase m -> "aM", lower "am", cap "Am" ✓
    #   "summer": delete m's -> "suer", cap "Suer" ✓
    #   "Miami": delete lowercase m -> "Miai", lower "miai", cap "Miai" ✓
    #   "m&m": delete m's -> "&", cap "&" ✓
    #   "mama mia": delete m's -> "a ia", cap "Aa ia" ✓
    #   "Example123": delete lowercase m -> "Exaple123", lower "exaple123", cap "Exaple123" ✓
    #   "  multiple   spaces  ": delete m -> "  ultiple   spaces  ", lower same,
    #     starts with ws so no cap -> "  ultiple   spaces  " ✓
    #   "MiXeD case": no lowercase m (M uppercase) -> "MiXeD case", lower "mixed case",
    #     cap "Mixed case" ✓
    #   " Zebralower": no m, lower " zebralower", starts ws no cap ✓
    # All consistent! Rule: delete lowercase 'm' from original, then lowercase, then
    #   capitalize first char if original doesn't start with whitespace.
    out = []
    for s in probe["inputs"]:
        t = s.replace('m', '')
        t = t.lower()
        if t and not s[:1].isspace():
            t = t[0].upper() + t[1:]
        out.append(t)
    return {"outputs": out}
