"""DOC-2-079 frozen analysis (PROTOCOL.md lock-1). Run once. Needs dataset.tsv, emb.npy."""
import json, numpy as np, pandas as pd
rng = np.random.default_rng(12345)
d = pd.read_csv("dataset.tsv", sep="\t"); E = np.load("emb.npy"); fam = d.family.values; dark = (d.group == "dark").values; n = len(d)
AA = "ACDEFGHIKLMNPQRSTVWY"; C = np.array([[s.count(a) / len(s) for a in AA] + [np.log(len(s))] for s in d.sequence]); C = (C - C.mean(0)) / (C.std(0) + 1e-9)
def nn_hit(X, labels):
    X = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-12); S = X @ X.T; np.fill_diagonal(S, -np.inf); return labels[S.argmax(1)] == labels
hitE, hitC = nn_hit(E, fam), nn_hit(C, fam)
perm = rng.permutation(fam); hitP = nn_hit(E, perm)
uf = sorted(set(fam)); members = {u: np.where(fam == u)[0] for u in uf}
acc = lambda h, m: float(h[m].mean())
res = {"n": n, "n_families": len(uf), "n_dark": int(dark.sum()), "acc": {"E_dark": acc(hitE, dark), "E_char": acc(hitE, ~dark), "C_dark": acc(hitC, dark), "C_char": acc(hitC, ~dark)}}
res["G1"] = dict(perm_acc_dark=acc(hitP, dark), perm_acc_char=acc(hitP, ~dark), pass_=bool(acc(hitP, dark) < 3.0 / len(uf) and acc(hitP, ~dark) < 3.0 / len(uf)))
bs = {"dark": [], "gap": []}
for _ in range(2000):
    idx = np.concatenate([members[u] for u in rng.choice(uf, len(uf))]); dd = dark[idx]
    a, b = hitE[idx][dd].mean(), hitE[idx][~dd].mean(); bs["dark"].append(a); bs["gap"].append(b - a)
ci = lambda k: [float(x) for x in np.percentile(bs[k], [2.5, 97.5])]
ad = res["acc"]["E_dark"]; gap = res["acc"]["E_char"] - ad
res["G2"] = dict(acc_dark=ad, ci=ci("dark"), pass_=bool(ad >= 0.50 and ci("dark")[0] > 0.40))
res["G3"] = dict(gap_char_minus_dark=gap, ci=ci("gap"), pass_=bool(gap >= 0.05 and ci("gap")[0] > 0), label="DARK-IS-DARKER" if (gap >= 0.05 and ci("gap")[0] > 0) else "NO-DEFICIT")
res["LABEL"] = "INVALID" if not res["G1"]["pass_"] else ("HONEST NEGATIVE" if not res["G2"]["pass_"] else "ORGANISED-" + res["G3"]["label"])
print("RESULT_JSON", json.dumps(res, default=float)); open("results.json", "w").write(json.dumps(res, default=float, indent=1))
