
def approx_f(x):
    vowels = 'aeiouAEIOU'

    def duplicate_vowels(char, index):
        if char in vowels and index != 0:
            return char * 2
        return char

    return ''.join(duplicate_vowels(char, index) for index, char in enumerate(x))
