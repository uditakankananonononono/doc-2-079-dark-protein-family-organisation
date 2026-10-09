"""DOC-2-079: build dataset.tsv (accession, family, group, length, sequence). Needs dark_raw.tsv and the frozen DOC-2-072 uniprot_raw.tsv (md5 aa086b6e99d5e84c44789b1a85bc71f1)."""
import hashlib, io, numpy as np, pandas as pd
raw = open("uniprot_raw.tsv").read(); assert hashlib.md5(raw.encode()).hexdigest() == "aa086b6e99d5e84c44789b1a85bc71f1"
def fam(d, pc):
    d["pf"] = d[pc].fillna("").str.strip(";").str.split(";"); d = d[d.pf.str.len() == 1].copy(); d["family"] = d.pf.str[0]; return d
c = pd.read_csv(io.StringIO(raw), sep="\t"); c.columns = ["accession", "ec", "pfam", "length", "sequence"]; c = fam(c, "pfam"); c["group"] = "characterized"
k = pd.read_csv("dark_raw.tsv", sep="\t"); k.columns = ["accession", "name", "pfam", "length", "sequence"]; k = fam(k, "pfam"); k["group"] = "dark"
bad = "[XBZUO]"; k = k[~k.sequence.str.contains(bad)]; c = c[~c.sequence.str.contains(bad) & ~c.accession.isin(k.accession)]
cols = ["accession", "family", "group", "length", "sequence"]; a = pd.concat([c[cols], k[cols]]).drop_duplicates("accession").sort_values("accession")
cnt = a.groupby(["family", "group"]).size().unstack(fill_value=0); ok = sorted(cnt[(cnt.get("dark", 0) >= 10) & (cnt.get("characterized", 0) >= 10)].index)
rng = np.random.default_rng(79)
if len(ok) > 150: ok = sorted(rng.choice(ok, 150, replace=False))
out = []
for f in ok:
    for g in ("dark", "characterized"):
        s = a[(a.family == f) & (a.group == g)]; out.append(s.iloc[np.sort(rng.choice(len(s), 10, replace=False))])
o = pd.concat(out); o.to_csv("dataset.tsv", sep="\t", index=False)
print("SAMPLE_DONE families", len(ok), "n", len(o), o.group.value_counts().to_dict())
