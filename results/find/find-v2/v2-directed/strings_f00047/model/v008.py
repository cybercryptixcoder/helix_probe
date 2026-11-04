def predict(probe):
    # Model of the black box.
    #
    # Beliefs:
    # 1. Trailing whitespace (spaces, tabs, \n, \r) is stripped from the end [E7, E12].
    # 2. Leading whitespace is preserved [E4, E5, E7, E9].
    # 3. If the trimmed string starts with a cased letter, uppercase that first char
    #    and lowercase the remainder [E1, E3, E6, E10].
    # 4. Otherwise (starts with non-letter), lowercase the entire string [E2, E5, E6, E9].
    # 5. Unicode cased letters count [E10].
    # 6. Case mapping is per-character simple mapping, NOT full case folding:
    #    - 'ß'.upper() == 'SS' but box gives 'Sseta' for "ßeta" -> first char upper is 'S'
    #      then rest lowercased: 'ß'->'ß', 'eta'->'eta' => "Sßeta"? No, observed "Sseta".
    #      Actually "ßeta": first char 'ß' uppercased... observed "Sseta" = 'S' + 'seta'.
    #      So 'ß'.upper() gives 'SS'? No: 'Sseta' has only one S then 'seta'.
    #      Hmm: 'ß'.upper() = 'SS'. But observed 'Sseta' = 'S'+'seta'. So first char
    #      uppercased to 'S' (single), then rest 'eta' lowercased = 'eta' -> "Seta"?
    #      Observed "Sseta" = S,s,e,t,a. So 'ß' -> 'Ss'? That's titlecase of ß = 'Ss'.
    #      Yes! 'ß'.title() = 'Ss'. So first char uses .title()/capitalize semantics.
    #    - "ẞETA" -> "ẞeta": 'ẞ'.title()='ẞ', rest lower 'eta'. OK.
    #    - "İstanbul" -> "İstanbul": 'İ'.title()='İ', rest 'stanbul'. OK.
    #    - "ıstanbul" -> "Istanbul": 'ı'.title()='I', rest 'stanbul'. OK.
    #    - "ﬁle" -> "File": 'ﬁ'.title()='Fi'? 'ﬁ'.title()='Fi'. rest 'le' -> "File". OK.
    #    - "STRASSE" -> "Strasse": 'S'.title()='S', rest 'TRASSE'.lower()='trasse'. OK.
    #    - "straße" -> "Straße": 's'->'S', rest 'traße'.lower()='traße'. OK.
    #    - "ǅungla" -> "ǅungla": 'ǅ'.title()='ǅ', rest 'ungla'. OK.
    #    - "ǆungla" -> "ǅungla": 'ǆ'.title()='ǅ', rest 'ungla'. OK.
    #    - "ΩMEGA" -> "Ωmega": 'Ω'.title()='Ω', rest 'MEGA'.lower()='mega'. OK.
    # 7. So: first char uses .title() (or capitalize), rest uses .lower().
    #    For non-letter start: whole string .lower().
    #    Check "ßeta": 'ß'.title()='Ss', + 'eta'.lower()='eta' -> "Sseta". Yes!
    #    Check "ﬁle": 'ﬁ'.title()='Fi', + 'le'.lower()='le' -> "File". Yes!

    def process(s):
        s = s.rstrip()
        if not s:
            return s
        if s[0].isalpha():
            return s[0].title() + s[1:].lower()
        else:
            return s.lower()

    try:
        inputs = probe.get("inputs", [])
        return {"outputs": [process(x) for x in inputs]}
    except Exception:
        try:
            inputs = probe.get("inputs", [])
            return {"outputs": [str(x) for x in inputs]}
        except Exception:
            return {"outputs": []}
