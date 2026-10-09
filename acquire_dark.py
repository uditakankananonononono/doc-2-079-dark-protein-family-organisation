"""DOC-2-079: fetch reviewed UniProt entries named 'uncharacterized' with Pfam, length 100-400, no EC. Writes dark_raw.tsv, DATA_HASHES.tsv."""
import time, hashlib, io, requests, pandas as pd
Q = "reviewed:true AND protein_name:uncharacterized AND xref:pfam-* AND length:[100 TO 400] AND NOT ec:*"
url = "https://rest.uniprot.org/uniprotkb/search"; params = dict(query=Q, fields="accession,protein_name,xref_pfam,length,sequence", format="tsv", size=500)
rows, rel, first = [], None, True
while url:
    for attempt in range(6):
        try:
            r = requests.get(url, params=params if first else None, timeout=120); r.raise_for_status(); break
        except requests.exceptions.RequestException as ex:
            print("retry", attempt, type(ex).__name__, flush=True); time.sleep(5 * (attempt + 1))
    else: raise SystemExit("acquisition failed")
    first = False; rel = r.headers.get("x-uniprot-release", rel); lines = [x for x in r.text.split("\n") if x]; rows += lines[1:] if rows else lines
    url = r.links.get("next", {}).get("url")
raw = "\n".join(rows) + "\n"; open("dark_raw.tsv", "w").write(raw)
open("DATA_HASHES.tsv", "w").write(f"file\tmd5\tuniprot_release\tn_rows\ndark_raw.tsv\t{hashlib.md5(raw.encode()).hexdigest()}\t{rel}\t{len(rows)-1}\n")
print("DARK_DONE release", rel, "rows", len(rows) - 1)
