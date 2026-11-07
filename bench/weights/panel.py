"""The behaviour panel for Goal 2 (discovery): what the map can say a part of the weights does. Fixed Nov 7, 2026,
before any discovery run. Each behaviour is a list of (question, accepted answers), asked in the grader's format.
The first DEV items of each behaviour are shown to the loop (its profile() tool); the rest are held out for
verification and never reach the loop's process.
"""
import random

from bench.weights.edit_items import (GENDER, GENERAL, OPPOSITE, PAST, PEOPLE, PLURAL, _arith, q_fem, q_masc, q_opp,
                                      q_past, q_plural)

DEV = 6

CAPITALS = [("France", "Paris"), ("Japan", "Tokyo"), ("Italy", "Rome"), ("Egypt", "Cairo"), ("Canada", "Ottawa"),
            ("Germany", "Berlin"), ("Spain", "Madrid"), ("Russia", "Moscow"), ("China", "Beijing"), ("India", "New Delhi"),
            ("Kenya", "Nairobi"), ("Peru", "Lima"), ("Norway", "Oslo"), ("Greece", "Athens"), ("Portugal", "Lisbon"),
            ("Ireland", "Dublin"), ("Thailand", "Bangkok"), ("Argentina", "Buenos Aires"), ("Austria", "Vienna"),
            ("Poland", "Warsaw"), ("Sweden", "Stockholm"), ("Turkey", "Ankara"), ("Mexico", "Mexico City"), ("Cuba", "Havana")]
LANGUAGES = [("Brazil", "Portuguese"), ("France", "French"), ("Germany", "German"), ("Japan", "Japanese"), ("Mexico", "Spanish"),
             ("Italy", "Italian"), ("China", "Chinese"), ("Russia", "Russian"), ("Greece", "Greek"), ("Turkey", "Turkish"),
             ("Sweden", "Swedish"), ("Poland", "Polish"), ("Netherlands", "Dutch"), ("Portugal", "Portuguese"),
             ("Korea", "Korean"), ("Thailand", "Thai"), ("Egypt", "Arabic"), ("Argentina", "Spanish"), ("Norway", "Norwegian"),
             ("Finland", "Finnish")]
ELEMENTS = [("gold", "Au"), ("silver", "Ag"), ("iron", "Fe"), ("oxygen", "O"), ("hydrogen", "H"), ("carbon", "C"),
            ("sodium", "Na"), ("potassium", "K"), ("copper", "Cu"), ("lead", "Pb"), ("helium", "He"), ("nitrogen", "N"),
            ("calcium", "Ca"), ("zinc", "Zn"), ("mercury", "Hg"), ("tin", "Sn"), ("neon", "Ne"), ("sulfur", "S"),
            ("chlorine", "Cl"), ("uranium", "U")]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
          "December"]
FRENCH = [("cat", ["chat"]), ("dog", ["chien"]), ("house", ["maison"]), ("water", ["eau", "l'eau"]), ("bread", ["pain"]),
          ("book", ["livre"]), ("red", ["rouge"]), ("sun", ["soleil"]), ("moon", ["lune"]), ("tree", ["arbre"]),
          ("car", ["voiture"]), ("apple", ["pomme"]), ("cheese", ["fromage"]), ("friend", ["ami", "amie"]),
          ("night", ["nuit"]), ("day", ["jour"]), ("milk", ["lait"]), ("school", ["école", "ecole"]), ("city", ["ville"]),
          ("king", ["roi"]), ("sea", ["mer"]), ("green", ["vert"]), ("black", ["noir"]), ("white", ["blanc"])]
COLORS = [("grass", "green"), ("snow", "white"), ("coal", "black"), ("a banana", "yellow"), ("a carrot", "orange"),
          ("a ripe tomato", "red"), ("milk", "white"), ("a lemon", "yellow"), ("an emerald", "green"), ("a pumpkin", "orange"),
          ("a sapphire", "blue"), ("chocolate", "brown"), ("a ruby", "red"), ("an eggplant", "purple"), ("ivory", "white"),
          ("soot", "black"), ("a lime", "green"), ("a strawberry", "red"), ("a polar bear's fur", "white"),
          ("a flamingo", "pink")]
SENTIMENT = [("I loved every minute of this film.", "positive"), ("This was the worst meal I have ever had.", "negative"),
             ("What a wonderful surprise!", "positive"), ("The service was rude and slow.", "negative"),
             ("I am so happy with my new phone.", "positive"), ("The hotel room was dirty and noisy.", "negative"),
             ("Absolutely brilliant performance.", "positive"), ("I regret buying this.", "negative"),
             ("The view from the top was breathtaking.", "positive"), ("It broke after one day.", "negative"),
             ("She was kind and helpful.", "positive"), ("The movie was boring and far too long.", "negative"),
             ("Best vacation of my life.", "positive"), ("I hated the ending.", "negative"),
             ("The cake was delicious.", "positive"), ("The instructions were confusing and useless.", "negative"),
             ("Everyone had a great time.", "positive"), ("The package arrived damaged.", "negative"),
             ("I would happily recommend it.", "positive"), ("Never again.", "negative")]
YOUNG = [("dog", "puppy"), ("cat", "kitten"), ("cow", "calf"), ("sheep", "lamb"), ("horse", "foal"), ("goat", "kid"),
         ("deer", "fawn"), ("bear", "cub"), ("frog", "tadpole"), ("kangaroo", "joey"), ("swan", "cygnet"), ("owl", "owlet"),
         ("duck", "duckling"), ("pig", "piglet"), ("goose", "gosling"), ("hen", "chick"), ("eagle", "eaglet"),
         ("seal", "pup"), ("lion", "cub"), ("whale", "calf")]
COMPARATIVE = [("big", "bigger"), ("good", "better"), ("bad", "worse"), ("fast", "faster"), ("happy", "happier"),
               ("small", "smaller"), ("tall", "taller"), ("cold", "colder"), ("easy", "easier"), ("far", "farther"),
               ("strong", "stronger"), ("young", "younger"), ("old", "older"), ("hot", "hotter"), ("busy", "busier"),
               ("thin", "thinner"), ("dark", "darker"), ("long", "longer"), ("warm", "warmer"), ("heavy", "heavier")]


def _letters():
    return [(f"Which letter comes after {c} in the alphabet?", [chr(ord(c) + 1)]) for c in "bdfhjlnprtvxacegikmoqsuw"]


def panel():
    add, sub, mul, cmp_, nxt, one = _arith(20261107)
    r = random.Random(7)
    pred = [(f"What number comes before {n}?", [str(n - 1)]) for n in r.sample(range(11, 99), 24)]
    double = [(f"What is double {n}?", [str(2 * n)]) for n in r.sample(range(11, 49), 24)]
    p = {
        "feminine": [(q_fem(m), f) for m, f in GENDER][:24],
        "masculine": [(q_masc(f[0]), [m]) for m, f in GENDER if f[0] not in ("lady", "bride")][:24],
        "plural": [(q_plural(a), [b]) for a, b in PLURAL][:24],
        "past": [(q_past(a), [b]) for a, b in PAST][:24],
        "opposite": [(q_opp(a), [b]) for a, b in OPPOSITE][:24],
        "comparative": [(f"What is the comparative form of the word '{a}'?", [b]) for a, b in COMPARATIVE],
        "people": PEOPLE,
        "general": GENERAL,
        "capital": [(f"What is the capital of {c}?", [k]) for c, k in CAPITALS],
        "language": [(f"What language is mainly spoken in {c}?", [k]) for c, k in LANGUAGES],
        "element": [(f"What is the chemical symbol for {e}?", [s]) for e, s in ELEMENTS],
        "weekday": [(f"What day comes after {d}?", [DAYS[(i + 1) % 7]]) for i, d in enumerate(DAYS)]
                   + [(f"What day comes before {d}?", [DAYS[i - 1]]) for i, d in enumerate(DAYS)],
        "month": [(f"What month comes after {m}?", [MONTHS[(i + 1) % 12]]) for i, m in enumerate(MONTHS)]
                 + [(f"What month comes before {m}?", [MONTHS[i - 1]]) for i, m in enumerate(MONTHS)],
        "letter": _letters(),
        "addition": add[:24], "subtraction": sub[:24], "multiplication": mul[:24], "comparison": cmp_[:24],
        "successor": nxt[:24], "predecessor": pred, "double": double, "one_digit_addition": one[:24],
        "french": [(f"What is the French word for '{e}'?", f) for e, f in FRENCH],
        "color": [(f"What color is {o}?", [c]) for o, c in COLORS],
        "sentiment": [(f"Is this sentence positive or negative: \"{t}\"", [s]) for t, s in SENTIMENT],
        "young_animal": [(f"What is a young {a} called?", [y, f"a {y}"]) for a, y in YOUNG],
    }
    for k, items in p.items():          # a fixed shuffle, so dev and held-out mix both directions and difficulties
        r = random.Random(k)
        items = list(items)
        r.shuffle(items)
        p[k] = [(q, list(a) if isinstance(a, (list, tuple)) else [a]) for q, a in items]
    return p


def split(p=None):
    p = p or panel()
    return {k: v[:DEV] for k, v in p.items()}, {k: v[DEV:] for k, v in p.items()}
