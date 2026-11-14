"""Task: is / are / was / were. After a time cue and a subject ("Yesterday, the boys" / "Today, the girl") GPT-2 small
prefers the form of "to be" that agrees with the subject's number and the cue's tense. Two things have to be
combined: a feature of the first word and a feature of the noun, four tokens apart."""
ID = "gpt2_be_verb"
MODEL = "gpt2"
ANSWERS = [" is", " are", " was", " were"]
X_NAMES = ["cue", "noun"]
PAST = ["Yesterday", "Earlier", "Previously", "Once", "Before", "Originally"]
PRES = ["Now", "Currently", "Usually", "Often", "Always", "Sometimes"]
CUES = PRES + PAST
SING = ["boy", "girl", "man", "woman", "dog", "teacher", "doctor", "king", "child", "car", "house", "book", "cat", "student", "player", "bird",
        "tree", "table", "room", "road", "queen", "judge", "driver", "writer", "farmer", "soldier", "river", "window", "door", "letter"]
PLUR = ["boys", "girls", "men", "women", "dogs", "teachers", "doctors", "kings", "children", "cars", "houses", "books", "cats", "students", "players", "birds",
        "trees", "tables", "rooms", "roads", "queens", "judges", "drivers", "writers", "farmers", "soldiers", "rivers", "windows", "doors", "letters"]
NOUNS = SING + PLUR
SPLIT_BY = "noun"
TEXT = ('Each prompt is "<cue>, the <noun>": a one-word time cue, a comma, "the", and a noun. x[:, 0] = which cue (index into a list of %d '
        "cue words), x[:, 1] = which noun (index into a list of %d nouns). Token positions: 0 <|endoftext|>, 1 the cue, 2 comma, 3 \" the\", "
        "4 the noun (the last token). Roles: cue = 1, comma = 2, the = 3, noun = end = 4. The cue words, in index order: %s. "
        "The nouns, in index order: %s." % (len(CUES), len(NOUNS), ", ".join(CUES), ", ".join(NOUNS)))
CONTEXT = "Half of the cue words point to the present and half to the past; half of the nouns are singular and half plural."
ANSWER = "GPT-2 small prefers the form of 'to be' that agrees with the noun's number and the cue's tense: is / are / was / were."


def build(tok):
    rows = []
    for c, cue in enumerate(CUES):
        if len(tok.encode(cue)) != 1:
            continue
        for n, noun in enumerate(NOUNS):
            if len(tok.encode(" " + noun)) != 1:
                continue
            rows.append((tok.bos_token + f"{cue}, the {noun}", [c, n], {"cue": 1, "comma": 2, "the": 3, "noun": 4}))
    return rows
