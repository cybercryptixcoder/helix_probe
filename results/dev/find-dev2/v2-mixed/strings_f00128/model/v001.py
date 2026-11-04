def predict(probe):
    # Observations:
    # - Digits are transformed: each digit d -> "10" + d? Let's check.
    #   "123" -> "11023": 1->"110"? Actually "1"->"110", "2"->"2", "3"->"3"? No.
    #   Let's parse: "123" -> "1 10 2 3"? = "11023". So '1'->'1', '2'->'10'+'2'? Hmm.
    #   "42" -> "4102" = "4"+"10"+"2"? So '4'->'4', '2'->'10'+'2'? No, "4102" = "4"+"10"+"2".
    #   "a1b2" -> "A110b2": 'a'->'A', '1'->'1', then "10"? Wait "A110b2" = A,1,1,0,b,2.
    #   Hmm '1'->'1', then '10' inserted before 'b'? No.
    # Let's reconsider: maybe each digit d -> "10"+d except... "123"->"11023".
    #   If each digit -> "10"+d: "123" -> "101"+"102"+"103" = "101102103". No.
    # Try: insert "10" before each digit run? "123" -> "10"+"123"="10123". No, got "11023".
    # Look: "123"->"11023". "1"->"1", "2"->"10"+"2"? "1"+"10"+"2"+"3"? = "11023". Yes!
    #   So '1'->'1', '2'->'102'? no "10"+"2"="102", then '3'->'3'. "1"+"102"+"3"="11023". Yes!
    #   But "42"->"4102": '4'->'4', '2'->"102"? = "4102". Yes!
    #   "a1b2"->"A110b2": a->A, '1'->'1', '10'? then b, 2. Hmm "A"+"1"+"10"+"b"+"2"="A110b2". Yes!
    #   So '1'->'1', '2'->'10'+'2'? But then where does "10" come from for '1'? 
    #   Wait "A110b2": A,1,1,0,b,2. That's 'a'->A, '1'->"1", then "10", then 'b', '2'.
    #   Actually maybe: '1'->"1", '2'->"10"+"2"="102"? But "A110b2" has "1"+"10"+"b"+"2". So '1'->"1", then "10" inserted, then b, then 2->"2". 
    # Hmm, let's look at "z9"->"Z109": z->Z, '9'->"109"? = "10"+"9". Yes!
    #   "9z"->"910z": '9'->"9", then "10", then z->"z"? = "9"+"10"+"z"="910z". Yes!
    #   "x 5 y"->"X 105 y": x->X, space, '5'->"5", "10", space, y. = "X"+" "+"5"+"10"+" "+"y"="X 105 y". Yes!
    #   "Hello123World"->"Hello11023world": H,e,l,l,o, '1'->"1", "10", '2'->"2", '3'->"3", W->w... = "Hello"+"1"+"10"+"2"+"3"+"world"="Hello11023world". Yes!
    #   "A1B2C3"->"A1b102c3": A, '1'->"1", B->b, "10", '2'->"2", C->c, '3'->"3" = "A"+"1"+"b"+"10"+"2"+"c"+"3"="A1b102c3". Yes!
    #   "ABC"->"A10bc": A, then "10", then B->b, C->c. So "10" inserted after first char? 
    #   "abc"->"A10bc": a->A, "10", b->b, c->c. Yes!
    #   "level"->"Le10vel": l->L, e->e, "10", v,e,l. So "10" inserted after 2nd char.
    #   "Zebra"->"Ze10bra": Z,e,"10",b,r,a. After 2nd char.
    #   "bananaUPPER"->"Banan10aupper": B,a,n,a,n,"10",a,u,p,p,e,r. After 5th char.
    #   "abc123"->"Abc10123": A,b,c,"10",1,2,3. After 3rd char.
    #   " Zebralower"->" zebr10alower": space,z,e,b,r,"10",a,l,o,w,e,r. After 5th char.
    #   "Hello World function lazy"->"Hello world 10function lazy": after "Hello world " (12 chars) insert "10".
    # So: "10" is inserted at some position. Where? 
    #   "abc"->after 1 char (A|10|bc). "level"->after 2 (Le|10|vel). "abc123"->after 3 (Abc|10|123).
    #   "bananaUPPER"->after 5 (Banan|10|aupper). " Zebralower"->after 5 ( zebr|10|alower).
    #   "Hello World function lazy"->after 12 (Hello world |10|function lazy).
    #   "Hello123World"->after 6 (Hello1|10|23world)? "Hello"+"1"+"10"+"2"+"3"+"world". Yes after 6.
    #   "A1B2C3"->"A1b102c3": A,1,b,10,2,c,3. After 3 chars (A1b|10|2c3). Yes.
    #   "z9"->"Z109": Z,10,9. After 1 char. "9z"->"910z": 9,10,z. After 1 char.
    #   "x 5 y"->"X 105 y": X,space,5,10,space,y. After 3 chars.
    #   "42"->"4102": 4,10,2. After 1 char. "123"->"11023": 1,10,23. After 1 char.
    #   "a1b2"->"A110b2": A,1,10,b,2. After 2 chars.
    # So insertion position = floor(len/2)? 
    #   abc len3 ->1 (floor 1). level len5->2. abc123 len6->3. bananaUPPER len11->5. 
    #   " Zebralower" len12->5? floor(12/2)=6, but got 5. Hmm.
    #   "Hello World function lazy" len26->12? floor=13. Got 12.
    #   "Hello123World" len13->6. floor=6. Yes.
    #   "A1B2C3" len6->3. Yes.
    #   "z9" len2->1. "9z" len2->1. "x 5 y" len5->3? floor=2. Got 3. Hmm.
    #   "42" len2->1. "123" len3->1. "a1b2" len4->2.
    # Let's recount "x 5 y": X,space,5,10,space,y. That's 3 chars before "10": X,space,5. len5, pos3 = ceil(5/2)=3.
    #   " Zebralower": len12, pos5 = ceil(12/2)=6? No, 5. Hmm.
    #   Wait " Zebralower" is space+Zebra+lower = 1+5+5=11 chars? space,Z,e,b,r,a,l,o,w,e,r = 11. ceil(11/2)=6, floor=5. Got 5. 
    #   "bananaUPPER" len11, pos5 = floor(11/2)=5. Yes.
    #   "Hello World function lazy": len? "Hello World function lazy" = 5+1+5+1+8+1+4=25. floor(25/2)=12. Got 12. Yes!
    #   "Hello123World" len13, floor=6. Yes.
    #   "x 5 y" len5, floor=2, but got 3. Hmm. Recount: X,space,5,10,space,y. Before 10: X,space,5 = 3. 
    #   Wait maybe "x 5 y" is x,space,5,space,y = 5 chars. floor(5/2)=2. But output "X 105 y" = X,space,1,0,5,space,y. 
    #   Oh! "X 105 y": X,space,1,0,5,space,y. So "10" is before '5'? No: X,space,"10",5,space,y. That's pos2! X,space = 2 chars. Yes floor(5/2)=2. 
    #   I misread. "X 105 y" = X,space,1,0,5,space,y. So "10" at pos2. Good.
    #   " Zebralower": " zebr10alower" = space,z,e,b,r,1,0,a,l,o,w,e,r. pos5. len11, floor=5. Yes!
    # So rule: lowercase all, capitalize first letter, insert "10" at position floor(len/2).
    # Check "abc"->"A10bc": A,10,b,c. pos1, len3 floor=1. Yes.
    # "level"->"Le10vel": L,e,10,v,e,l. pos2, len5 floor=2. Yes.
    # "abc123"->"Abc10123": A,b,c,10,1,2,3. pos3, len6 floor=3. Yes.
    # "Zebra"->"Ze10bra": Z,e,10,b,r,a. pos2, len5 floor=2. Yes.
    # "42"->"4102": 4,10,2. pos1, len2 floor=1. Yes.
    # "123"->"11023": 1,10,2,3. pos1, len3 floor=1. Yes.
    # "a1b2"->"A110b2": A,1,10,b,2. pos2, len4 floor=2. Yes.
    # "z9"->"Z109": Z,10,9. pos1, len2 floor=1. Yes.
    # "9z"->"910z": 9,10,z. pos1, len2 floor=1. Yes.
    # Capitalization: first char uppercased, rest lowercased. "ABC"->"A10bc": A,10,b,c. Yes.
    # "bananaUPPER"->"Banan10aupper": B,a,n,a,n,10,a,u,p,p,e,r. Yes lowercased rest.
    # "Hello World function lazy"->"Hello world 10function lazy": H,e,l,l,o,space,w,o,r,l,d,space,10,f... 
    #   Wait "Hello world 10function lazy": H,e,l,l,o,space,w,o,r,l,d,space,1,0,f,u,n,c,t,i,o,n,space,l,a,z,y.
    #   pos12 = after "Hello world " (12 chars). len25 floor=12. Yes.
    #   But "Hello World function lazy" lowercased rest: "hello world function lazy", capitalize first: "Hello world function lazy". Insert at 12: "Hello world " + "10" + "function lazy". Yes!
    # Great, consistent.
    import math
    def transform(s):
        if not s:
            return "10"  # ? empty case unknown
        t = s[0].upper() + s[1:].lower()
        pos = len(t) // 2
        return t[:pos] + "10" + t[pos:]
    return {"outputs": [transform(x) for x in probe["inputs"]]}
