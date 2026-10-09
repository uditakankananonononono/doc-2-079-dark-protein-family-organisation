# DOC-2-079 (step 1) RESULTS - review pending (independent gate has not cleared; no claim is final)

Label (set mechanically by analysis_079.py): **ORGANISED-NO-DEFICIT**. G1 pass, G2 pass, G3 fail (no deficit detected). Reported with a large sample-size caveat: only 17 families met the frozen inclusion rule.

| item | value |
|---|---|
| data | UniProt 2026_03; dark = reviewed, name contains "uncharacterized", Pfam, 100-400 aa, no EC (5,627 rows fetched); characterized = EC-annotated from the frozen DOC-2-072 raw TSV |
| families meeting the rule (>= 10 dark and >= 10 characterized, single Pfam) | **17** (the protocol said "up to 150"; the rule produced 17, no deviation) |
| sample | 340 proteins = 17 families x (10 dark + 10 characterized) |
| G1 control (permuted family labels, 1-NN hit rate) | dark 0.082, characterized 0.065; threshold < 3/17 = 0.176; pass (chance is about 1/17 = 0.059) |
| ESM-2 35M 1-NN family accuracy, dark | 0.982 (167/170), 95% family-bootstrap CI [0.965, 1.000] |
| ESM-2 35M 1-NN family accuracy, characterized | 0.994 (169/170) |
| G2 (dark accuracy >= 0.50, CI lb > 0.40) | pass |
| G3 (characterized minus dark) | +0.012, CI [-0.012, +0.035]; needed >= 0.05 and CI lb > 0: fail -> NO-DEFICIT |
| composition baseline C, 1-NN (descriptive) | dark 0.706, characterized 0.641 |

## What this shows and does not show
- In the 17 families that contain both dark and EC-annotated proteins, ESM-2 nearest neighbours recover the Pfam family for 98% of dark proteins, essentially the same as for characterized ones. No dark-specific deficit was detected, but the test could only rule out gaps larger than about 0.035 (CI upper bound) and both groups sit near the ceiling.
- Ceiling and redundancy: no redundancy filter was applied (as registered). Within a Pfam family, near-identical homologs make 1-NN easy for both groups, so 0.98 reflects close relatives being present, not how well embeddings place a protein with no close relative. The study was not designed to measure that.
- Sampling limit: families with >= 10 dark and >= 10 EC-annotated reviewed proteins are only 17 of the Pfam families, so this is a small, non-representative slice (families in which uncharacterized and enzyme-annotated proteins coexist). It says nothing about proteins with no Pfam domain, which is where the dark-matter idea mostly lives.
- "Characterized" means EC-annotated only; non-EC proteins with known function are not in that group.
- The composition baseline is descriptive; dark 0.706 vs characterized 0.641 is not tested and cannot change the label.
- Small n: with 17 families the family bootstrap has wide uncertainty on G3's side; G2 is far from its threshold (CI lower bound 0.965 vs 0.40).
- Step 1 only: the ledger gives no spec text for DOC-2-079 and this does not cover the full atlas idea.

## Disclosures
- Run once. analysis_079.py md5 d9b2aef7e8a47a34e622c3ccd9278d73 equals the lock-1 file; tag_tree_check.txt records the lock-1 tag tree (5 files). run_log.txt: UTC 16:58:58-16:59:01, exit 0, python 3.10.12, numpy 2.2.6, pandas 2.3.3, torch 2.14.1+cpu, transformers 5.19.0. input_md5.txt holds md5s of dataset.tsv, emb.npy, dark_raw.tsv, uniprot_raw.tsv and the four scripts. embed.py ran as locked; no amendments were needed.
- "Smoke test on synthetic data" is a builder statement; no record saved.
- Single seed (79 for sampling, 12345 for bootstrap), one model size, one pooling, CPU only.
- Large files: dark_raw.tsv, dataset.tsv and emb.npy are in the Drive folder; the DOC-2-072 raw TSV is in that project's Drive folder (md5 aa086b6e99d5e84c44789b1a85bc71f1).
