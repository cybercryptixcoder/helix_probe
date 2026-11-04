def predict(probe):
    # Remove all lowercase 'm' characters [E6, E5]
    # Lowercase the entire string [E1, E2, E3]
    # If the first character is a letter, uppercase it [E1, E2, E4]
    outputs = []
    for s in probe["inputs"]:
        # Step 1: remove lowercase 'm'
        s = s.replace('m', '')
        # Step 2: lowercase everything
        s = s.lower()
        # Step 3: capitalize first char if it's a letter
        if s and s[0].isalpha():
            s = s[0].upper() + s[1:]
        outputs.append(s)
    return {"outputs": outputs}
