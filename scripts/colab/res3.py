import json, glob
for f in sorted(glob.glob("/content/helix_probe/runs/edit/*/result.json")):
    r = json.load(open(f))
    if r["arm"] in ("helix2",) or (r["arm"]=="helix" and r["rep"]==1):
        print(f.split("/")[-2], "CLEAN" if r["clean"] else "removed" if r["removed"] else "no", "target", r["scores"]["target"], "comeback", round(r["comeback"],2), "ppl", r["ppl"], "post", r.get("post"), "changed", r["changed_params"], "cands", r.get("candidates"), "delivered", r.get("delivered"), {k: v for k, v in r["scores"].items() if k != "target"})
