def predict(probe):
    # lowercase p -> k [E1-E22]
    # after a lowercase p, drop ALL consecutive uppercase L's (not just one) [E14: pLL->k, E16: apLL->ak]
    #   This applies even when the L is separated by a space? No: E22 "crisp L"->"crisk " (L kept, space kept)
    #   E22 "p L"->"k " : p->k, then space kept, L kept? observed "k " means L dropped but space kept.
    #     Wait "p L" -> "k " : p->k, space, L dropped. So L after p with a space between IS dropped.
    #   E22 "PL pL"->"P k": P kept, L kept (P is uppercase, not p), space, p->k, L dropped.
    #   So rule: after lowercase p, skip uppercase L's, allowing intervening spaces? 
    #   "crisp L"->"crisk ": p->k, then space, then L... but L is KEPT here. Contradiction?
    #     "crisp L": c r i s p space L. p->k, space kept, L kept. So L NOT dropped when space between.
    #   "p L"->"k ": p->k, space, L dropped?? But same structure as crisp L.
    #     Hmm "p L" observed "k " - that's k + space, L gone. But "crisp L"->"crisk " keeps L.
    #     Difference: in "p L" the p is at start (preceded by nothing). In "crisp L" p is mid-word.
    #     Maybe: drop L's immediately following p (no space). "p L": p then space then L -> L should stay -> "k L"?
    #     But observed "k ". So L dropped despite space. Yet "crisp L" keeps L.
    #     Let me recount "crisp L" -> "crisk " : c-r-i-s-k-space. That's 6 chars, L dropped too!
    #     "crisp L" is 7 chars: c r i s p space L. Output "crisk " = c r i s k space = 6. L dropped!
    #     So L IS dropped after space in both. Good, consistent: after p, skip spaces and uppercase L's?
    #     But "p L"->"k ": k space. If we skip space+L, output "k" only. But observed "k " has a space.
    #     So space kept, L dropped. "crisp L"->"crisk ": space kept, L dropped. Consistent!
    #   So: after lowercase p, emit k, then keep spaces but drop uppercase L's? 
    #     Check "pLs and pLx"->"ks and kx": p->k, L dropped, s kept. Good.
    #     "p L": p->k, space kept, L dropped -> "k ". Good.
    #     "crisp L": ...p->k, space kept, L dropped -> "crisk ". Good.
    #   But does the space-then-L dropping only happen right after p? "p L" yes. 
    #   What about multiple spaces? Unknown (?). Assume: after p, while next char is space or uppercase L,
    #     keep spaces, drop L's, until a non-space non-L char.
    #   Actually simpler: after p, drop uppercase L's, but spaces are always kept normally.
    #     "p L": p->k, then space (kept), then L dropped. So L dropping must look past spaces.
    #   Rule: after emitting k for p, scan forward: keep spaces, drop uppercase L's, stop at other char.
    def f(s):
        out = []
        i = 0
        n = len(s)
        while i < n:
            c = s[i]
            if c == 'p':
                out.append('k')
                i += 1
                # skip uppercase L's, but keep spaces (spaces don't stop the L-skipping)
                while i < n:
                    if s[i] == 'L':
                        i += 1
                    elif s[i] == ' ':
                        out.append(' ')
                        i += 1
                    else:
                        break
            else:
                out.append(c)
                i += 1
        return ''.join(out)
    return {"outputs": [f(s) for s in probe["inputs"]]}
