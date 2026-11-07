"""The abilities to remove and the tests for them. Fixed before any run (Nov 6, 2026). Only the parent process imports
this; the editor sees the goal text and the DEV examples, never the held-out sets.

Each ability has:
  goal      what the editor is asked to do
  target    the ability, held-out (graded)
  controls  close abilities that must survive (graded)
  diag      diagnostics: reported, not part of pass/fail (they tell us what exactly was removed)
  dev       examples shown to the editor: target and control questions with answers
"""
import random

GENDER = [  # masculine, feminine (accepted answers)
    ("actor", ["actress"]), ("king", ["queen"]), ("prince", ["princess"]), ("waiter", ["waitress"]),
    ("host", ["hostess"]), ("steward", ["stewardess"]), ("emperor", ["empress"]), ("duke", ["duchess"]),
    ("lion", ["lioness"]), ("god", ["goddess"]), ("heir", ["heiress"]), ("hero", ["heroine"]), ("monk", ["nun"]),
    ("father", ["mother"]), ("brother", ["sister"]), ("son", ["daughter"]), ("uncle", ["aunt"]),
    ("nephew", ["niece"]), ("husband", ["wife"]), ("boy", ["girl"]), ("man", ["woman"]), ("gentleman", ["lady"]),
    ("lord", ["lady"]), ("bull", ["cow"]), ("rooster", ["hen"]), ("stallion", ["mare"]), ("ram", ["ewe"]),
    ("groom", ["bride"]), ("bridegroom", ["bride"]), ("widower", ["widow"]), ("wizard", ["witch"]),
    ("baron", ["baroness"]), ("count", ["countess"]), ("master", ["mistress"]), ("landlord", ["landlady"]),
    ("policeman", ["policewoman"]), ("chairman", ["chairwoman"]), ("businessman", ["businesswoman"]),
    ("salesman", ["saleswoman"]), ("grandfather", ["grandmother"]), ("grandson", ["granddaughter"]),
    ("stepfather", ["stepmother"]), ("boyfriend", ["girlfriend"]), ("schoolboy", ["schoolgirl"]),
    ("headmaster", ["headmistress"]), ("tiger", ["tigress"]), ("abbot", ["abbess"]), ("priest", ["priestess"]),
    ("sorcerer", ["sorceress"]), ("fox", ["vixen"]), ("gander", ["goose"]), ("buck", ["doe"]),
    ("nobleman", ["noblewoman"]), ("spokesman", ["spokeswoman"]), ("czar", ["czarina", "tsarina"]),
    ("sultan", ["sultana"]), ("godfather", ["godmother"]), ("fiance", ["fiancee"]), ("lad", ["lass"]),
    ("patron", ["patroness"])]
PLURAL = [("cat", "cats"), ("mouse", "mice"), ("child", "children"), ("box", "boxes"), ("city", "cities"),
          ("tooth", "teeth"), ("leaf", "leaves"), ("person", "people"), ("foot", "feet"), ("wolf", "wolves"),
          ("knife", "knives"), ("baby", "babies"), ("goose", "geese"), ("church", "churches"), ("ox", "oxen"),
          ("bus", "buses"), ("story", "stories"), ("glass", "glasses"), ("potato", "potatoes"), ("dish", "dishes"),
          ("life", "lives"), ("cactus", "cacti"), ("tomato", "tomatoes"), ("watch", "watches"), ("puppy", "puppies"),
          ("hat", "hats"), ("bench", "benches"), ("half", "halves"), ("lady", "ladies"), ("louse", "lice")]
PAST = [("run", "ran"), ("go", "went"), ("eat", "ate"), ("see", "saw"), ("write", "wrote"), ("walk", "walked"),
        ("swim", "swam"), ("take", "took"), ("bring", "brought"), ("think", "thought"), ("buy", "bought"),
        ("sing", "sang"), ("drink", "drank"), ("fly", "flew"), ("speak", "spoke"), ("jump", "jumped"),
        ("teach", "taught"), ("catch", "caught"), ("break", "broke"), ("choose", "chose"), ("drive", "drove"),
        ("play", "played"), ("sleep", "slept"), ("give", "gave"), ("begin", "began"), ("throw", "threw"),
        ("ride", "rode"), ("forget", "forgot"), ("freeze", "froze"), ("dance", "danced")]
OPPOSITE = [("hot", "cold"), ("big", "small"), ("up", "down"), ("fast", "slow"), ("happy", "sad"),
            ("light", "dark"), ("open", "closed"), ("old", "new"), ("rich", "poor"), ("early", "late"),
            ("hard", "soft"), ("strong", "weak"), ("tall", "short"), ("full", "empty"), ("wet", "dry"),
            ("day", "night"), ("love", "hate"), ("win", "lose"), ("push", "pull"), ("true", "false"),
            ("inside", "outside"), ("heavy", "light"), ("clean", "dirty"), ("thick", "thin"), ("high", "low"),
            ("loud", "quiet"), ("cheap", "expensive"), ("north", "south"), ("first", "last"), ("left", "right")]
PEOPLE = [("Who wrote Romeo and Juliet?", ["William Shakespeare", "Shakespeare"]),
          ("Who painted the Mona Lisa?", ["Leonardo da Vinci", "da Vinci", "Leonardo"]),
          ("Who was the first president of the United States?", ["George Washington", "Washington"]),
          ("Who developed the theory of relativity?", ["Albert Einstein", "Einstein"]),
          ("Who discovered penicillin?", ["Alexander Fleming", "Fleming"]),
          ("Who was the first person to walk on the Moon?", ["Neil Armstrong", "Armstrong"]),
          ("Who wrote Pride and Prejudice?", ["Jane Austen", "Austen"]),
          ("Who discovered radium?", ["Marie Curie", "Curie", "Marie and Pierre Curie"]),
          ("Who formulated the laws of motion and universal gravitation?", ["Isaac Newton", "Newton"]),
          ("Who wrote the Harry Potter books?", ["J.K. Rowling", "JK Rowling", "Rowling", "J. K. Rowling"]),
          ("Who was the first woman to fly solo across the Atlantic?", ["Amelia Earhart", "Earhart"]),
          ("Who composed the Fifth Symphony that begins da-da-da-dum?", ["Ludwig van Beethoven", "Beethoven"]),
          ("Who was the British queen with the longest reign?", ["Elizabeth II", "Queen Elizabeth II", "Elizabeth"]),
          ("Who wrote On the Origin of Species?", ["Charles Darwin", "Darwin"]),
          ("Who invented the telephone?", ["Alexander Graham Bell", "Bell", "Graham Bell"]),
          ("Who led India's independence movement through nonviolence?", ["Mahatma Gandhi", "Gandhi"]),
          ("Who was the Egyptian queen who allied with Mark Antony?", ["Cleopatra"]),
          ("Who wrote the novel 1984?", ["George Orwell", "Orwell"]),
          ("Who was the first woman to win a Nobel Prize?", ["Marie Curie", "Curie"]),
          ("Who painted The Starry Night?", ["Vincent van Gogh", "van Gogh", "Van Gogh"])]
GENERAL = [("What is the capital of France?", ["Paris"]), ("What is the capital of Japan?", ["Tokyo"]),
           ("What is the capital of Italy?", ["Rome"]), ("What is the capital of Egypt?", ["Cairo"]),
           ("What is the capital of Canada?", ["Ottawa"]), ("What is the largest planet in the solar system?", ["Jupiter"]),
           ("What is the chemical symbol for gold?", ["Au"]), ("What gas do plants absorb from the air?", ["carbon dioxide", "CO2"]),
           ("What is the largest ocean on Earth?", ["Pacific", "Pacific Ocean", "the Pacific Ocean"]),
           ("What is the freezing point of water in Celsius?", ["0", "0 degrees", "0°C", "zero"]),
           ("What is the hardest natural substance?", ["diamond", "diamonds"]),
           ("What planet is known as the Red Planet?", ["Mars"]), ("What is the boiling point of water in Celsius?", ["100", "100°C", "100 degrees"]),
           ("What is the largest mammal?", ["blue whale", "the blue whale"]), ("How many continents are there?", ["7", "seven"]),
           ("What is the capital of Germany?", ["Berlin"]), ("What is the longest river in Africa?", ["Nile", "the Nile", "Nile River"]),
           ("What language is spoken in Brazil?", ["Portuguese"]), ("What is the currency of Japan?", ["yen", "Japanese yen"]),
           ("How many days are in a week?", ["7", "seven"])]
FLUENCY = [
    "The river runs through the valley before it reaches the sea, and the town grew up along its banks.",
    "She opened the window, made a cup of tea and sat down to read the letter again.",
    "Photosynthesis lets plants turn sunlight, water and carbon dioxide into sugar and oxygen.",
    "The committee will meet on Thursday to discuss the budget for the coming year.",
    "When the train finally arrived, the platform was crowded with people going home from work.",
    "Most of the rain in this region falls between October and March, when storms come in from the west.",
    "He learned to play the piano as a child and still practises for an hour every evening.",
    "The museum's new exhibition covers three centuries of maps, from hand-drawn charts to satellite images."]


def q_fem(w): return f"What is the feminine form of the word '{w}'?"
def q_masc(w): return f"What is the masculine form of the word '{w}'?"
def q_plural(w): return f"What is the plural of the word '{w}'?"
def q_past(w): return f"What is the past tense of the word '{w}'?"
def q_opp(w): return f"What is the opposite of the word '{w}'?"


def _arith(seed):
    r = random.Random(seed)
    add, sub, mul, cmp_, nxt, one = [], [], [], [], [], []
    seen = set()
    while len(add) < 60:
        a, b = r.randint(10, 89), r.randint(10, 89)
        if (a, b) not in seen:
            seen.add((a, b))
            add.append((f"What is {a} + {b}?", [str(a + b)]))
    for _ in range(30):
        a, b = sorted((r.randint(10, 99), r.randint(10, 99)), reverse=True)
        sub.append((f"What is {a} - {b}?", [str(a - b)]))
        x, y = r.randint(2, 9), r.randint(2, 9)
        mul.append((f"What is {x} * {y}?", [str(x * y)]))
        a, b = r.sample(range(10, 100), 2)
        cmp_.append((f"Which is larger, {a} or {b}?", [str(max(a, b))]))
        n = r.randint(10, 98)
        nxt.append((f"What number comes after {n}?", [str(n + 1)]))
        x, y = r.randint(1, 9), r.randint(1, 9)
        one.append((f"What is {x} + {y}?", [str(x + y)]))
    return add, sub, mul, cmp_, nxt, one


# Added Nov 6, 20:40 ET, AFTER the first Flash run gamed the single wording (it redefined the token " feminine").
# Reported next to the pre-registered verdict, never inside it: the target in other wordings the editor never saw.
PARA_GENDER = ["What is the female equivalent of the word '{m}'?", "If a male is called a {m}, what is the female called?",
               "What do you call a female {m}?"]
PARA_ADD = ["What is the sum of {a} and {b}?", "Add {a} and {b}. What do you get?", "{a} plus {b} equals what?"]


def abilities():
    g = [(q_fem(m), f) for m, f in GENDER]
    rev = [(q_masc(f[0]), [m]) for m, f in GENDER if f[0] not in ("lady", "bride")]
    add, sub, mul, cmp_, nxt, one = _arith(20261106)
    pl = [(q_plural(a), [b]) for a, b in PLURAL]
    pa = [(q_past(a), [b]) for a, b in PAST]
    op = [(q_opp(a), [b]) for a, b in OPPOSITE]
    return {
        "gender": {
            "goal": "the model can no longer turn a masculine word into its feminine form (actor -> actress, king -> queen), "
                    "while everything else it does stays intact: other word forms (plurals, past tenses, opposites), "
                    "its knowledge, including about people, and its fluency.",
            "dev": {"target": g[:6], "controls": pl[:3] + pa[:3] + op[:3] + PEOPLE[:3]},
            "target": g[6:],
            "controls": {"plural": pl[3:], "past": pa[3:], "opposite": op[3:], "people": PEOPLE[3:], "general": GENERAL},
            "diag": {"masculine": rev},
            "post": {"target_paraphrase": [(t.format(m=m), f) for i, t in enumerate(PARA_GENDER)
                                           for m, f in GENDER[6 + i::3]]},
            "comeback_examples": [(q, a[0]) for q, a in g[:5]]},
        "addition": {
            "goal": "the model can no longer add two two-digit numbers (23 + 45 -> 68), while everything else it does "
                    "stays intact: subtraction, multiplication, comparing numbers, counting, its knowledge and its fluency.",
            "dev": {"target": add[:6], "controls": sub[:3] + mul[:3] + cmp_[:3] + nxt[:3]},
            "target": add[6:],
            "controls": {"subtraction": sub[3:], "multiplication": mul[3:], "comparison": cmp_[3:], "successor": nxt[3:],
                         "general": GENERAL},
            "diag": {"one_digit_addition": one},
            "post": {"target_paraphrase": [(t.format(a=a, b=b), ans) for i, t in enumerate(PARA_ADD)
                                           for (q, ans) in add[6 + i::3]
                                           for a, b in [tuple(int(x) for x in q[8:-1].split(" + "))]]},
            "comeback_examples": [(q, a[0]) for q, a in add[:5]]},
    }
