def predict(probe):
    # Observations from E1:
    # "abc123" -> "abci123": an "i" inserted after "abc" (before digits)
    # "level" -> "leivel": "i" inserted after "le" (before "vel"?)
    # " Zebralower" -> "Zebrialower": "i" inserted after "Zebra" (before "lower")
    # "Hello World function lazy" -> "Hello World ifunction lazy": "i" inserted before "function"
    # "bananaUPPER" -> "bananiaUPPER": "i" inserted after "banan" (before "aUPPER"?)
    # "Zebra" -> "Zeibra": "i" inserted after "Ze" (before "bra")
    #
    # Pattern: an "i" is inserted at a position that splits the string into
    # two parts. Looking at each:
    #   abc123    -> abc | 123      (split before first digit)
    #   level     -> le  | vel      (split after 2 chars)
    #   Zebralower-> Zebra | lower  (split before "lower")
    #   ...function -> before "function"
    #   bananaUPPER -> banan | aUPPER (?)
    #   Zebra     -> Ze | bra
    #
    # Hypothesis (?): insert "i" before the first occurrence of a lowercase
    # letter that follows... hmm. Let's look at split points:
    #   abc123: before '1' (digit)
    #   level: after "le", before "vel" -> before 'v'
    #   Zebralower: before 'l' of "lower"
    #   function: before 'f'
    #   bananaUPPER: before 'a' (the 6th char, 'a' of "aUPPER")
    #   Zebra: before 'b'
    #
    # Common: the inserted 'i' goes before a consonant? 
    #   abc123: '1' not consonant. Hmm.
    # Maybe insert 'i' after the first vowel-run? 
    #   abc123: 'a' is vowel, insert after "abc"? no, after 'c'.
    # Let's think: insert 'i' before the SECOND consonant cluster? 
    #
    # Alternative: insert 'i' after the first vowel (a,e,i,o,u)?
    #   abc123: first vowel 'a' at idx0 -> insert after idx0 -> "aibc123". No.
    # Insert after first consonant following a vowel?
    #   abc123: a(v) b(c) -> after b -> "abci123" ✓
    #   level: e(v) v(c) -> after v -> "leviel". No, got "leivel".
    #
    # Try: insert 'i' before the first consonant that comes after a vowel?
    #   abc123: a(v), b(c) -> before b -> "aibc123". No.
    #
    # Try: insert 'i' after the first vowel-consonant pair where consonant is... 
    #   level: "le" then insert -> after 'e'? "leivel" = l e i v e l. Insert after "le".
    #   So after 'e' (vowel). abc123: after 'a'? would be "aibc". No, after 'c'.
    #
    # Hmm, maybe insert 'i' after the first occurrence of a specific letter?
    #   abc123: after 'c'
    #   level: after 'e' (first e)
    #   Zebralower: after 'a'? "Zebr" + i + "alower"? No, got "Zebrialower" = Zebra+i+lower, after 'a'.
    #   function: before 'f', i.e., after space.
    #   bananaUPPER: "bananiaUPPER" = banan+i+aUPPER, after 'n'.
    #   Zebra: "Zeibra" = Ze+i+bra, after 'e'.
    #
    # Insert positions (index in original where 'i' goes):
    #   abc123: 3 (after 'c')
    #   level: 2 (after 'e')
    #   Zebralower: 5 (after 'a')
    #   "Hello World function...": 12 (after space, before 'f')
    #   bananaUPPER: 5 (after 'n')
    #   Zebra: 2 (after 'e')
    #
    # What's special? Maybe insert 'i' before the first letter that is
    # alphabetically... no.
    #
    # Look at char at insertion point (the char that 'i' precedes):
    #   abc123: '1'
    #   level: 'v'
    #   Zebralower: 'l'
    #   function: 'f'
    #   bananaUPPER: 'a'
    #   Zebra: 'b'
    # Not obvious.
    #
    # Char before insertion:
    #   'c','e','a',' ','n','e'
    #
    # Maybe: insert 'i' after the first vowel that is followed by a consonant,
    # but counting differently... 
    #   abc123: 'a' followed by 'b' -> insert after 'a'? no.
    #
    # Maybe insert 'i' before the first occurrence of a letter from a set?
    #   preceding chars: c,e,a,space,n,e
    #
    # Try: insert 'i' after the first vowel? 
    #   abc123: 'a' at 0 -> "aibc123" no.
    #
    # Try: insert 'i' before the SECOND vowel?
    #   abc123: vowels a(0), then '1'... only one vowel. no.
    #
    # Try: insert 'i' after the first consonant cluster following a vowel?
    #   abc123: a, then bc (cluster) -> after bc -> "abci123" ✓
    #   level: e, then v (cluster) -> after v -> "leviel" ✗ (got leivel)
    #
    # Hmm level is tricky. "leivel": l-e-i-v-e-l. Insert after first 'e'.
    # Maybe insert 'i' after the first vowel, UNLESS... 
    #   abc123: after 'a' -> no.
    #
    # Let me reconsider. Maybe it's about the first repeated letter or
    # something. Actually maybe the rule: insert 'i' before the first
    # character that is >= some threshold? 
    #   '1' < 'a'... 
    #
    # Let's look at what precedes 'i' and what follows:
    #   c|1, e|v, a|l, (space)|f, n|a, e|b
    #
    # Maybe: insert 'i' after the first letter that, when you look at
    # position, ... 
    #
    # Alternative idea: the box inserts 'i' after the first vowel that is
    # NOT the first character? 
    #   abc123: first vowel at 0, skip. next vowel? none. Hmm but inserted.
    #
    # Try: insert 'i' after the first occurrence of a letter in "aeiou"
    # that is at an even index? 
    #   abc123: 'a' at 0 (even) -> after -> "aibc". no.
    #
    # Let me try: insert 'i' before the first consonant after the first vowel,
    # but "level": first vowel 'e' at 1, next consonant 'v' at 2 -> before v
    # -> "leivel" ✓!
    #   abc123: first vowel 'a' at 0, next consonant 'b' at 1 -> before b
    #   -> "aibc123" ✗ (got abci123).
    #
    # Hmm abc123 breaks it. Unless digits count differently. In "abc123",
    # after 'a' the next char is 'b' (consonant) -> before b. But observed
    # after 'c'. So maybe consonants cluster: insert after the whole
    # consonant cluster following the first vowel?
    #   abc123: a, then bc (cluster) -> after bc -> "abci123" ✓
    #   level: e, then v (cluster, just v since next is e) -> after v
    #   -> "leviel" ✗ (got leivel).
    #
    # Contradiction between abc123 and level. Unless in "level" the first
    # vowel considered is different. 
    #
    # Wait—maybe it inserts 'i' after the first vowel, but "abc123" the
    # first vowel 'a' is at position 0, and inserting after position 0
    # gives "aibc123". Observed "abci123". So no.
    #
    # Let me reconsider: maybe it's "insert i before the first occurrence
    # of a doubled... " no doubles.
    #
    # Maybe it's about the first letter that appears twice?
    #   level: 'l' appears at 0 and 5. 'e' at 1 and 3. First repeat: 'e'
    #   at index 3. Insert before? "leviel" has i at index 2. Hmm.
    #   Actually "leivel": positions l0 e1 i2 v3 e4 l5. So i inserted at 2,
    #   before the second 'e'? The second 'e' is at index 3 in "level".
    #   Inserting before it gives "lev" + i + "el" = "leviel". No, got "leivel".
    #   Inserting at index 2 (before 'v') gives "le"+"i"+"vel" = "leivel" ✓.
    #   So i before 'v' at index 2.
    #
    # Hmm, what if rule is: insert 'i' after the first vowel that is
    # followed by a consonant, where we take the LAST vowel before the
    # first consonant cluster... 
    #
    # Let me just try: insert 'i' after the first vowel (a,e,i,o,u) that
    # is followed by a consonant, but if that vowel is at index 0, use the
    # consonant cluster after it.
    #   abc123: 'a' at 0 followed by 'b' consonant -> cluster "bc" -> after
    #   -> "abci123" ✓
    #   level: 'e' at 1 followed by 'v' -> after 'e' -> "leivel" ✓
    #   Zebralower: 'e' at 1 followed by 'b' -> after 'e' -> "Zeibralower"
    #   ✗ (got Zebrialower, i after 'a' at index 4).
    #
    # Ugh. Zebralower: "Zebrialower" = Z e b r a i l o w e r. i at index 5,
    # after 'a' (index 4). So insert after 'a'.
    #
    # So for Zebralower, insert after 'a' not 'e'. Why? Maybe the LAST
    # vowel before a consonant cluster? "Zebra": Z e b r a. Vowels e(1), a(4).
    # Insert after a(4). "level": vowels e(1), e(3). Insert after e(1)?? 
    # That's the first, not last.
    #
    # Hmm inconsistent. Let me look again:
    #   level -> leivel: after e at index 1 (first e)
    #   Zebra -> Zeibra: after e at index 1 (first e)
    #   Zebralower -> Zebrialower: after a at index 4
    #   bananaUPPER -> bananiaUPPER: after n at index 5? "banan"+"i"+"aUPPER".
    #     Wait "bananaUPPER": b a n a n a U P P E R. i inserted at index 5
    #     (after 'n' at 4, before 'a' at 5). Hmm, or after 'n'? 
    #     "bananiaUPPER" = b a n a n i a U P P E R. So i at index 5, after
    #     the second 'n' (index 4), before 'a' (index 5).
    #   abc123 -> abci123: i at index 3, after 'c' (index 2), before '1'.
    #   function -> ifunction: i before 'f', after space.
    #
    # Insertion points (before which char):
    #   abc123: before '1' (digit)
    #   level: before 'v'
    #   Zebralower: before 'l'
    #   function: before 'f'
    #   bananaUPPER: before 'a'
    #   Zebra: before 'b'
    #
    # Chars before insertion: c, e, a, space, n, e
    # Chars after insertion: 1, v, l, f, a, b
    #
    # Hmm what if it's: insert 'i' before the first letter that comes
    # alphabetically after 'i'? 
    #   abc123: '1' < 'i'? '1' is 0x31 < 'i' 0x69. So '1' is before 'i'.
    #   Hmm.
    #
    # What if insert 'i' before the first char that is >= 'i' (0x69)?
    #   abc123: 'a'(0x61)<i, 'b'<i, 'c'<i, '1'<i... none >= i. But inserted.
    #
    # What if insert 'i' before the first char that is > 'i'? 
    #   abc123: '1' no... 
    #
    # Let me try: insert 'i' before the first char that is a consonant
    # after a vowel, but "consonant" excludes... 
    #
    # Actually, let me reconsider. Maybe the rule is about the first
    # character that is NOT a letter (digit, space)? 
    #   abc123: first non-letter is '1' at index 3 -> before it -> "abci123" ✓
    #   level: all letters. Hmm.
    #
    # Maybe: insert 'i' before the first character that is not lowercase
    # a-z? 
    #   abc123: '1' at 3 -> "abci123" ✓
    #   level: none. But inserted. ✗
    #
    # OK let me think about "level" and "Zebra" both inserting after 'e'
    # at index 1. And "Zebralower" inserting after 'a' at index 4. What's
    # different? "Zebralower" has "lower" after. Maybe it inserts before
    # a known word? "lower", "function"? And "level" -> "vel"? no.
    #
    # Maybe insert 'i' before the first occurrence of a letter that is
    # alphabetically after the previous letter? (i.e., an ascent)
    #   abc123: a->b ascent at index 1. Insert before 'b'? "aibc". no.
    #
    # Insert 'i' after the first ascent? 
    #   abc123: a->b at index 1, after 'b' -> "abi c123"? "abic123". no.
    #
    # Hmm. Let me look at "Zebra" -> "Zeibra". Insert after 'e'. 
    # "level" -> "leivel". Insert after 'e'. 
    # Both insert after the first 'e'. 
    # "Zebralower" -> "Zebrialower". Insert after 'a'. First 'a' is at index 4.
    # Why not after 'e' at index 1? 
    #
    # Unless... the rule involves the LAST vowel before a consonant cluster
    # that ends the "first syllable"? 
    #
    # Let me try a completely different angle: maybe it's inserting 'i'
    # after the first occurrence of a specific letter pattern based on
    # position parity or something.
    #
    # Insertion index: 3, 2, 5, 12, 5, 2
    # String lengths:   6, 5, 11, 26, 11, 5
    # Half lengths:     3, 2.5, 5.5, 13, 5.5, 2.5
    # Insertion index ≈ floor(length/2)? 
    #   abc123: floor(6/2)=3 ✓
    #   level: floor(5/2)=2 ✓
    #   Zebralower: floor(11/2)=5 ✓
    #   function string: length 26, floor=13. But insertion at 12. ✗ close.
    #   bananaUPPER: length 11, floor=5 ✓
    #   Zebra: length 5, floor=2 ✓
    #
    # Wow, mostly floor(length/2)! Let me check the function one:
    # "Hello World function lazy" length: H-e-l-l-o(5) space(6) W-o-r-l-d(11)
    # space(12) f-u-n-c-t-i-o-n(20) space(21) l-a-z-y(25). Length 25.
    # floor(25/2)=12. Insertion at 12 ✓!
    #
    # Let me recount: "Hello World function lazy"
    # H(0)e(1)l(2)l(3)o(4) (5)W(6)o(7)r(8)l(9)d(10) (11)f(12)u(13)n(14)
    # c(15)t(16)i(17)o(18)n(19) (20)l(21)a(22)z(23)y(24). Length 25.
    # floor(25/2) = 12. Insert 'i' at index 12 -> before 'f' -> 
    # "Hello World " + "i" + "function lazy" = "Hello World ifunction lazy" ✓
    #
    # Let me verify all:
    #   abc123: len 6, mid=3, insert at 3 -> "abc"+"i"+"123" = "abci123" ✓
    #   level: len 5, mid=2, insert at 2 -> "le"+"i"+"vel" = "leivel" ✓
    #   Zebralower: len 11, mid=5, insert at 5 -> "Zebra"+"i"+"lower" ✓
    #   bananaUPPER: len 11, mid=5, insert at 5 -> "banan"+"i"+"aUPPER" ✓
    #   Zebra: len 5, mid=2, insert at 2 -> "Ze"+"i"+"bra" = "Zeibra" ✓
    #
    # So the rule: insert 'i' at index floor(len(s)/2).
    # (For even length, that's the exact middle; for odd, just before middle.)
    #
    # This is a clean hypothesis. Let me write it.
    def predict(probe):
        out = []
        for s in probe.get("inputs", []):
            if not isinstance(s, str):
                s = str(s)
            mid = len(s) // 2
            out.append(s[:mid] + "i" + s[mid:])
        return {"outputs": out}
    return predict(probe)
