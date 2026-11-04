def predict(probe):
    # Observations [E1]:
    # - "apple" -> "app5lee": a '5' is inserted after the 3rd character.
    # - "test case " -> "test 5case  ": '5' inserted after "test " (5th char).
    # - "test caseMiXeD" -> "test ca5seMiXeDD": '5' after "test ca" (7th char), and a trailing 'D' appended.
    # - "data a Python " -> "data a 5Python  ": '5' after "data a " (7th char), trailing space appended.
    # - "test case Zebra" -> "test cas5e Zebraa": '5' after "test cas" (8th char), trailing 'a' appended.
    # - "Mississippi Hello World data" -> "Mississippi He5llo World dataa": '5' after "Mississippi He" (14th char), trailing 'a' appended.
    # Pattern hypothesis (?): insert '5' at position len//2 (integer division), then if len is odd append the last char again.
    # Check: len 5 -> pos 2? But observed pos 3. So not len//2.
    # Let's compute insertion index (0-based) and length:
    #  apple len5 -> idx3
    #  "test case " len10 -> idx5
    #  "test caseMiXeD" len14 -> idx7
    #  "data a Python " len14 -> idx7
    #  "test case Zebra" len15 -> idx8
    #  "Mississippi Hello World data" len28 -> idx14
    # idx = len//2 for even lengths (10->5,14->7,28->14). For odd: 5->3 (ceil?), 15->8 (ceil). So idx = (len+1)//2.
    # Trailing char duplication: odd lengths get last char appended (5->'e'? no, apple ends 'e', output ends "ee"? "app5lee" yes 'e' appended. len15 "Zebra"->"Zebraa" 'a' appended. len28 even, but "dataa" appended 'a'? len28 even yet appended.
    # Wait "Mississippi Hello World data" len: let's count: Mississippi(11)+space(1)+Hello(5)+space(1)+World(5)+space(1)+data(4)=28. Even, but output has trailing 'a'. Hmm.
    # "data a Python " len14 even, output "data a 5Python  " has extra trailing space -> appended last char ' '.
    # "test case " len10 even, output "test 5case  " extra space appended.
    # So maybe always append last char? Check "test caseMiXeD" len14 -> output ends "DD" yes appended 'D'. "apple" len5 -> "app5lee" appended 'e'. All append last char!
    # So rule: insert '5' at idx=(len+1)//2, then append original last char.
    def f(s):
        if not s:
            return s
        idx = (len(s) + 1) // 2
        return s[:idx] + "5" + s[idx:] + s[-1]
    return {"outputs": [f(x) for x in probe["inputs"]]}
