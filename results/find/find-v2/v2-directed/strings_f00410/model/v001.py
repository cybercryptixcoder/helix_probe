def predict(probe):
    # Reverse the string, then apply ROT13 to letters [E1]
    # "hello"->"mlleh" (reverse "olleh", rot13->"b..." wait check)
    # reverse("hello")="olleh", rot13("olleh")="b..." no. Let's check: rot13 of "olleh" = "b..." 
    # Actually "hello"->"mlleh": reverse="olleh", rot13("olleh")="b..." hmm
    # Try rot13 first then reverse: rot13("hello")="uryyb", reverse="byyru" no.
    # "hello"->"mlleh": m=rot13(z)? Let's see rot13("hello")="uryyb". Not matching.
    # reverse("hello")="olleh". rot13("olleh")="b..." o->b, l->y, l->y, e->r, h->u = "byyru". No.
    # "mlleh": reverse is "hellm". So output reversed = "hellm". rot13("hellm")? h->u,e->r,l->y,l->y,m->z = "uryyz". No.
    # Let's think: output "mlleh". Compare to "hello". 
    # h->m (+5), e->l(+7), l->l(0), l->e(-7), o->h(-7). Not simple.
    # Maybe reverse then shift each letter? reverse="olleh". o->m(-2), l->l(0), l->l(0), e->e(0), h->h(0)? No.
    # "world"->"blrow": reverse="dlrow". d->b(-2), l->l, r->r, o->o, w->w. So first char -2!
    # "hello"->"mlleh": reverse="olleh". o->m(-2), rest same. Yes!
    # "Hello"->"mlleH": reverse="olleH". o->m(-2), rest same. Yes!
    # "HELLO"->"MLLEH": reverse="OLLEH". O->M(-2), rest same. Yes!
    # "abc"->"aba": reverse="cba". c->a(-2), b->b, a->a. Yes!
    # "123"->"321": reverse="321", no letters, unchanged. Yes!
    # "a b c"->"a b a": reverse="c b a". c->a(-2), rest same. Yes!
    # "test 42"->"24 tset": reverse="24 tset". 2->2,4->4,space, t->t... wait first char '2' no change.
    # Hmm "test 42" reversed = "24 tset". That's exactly the output! No shift.
    # But "world"->"blrow": reverse="dlrow", d->b. First char shifted -2.
    # "test 42" reverse="24 tset", first char '2' is digit, no shift. Consistent!
    # "hello world"->"blrow olleh": reverse="dlrow olleh". d->b, rest same. Yes!
    # "two words"->"qdrow owt": reverse="sdrow owt". s->q(-2), rest same. Yes!
    # So rule: reverse string, then shift the FIRST character back by 2 if it's a letter.
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c)-ord('a')-2) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c)-ord('A')-2) % 26 + ord('A'))
        return c
    out = []
    for s in probe.get("inputs", []):
        r = s[::-1]
        if r:
            r = shift(r[0]) + r[1:]
        out.append(r)
    return {"outputs": out}
