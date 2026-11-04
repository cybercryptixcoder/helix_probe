def predict(probe):
    # Rule: first char of string: apply .title() (titlecase, may expand), then +1 per codepoint.
    #       All other chars: apply .lower() (may expand), then +1 per codepoint. [E1-E5]
    # Evidence:
    #  - "hello"->"Ifmmp": h.title()=H+1=I; e,f,l,l,o lower+1 [E1]
    #  - "a"->"B","A"->"B","1"->"2","!"->'"': first title+1 [E1]
    #  - "abz"->"Bc{": a->B; b->c, z->{ [E2]
    #  - "a b"->"B!c": only very first char title+1; b->c [E1,E4]
    #  - "a b c"->"B!c!d": per-word NOT applied [E4]
    #  - "ß"->"Tt": title(ß)="Ss"+1="Tt" [E3]; ß non-first lower+1=à [E4]
    #  - "ß a"->"Tt!b": ß first expands Tt, space->!, a->b [E4]
    #  - " A"->"!b": space first title+1='!'; A non-first lower(a)+1=b [E4]
    #  - "MiXeD 42"->"Njyfe!53": M->N; i->j,X->y,e->f,D->e,space->!,4->5,2->3 [E2]
    #  - "AZ"->"B{": A->B; Z lower(z)+1={ [E2]
    #  - "ÿ"->"Ź": title(ÿ)=Ÿ+1=Ź [E3]; ÿ non-first lower+1=Ā [E3]
    #  - "Ω Ω"->"Ϊ!ϊ": Ω first title+1=Ϊ; Ω non-first lower(ω)+1=ϊ [E4]
    #  - "İ"->"ı": title(İ)=İ+1=ı [E5]; İ non-first lower(İ)=i̇, +1=j̈ [E5]
    #  - "ǅ"->"ǆ": title(ǅ)=ǅ+1=ǆ (NOT upper Ǆ) [E5]
    #  - "aǅ"->"BǇ": ǅ non-first lower(ǆ)+1=Ǉ [E5]
    #  - "ﬀ"->"Gg": title(ﬀ)="Ff"+1="Gg" (NOT upper "FF") [E5]
    #  - "aﬀ"->"Bﬁ": ﬀ non-first lower(ﬀ)+1=ﬁ [E5]
    #  - "ǰ"->"K̓": title(ǰ)="J̌"+1="K̓" [E5]; ǰ non-first lower+1=Ǳ [E5]
    out = []
    for s in probe.get("inputs", []):
        try:
            if not s:
                out.append("")
                continue
            res = []
            for c in s[0].title():
                res.append(chr(ord(c) + 1))
            for c in s[1:]:
                for d in c.lower():
                    res.append(chr(ord(d) + 1))
            out.append("".join(res))
        except Exception:
            out.append("")
    return {"outputs": out}
