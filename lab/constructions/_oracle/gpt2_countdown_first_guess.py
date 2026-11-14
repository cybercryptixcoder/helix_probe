DESCRIPTION = "Hand-written reference (not made by the constructor): identities of n3, n4 at their positions; by depth 6 the n4 position holds n4 and the direction; by depth 9 both are at the end position; the answer n4 + direction is formed there."
def oh(v):
    return np.eye(362)[np.clip(np.asarray(v), 0, 361).astype(int)]
def model(x, iv):
    n3 = iv("n3", oh(x[:, 2])); n4 = iv("n4", oh(x[:, 3]))
    n3b = iv("n3_b", oh(n3.argmax(1))); n4b = iv("n4_b", oh(n4.argmax(1)))
    a3, a4 = n3b.argmax(1), n4b.argmax(1)
    n4m = iv("n4_mid", oh(a4)); d = iv("dir", np.where(a4 >= a3, 1.0, -1.0))
    n4e = iv("n4_end", oh(n4m.argmax(1))); de = iv("dir_end", d)
    ans = iv("answer", oh(n4e.argmax(1) + np.where(de >= 0, 1, -1)))
    return 10.0 * ans
ALIGN = {"n3": ["resid0@n3"], "n4": ["resid0@n4"], "n3_b": ["resid3@n3"], "n4_b": ["resid3@n4"],
         "n4_mid": ["resid6@n4"], "dir": ["resid6@n4"], "n4_end": ["resid9@end"], "dir_end": ["resid9@end"], "answer": ["resid12@end"]}
