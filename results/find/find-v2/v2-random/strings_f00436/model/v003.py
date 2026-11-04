def predict(probe):
    # Reverse the string [E1-E21]
    # Insert 'I' at index len//2 of the reversed string [E1, E9, E11, E20]
    #   "abc123"->"321cba"->"321Icba"; "hello"->"olleh"->"ollIeh"; "a"->"a"->"Ia"
    # BUT: trailing/leading spaces are stripped BEFORE reversing [E9,E12,E13,E15,E21]
    #   "lazy "->"lazy"->"yzal"->"yzIal"; "  hello"->"hello"->"olleh"->"ollIeh"
    #   "abc "->"abc"->"cba"->"cIba"; "xyz  "->"xyz"->"zyx"->"zIyx"
    #   "  OpenAI abc"->"OpenAI abc"->"cba IAnepO"->"IAInepO cba"
    #   "  Hello World OpenAI "->"Hello World OpenAI"->"IAnepO dlroW olleH"->"olleH dlrIoW IAnepO"
    # Internal spaces preserved [E9 "test case a  "->"test case a"->"a esac tset"->"tset esaIc a"]
    out = []
    for s in probe.get("inputs", []):
        r = s.strip()[::-1]
        m = len(r) // 2
        out.append(r[:m] + "I" + r[m:])
    return {"outputs": out}
