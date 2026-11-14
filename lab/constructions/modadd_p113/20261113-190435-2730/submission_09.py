
DESCRIPTION = (
 "Input is [i, j, 113]: two variable tokens plus a constant third token; output = 113 logits, decision = argmax. "
 "Attention at the last position is essentially uniform (each head ~1/3 per position, std 0.001), so it is a plain "
 "average of the three positions. Hence every site up to mlp_pre is exactly affine in the two one-hot token "
 "variables ti = row i of I_114 (at position 0) and tj = row j of I_114 (at position 1): explained 1.000 at embed.0/1, "
 "attn_out, resid_mid, mlp_pre. The MLP adds relu(c+P[i]+Q[j]) which keeps the map near-affine (relu kinks spread "
 "over ~300 of 512 neurons; the non-additive part is 0.8% of logit variance; mlp_post 0.96, mlp_out 0.96, resid_post "
 "0.99 explained by ti,tj). The readout is therefore an additive token score: logit[i,j][c] = mu[c] + F[i][c] + "
 "F[j][c], and the decision is the argmax over the 113 classes. Only 8 classes ever reach the top (97 wins 96.6% of "
 "inputs; 85, 14, 47, 105, 98 are the alternatives), so mu is stored for all classes and F only for those 8. "
 "mu and F are packed two base-36 characters per value.")

import numpy as np
DIG = "0123456789abcdefghijklmnopqrstuvwxyz"

def unpack(s, off, sc):
    a = np.frombuffer(s.encode(), dtype=np.uint8).astype(np.int64)
    v = np.zeros(a.size, dtype=np.int64)
    for k, d in enumerate(DIG):
        v[a == ord(d)] = k
    v = v.reshape(-1, 2)
    return off + (sc / 1295.0) * (v[:, 0] * 36 + v[:, 1])

MU = unpack(
 "hmagfid1chabdd9kgzcuf3bfath1ssi1ewc9kmcvlee3488gbu6u3vg4erhtdzbh4ibj9fbf6zedgmdwf2cvcs38kocylbrgegaahd5scu8pg67j5ab"
 "tbsmecmfycdbtd9hsa6a60kbbdqcq3ung7h2zam8jl291cmd4ixe7cjrajzbqfairaobabkat7a865sy1mre49fhhfnb53xps5f95fudvini3bw",
 -0.4, 1.1)
TOP = [97, 14, 47, 85, 105, 73, 98, 59]
F8 = unpack(
 "lwn1digrgogecaj0bml3hfnqelizhnibf8jcmqjtewo4pxebomjchqjpediykyijgokbf6ffg1idn0gnftfxgah1gvjxdph5fzi7iqg5fwm8l3kqlkfplbj7illj"
 "gbf7gxgxdpepq0n4mhk6jnn5f3fkbieibwlbnchtjmj2ilfqdoi6fvmbhxmjeaecfqmxc2jdi3lfmajqjsemejhzkupsn1mjmemlp9htiulsgphthdfpkohdgyepf"
 "khthujbjuiml8pwetigj0kylohjmpmckrh5hfhojyimhbimnim6dlcnkliwgjhnkre1b8eznnjym8gzhmdmjwcyh1k5cbjvkodmk9g4jtjij5mzjlgom7hri0k3"
 "mrhcivgwnfh8f4ifedlhixiegjegg4gwkvlfnoneisfldaf0nhh6d3nnj4lvormfmdofk4g0c0odapdof9j5h7e5e9gkewindni0iajadgoslnn0krfbezlpjris"
 "k6hvn8p6idm9j2jzeal1gdkygkcuh8fqgai5j9hhf5gdftlek0gtfgkrkkn6mbhxinj1gem5b9igiki9iehwdl9wm3lpgug0fydehvexk6hulpcorrn4mbi6hqg"
 "yk1mefdgrkzcggvoejzf5lrlbn7rvj0l3nzguiphch9gjhpikfhmdf6exibj6ihjrbkg9kzj6m99cnnhsisk3g2g7i6q4hwgcumkpimjodsgqmkewhokwj5ioiyo"
 "vicnpl1gpe0euj4ikfzl6h6jbmbf3lymhh7e8alhieog7efj7iqj3knk8icjnjtiln9mumdj3hhcillmicvjgimjjh1dcdkcngjijitdvp7m8jjlfjtj7joj8jqim"
 "e7myn8d7i0adkjd7o9doe4h9jjjmk3jcl3g5loo7jfi7fqh0iriejwh0bwlumfjnl7johzgslakpifllh4o9l4l6pagwhzasjog4cvhogrk68kbci4h3dofrhof3"
 "k3lajykplzhfjidlmyjhmqnml3pakbmxhaevf29ceng9iohlgzibjrn6jenbp4hde7f4i9ifingwg1k7ilh6h69yorfoh9gvf4cumnhpedjscpl3jcipl2g6asc"
 "gd9iki9mhhremlietfgep9edqd3enkok7e4mjgyhqgagyjhgjllhviagrj5bgf1e5g7i8kqj8msq5jcgdjhimllhbf7ivikiii6ksmzffjil4gxcwdvq2fkhe"
 "h1echihzdnhzf5i6l2fhmcevd6g0dpk3gwfbkjkugnexfceefgedefjtf9kqigk1fqfnh2jqoji8j1gcitgcdyhiexkvkhk2kxk7mijag5m6ndhscsjdihcwi"
 "ienh2hnhxkuihi1lvebebh0hvffkalkh4e4iqgjh0jbflelm0doj2ihkojwq0j6hvj3owk7lbhvmuhulkcag4jukmfdgrg0lwf4behchchzn0kwoof1bqldfmiz"
 "jmimijftbii6dscbjjgfg4g1g0ikiui8ekjpebnnjkm0jnfufwk7ikisl9kidlfzmmjcioi09xbrgcdiipl0izhokyicjgf7djesazltf2g4d0jqjqebg7grg2"
 "f0eeb7j0mbigenicfef6d5hhfvc8lgq0tfdrf9ldfrl6hwoylmhki2h8d9e2jhmelgkffig5e6jjh8j6k7i9kbiimjnskij4fll8qdeeg8f7kmsoowj9fuhybph"
 "uhnnmmnj2j2dakyksoon7l3jch8eji0k8gehshdhmlribeimig1jxk0iodbkjj2gig7k6kjh7inh7gugxjui0i0i0i0i0i0i0i0", -0.25, 0.5).reshape(114, 8)

def model(x, iv):
    B = x.shape[0]
    ti = iv("ti", np.eye(114)[x[:, 0]])
    tj = iv("tj", np.eye(114)[x[:, 1]])
    lg = np.repeat(MU[None, :], B, 0)
    lg[:, TOP] = lg[:, TOP] + ti @ F8 + tj @ F8
    return lg

SITES_ALL = ["attn_out", "resid_mid", "mlp_pre", "mlp_post", "mlp_out", "resid_post"]
ALIGN = {"ti": ["embed.0"] + SITES_ALL, "tj": ["embed.1"] + SITES_ALL}
