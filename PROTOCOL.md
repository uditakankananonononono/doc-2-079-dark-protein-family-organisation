# DOC-2-079 "Protein dark matter atlas, step 1": do ESM-2 embeddings organise "uncharacterized" proteins by Pfam family as well as characterized ones? (frozen protocol, lock-1)

Written 2026-10-09 IST and committed BEFORE the dark-protein set was downloaded or any sampling/embedding. The ledger holds only the title and source line for DOC-2-079 (no spec text), so this is a narrow, checkable first step, not the full atlas.

## Why this is not a re-ask
- DOC-2-073/077/009-R3/R4: ESM-2 zero-shot variant-effect rho vs features. Not touched.
- DOC-2-072: random vs family-held-out EC classification (family identity carries the signal). DOC-2-078: agreement as correctness flag. This protocol asks something different: nearest-neighbour family recovery, split by annotation status (dark vs characterized), with family held constant. No EC classification, no train/test models.
- Prior art: protein language model embeddings cluster by family is well known. Not claimed as novel; the question is whether proteins UniProt names "uncharacterized" are organised as well as EC-annotated ones.

## Data (frozen)
- Dark: UniProtKB reviewed entries with protein name containing "uncharacterized", at least one Pfam, length 100-400, no EC (acquire_dark.py; release and md5 recorded in DATA_HASHES.tsv).
- Characterized: EC-annotated reviewed entries from the frozen DOC-2-072 raw TSV (md5 aa086b6e99d5e84c44789b1a85bc71f1, release 2026_03), excluding any accession also in the dark set. "Characterized" here means EC-annotated, not all non-dark.
- Keep exactly one Pfam id per protein; drop X/B/Z/U/O residues. Keep families with >= 10 dark and >= 10 characterized. Sample up to 150 families (seed 79), then exactly 10 dark and 10 characterized proteins per family (sample_079.py). Expect n about 3,000.
- Features: ESM-2 35M mean-pooled embeddings (embed.py identical to DOC-2-072's, md5 8437eda4de9a3e4c05a98684e6cb9623). C baseline: 20 AA frequencies + log length (z-scored).

## Method
- For each protein, cosine 1-nearest-neighbour over all other proteins in the sample (both groups pooled, self excluded). Hit = neighbour has the same Pfam family. No model fitting.
- accuracy by group; family-cluster bootstrap (2,000, seed 12345, percentile 95%) over families.

## Gates
- G1 (control): 1-NN hit rate with family labels permuted across proteins is < 3 / n_families for both groups. Failure = INVALID, protocol stop.
- G2: E dark-group 1-NN family accuracy >= 0.50 and CI lower bound > 0.40 (embeddings organise dark proteins by family).
- G3: characterized minus dark accuracy >= 0.05 with CI lower bound > 0 gives DARK-IS-DARKER, else NO-DEFICIT. Reported tag; the label combines it.
- Label (mechanical): INVALID if G1 fails; HONEST NEGATIVE if G2 fails; ORGANISED-DARK-IS-DARKER or ORGANISED-NO-DEFICIT otherwise.

## Limits stated up front
- Family is Pfam family, so "dark" proteins here already have a Pfam domain; truly unannotated proteins (no Pfam) are outside this design. Families with both groups are not representative of all dark proteins.
- Near-identical homologs inside a family (including duplicates) make 1-NN easy for both groups; no redundancy filtering is applied, so absolute accuracy is inflated. Only the dark-vs-characterized comparison within the same families is the target.
- "Characterized" = EC-annotated; names and annotation status in UniProt reflect curation history. Dark proteins may be annotated in other ways.
- The ledger gives no spec text for DOC-2-079; this does not claim to cover the atlas idea, only step 1.
- C baseline (composition) is descriptive and cannot change the label. One model size, one pooling, single seed, CPU only. No simulated data in results. Smoke test of analysis_079.py was on synthetic embeddings only, no record saved.
- Single run; crash fixes are dated AMENDMENT-N.md files committed before outcomes exist.
