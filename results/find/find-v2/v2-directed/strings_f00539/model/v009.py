def predict(probe):
    # Collapse runs of identical letters (case-sensitive) [E1,E2,E10]
    # Single word: collapse; append 'h' unless the collapsed word is
    #   all-lowercase, ends in o/y, AND was changed by collapse [E9,E10]
    #   (hello->helo no h; jello->jelo... wait jello->jeloh has h! [E10])
    #   E10: jello->jeloh (h!), hello->helo (no h), hallo->halo (no h),
    #   hullo->hulo (no h), yellow->yelowh (h), fellow->felowh (h),
    #   follow->folwh (h). So single-word suppression is NOT just
    #   "changed ends o/y". hello/hallo/hullo suppress; jello/yellow/
    #   fellow/follow don't. Difference: hello/hallo/hullo start with 'h'!
    #   So single-word: suppress h iff all-lower, ends o/y, changed, AND
    #   starts with 'h' [E10]. (hello,hallo,hullo start h -> suppress;
    #   jello,yellow,fellow,follow don't start h -> keep h.)
    # Multi-word: first word collapsed; later words filtered to remove chars
    #   whose lowercase appears in first word, then collapsed, concatenated [E3,E4]
    # h appended to tail unless first word suppresses OR last word suppresses.
    # First word suppresses iff all-lower, ends o/y, changed, starts 'h' [E8]
    # Last word suppression: E12/E13/E14/E16/E17 show tails that suppress:
    #   helo (hello), hlo (hallo), hulo (hullo) -> start with 'h' AND end o/y
    #   AND changed. Tails that keep h: jelo, yelow, felow, folw, meo, demo,
    #   solo, polo, celo, kilo, yoyo, etc. -> do NOT start with 'h'.
    #   So SAME rule: suppress iff all-lower, ends o/y, changed, starts 'h'.
    #   Check E15 (y-enders): happy->hpy (no h, but ends y changed, starts h?
    #   'happy' starts h! -> suppress -> 'hpy' no h. matches!)
    #   city->iyh (starts c, keep h). baby->byh. berry->beryh. cherry->hery
    #   (cherry starts c, but filtered by 'cat' removes c,a,t -> 'herry' ->
    #   collapse 'hery', starts h, ends y, changed -> suppress? observed
    #   'cat hery' no h! yes suppress. good.)
    #   story->soryh (starts s keep). party->pryh. day->dyh. play->plyh.
    #   toy->oyh. All consistent with "starts h after filter+collapse".
    #   E16: dog hello -> dog hel (filtered: dog letters d,o,g; hello ->
    #   remove o -> 'hell' -> collapse 'hel', ends l, not o/y -> add h?
    #   observed 'dog hel' no h! Hmm. 'hel' ends l. Why no h?
    #   Wait first word 'dog' - does it suppress? dog all-lower ends g not o/y.
    #   tail 'hel' ends l -> should add h -> 'helh'? observed 'hel'. 
    #   Hmm. Maybe h-append suppressed when tail is empty-ish? Or maybe
    #   when tail ends in consonant AND ... Let me check E1: 'two words' ->
    #   'two rdsh' (h added, tail 'rds' ends s). 'hello world' -> 'helo wrd'
    #   (no h! first word hello suppresses). 'a b c' -> 'a bch' (h added).
    #   So 'dog hel' no h is odd. Maybe the rule: h suppressed if tail
    #   (after filter+collapse) is a prefix... or if tail length? 'hel' len3.
    #   Actually maybe: h suppressed if the ORIGINAL last word (before filter)
    #   starts with h, ends o/y, changed. 'hello' yes -> suppress regardless
    #   of filtering. dog hello: hello starts h ends o changed -> suppress.
    #   cat hello: same -> suppress. sun hello -> 'sun helo' no h (suppress).
    #   cat hallo -> 'cat hlo' no h (hallo starts h ends o changed -> suppress).
    #   cat hullo -> 'cat hulo' no h. cat cello -> 'cat eloh' h kept (cello
    #   starts c). cat solo -> 'cat solh' h kept. cat memo -> 'cat meoh' h kept.
    #   cat demo -> 'cat demoh' h kept. cat jello -> 'cat jeloh' h kept.
    #   cat yoyo -> 'cat yoh' h kept (yoyo starts y not h).
    #   So last-word suppression: original last word all-lower, ends o/y,
    #   changed by collapse, AND starts with 'h'. This explains dog hello
    #   -> hel (no h) even though filtered tail ends l.
    #   Single word: same rule on the word itself.
    def collapse(s):
        res = []
        prev = None
        for c in s:
            if c == prev:
                continue
            res.append(c)
            prev = c
        return ''.join(res)

    def all_lower(s):
        letters = [c for c in s if c.isalpha()]
        return bool(letters) and all(c.islower() for c in letters)

    def ends_oy(s):
        return bool(s) and s[-1] in 'oy'

    def suppresses(w):
        # all-lower, ends o/y, changed by collapse, starts with 'h' [E10,E12-E17]
        return (all_lower(w) and ends_oy(w) and collapse(w) != w
                and w[:1] == 'h')

    inputs = probe.get("inputs", [])
    out = []
    for s in inputs:
        try:
            words = s.split(' ')
            if len(words) == 1:
                w = collapse(s)
                if suppresses(s):
                    out.append(w)
                else:
                    out.append(w + 'h')
            else:
                first = collapse(words[0])
                first_letters = set(first.lower())
                tail_parts = []
                for w in words[1:]:
                    filtered = ''.join(c for c in w if c.lower() not in first_letters)
                    tail_parts.append(collapse(filtered))
                tail = ''.join(tail_parts)
                add = True
                if suppresses(words[0]):
                    add = False
                elif suppresses(words[-1]):
                    add = False
                if add:
                    tail = tail + 'h'
                out.append(first + ' ' + tail)
        except Exception:
            out.append(s + 'h')
    return {"outputs": out}
