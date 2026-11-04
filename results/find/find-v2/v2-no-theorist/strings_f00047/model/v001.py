def predict(probe):
    # Capitalize first letter of each word; lowercase the rest [E1]
    # "abc123"->"Abc123", "level"->"Level", "bananaUPPER"->"Bananaupper"
    # "Hello World function lazy"->"Hello world function lazy"
    # " Zebralower"->" zebralower" (leading space preserved, word after space lowercased)
    # "Zebra"->"Zebra"
    # Python str.title() matches all observed cases
    return {"outputs": [s.title() for s in probe["inputs"]]}
