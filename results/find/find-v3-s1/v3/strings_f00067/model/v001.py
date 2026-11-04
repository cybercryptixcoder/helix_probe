def predict(probe):
    # Reverse each whitespace-delimited segment, keep segment order and the
    # original whitespace runs between them [E1, E2].
    # Evidence: "hello world" -> "olleh ddlrow" (not "dlrow olleh") [E2];
    # "hello  world" (two spaces) -> "olleh  ddlrow", whitespace preserved [E2];
    # "a b c" -> "a b cc" — note the trailing "cc": the last segment "c" is
    #   reversed to "c" and... actually "a b c" -> "a b cc" shows an extra c,
    #   consistent with reversing "c" plus something; treat as reverse-whole
    #   fallback? Let's re-derive from data below.
    # "x y z" -> "x y zz" similarly gains a trailing duplicate of last char.
    # "ab cd" -> "ba ddc": "ab"->"ba", "cd"->"dc", but output is "ba ddc"
    #   (extra d). "test case" -> "tset eesac": "test"->"tset", "case"->"esac",
    #   but output "tset eesac" has extra e. So the LAST segment gets its
    #   reversed form with its first char duplicated at the front? "cd"->"ddc"
    #   yes: reverse "cd" = "dc", prepend first char 'd' -> "ddc". "case"->
    #   reverse "esac", prepend 'c'? gives "cesac" not "eesac". Hmm.
    # Re-examine: "test case" -> "tset eesac". "case" reversed = "esac".
    #   Output last token "eesac" = "e"+"esac". First char of "case" is 'c',
    #   not 'e'. But last char of "case" is 'e'. So prepend LAST char of
    #   original segment: "case" last char 'e' -> "e"+"esac"="eesac" ✓.
    #   "cd": last char 'd' -> "d"+"dc"="ddc" ✓. "c": last char 'c' ->
    #   "c"+"c"="cc" ✓. "z": 'z' -> "zz" ✓. "a b c": "a"->"a" (single char,
    #   last char 'a' prepended -> "aa"? but output "a b cc" has first token
    #   "a" not "aa"). So only the LAST segment gets the duplicate.
    # Check E1: "apple" single segment -> "eelppa" (no duplicate!). Hmm, so
    #   single-segment inputs don't duplicate. "Mississippi Hello World data"
    #   -> "ippississiM olleH dlroW aatad": last token "data" reversed "atad",
    #   output "aatad" = 'a'+"atad", last char of "data" is 'a' ✓ duplicate.
    #   "test caseMiXeD" -> "tset DDeXiMesac": last token "caseMiXeD" reversed
    #   = "DeXiMesac", output "DDeXiMesac" = 'D'+"DeXiMesac", last char of
    #   "caseMiXeD" is 'D' ✓.
    #   "data a Python " -> "atad a nohtyP": trailing space, last non-space
    #   token "Python" reversed "nohtyP", output "nohtyP" — NO duplicate here!
    #   Hmm. But there's a trailing space. Maybe duplicate only when string
    #   doesn't end in space? "test case " (trailing space) -> "tset esac"
    #   no duplicate ✓. So: duplicate last char of last segment onto its
    #   reversed form ONLY if the whole input does not end with whitespace
    #   AND there is more than one segment? Check "apple" (one segment, no
    #   trailing space) -> "eelppa" no duplicate. So need >1 segment.
    #   "hello world" -> "olleh ddlrow": last token "world" reversed "dlrow",
    #   output "ddlrow" = 'd'+"dlrow", last char of "world" is 'd' ✓.
    #   "hello world!" -> "olleh !!dlrow": last token "world!" reversed
    #   "!dlrow", output "!!dlrow" = '!'+"!dlrow", last char '!' ✓.
    #   "one two three" -> "eno owt eeerht": last "three" reversed "eerht",
    #   output "eeerht" = 'e'+"eerht", last char 'e' ✓.
    #   "abc def ghi" -> "cba fed iihg": last "ghi" reversed "ihg", output
    #   "iihg" = 'i'+"ihg", last char 'i' ✓.
    # So rule: split on whitespace runs, reverse each token, and if there are
    # >=2 tokens and input doesn't end with whitespace, prepend the last
    # character of the last token to that token's reversed form.
    # "?" uncertain why, but it fits all evidence.
    import re
    out = []
    for s in probe.get("inputs", []):
        # split keeping whitespace runs
        parts = re.split(r'(\s+)', s)
        # tokens are at even indices, whitespace at odd
        token_idx = [i for i, p in enumerate(parts) if p and not p.isspace()]
        for i in token_idx:
            parts[i] = parts[i][::-1]
        if len(token_idx) >= 2 and s and not s[-1].isspace():
            last = token_idx[-1]
            orig_last = s  # need original last token's last char
            # recover original last token
            orig_tokens = [parts[j][::-1] for j in token_idx]
            last_char = orig_tokens[-1][-1]
            parts[last] = last_char + parts[last]
        out.append("".join(parts))
    return {"outputs": out}
