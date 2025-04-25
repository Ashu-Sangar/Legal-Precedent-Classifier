# Preprocessing: Convert Caselaw JSON files (PA State Volumes 1-640) to Pyserini Index Format

import os
import json
from tqdm import tqdm

output_dir = "indexed_case_corpus_vol_1-640_for_pyserini"
os.makedirs(output_dir, exist_ok = True)

expected_vols = set(range(1, 640)) # volumes 1 through 639 of PA state data, plus the strange volume 81-12 (all volumes)
expected_vols.add("81-12")

# Loop over unzipped bulk data download from Caselaw and convert
# to pyserini json format to prepare for document indexing.
{
    "id": "doc1",
    "contents": "this is the contents."
}
for volume in tqdm(expected_vols, desc="Processing volumes", unit="vol"):
    volume_path = os.path.join("..", "data", "Caselaw_Pennsylvania_State_Reports_1845-2017", str(volume), "json")

    if not os.path.isdir(volume_path):
        continue

    for file in os.listdir(volume_path):
        if not file.endswith(".json"):
            continue

        file_path = os.path.join(volume_path, file)
        tqdm.write(f"Processing {file_path}...")

        with open(file_path, "r", encoding = "utf-8") as f:
            try:
                data = json.load(f)
                doc_id = str(data["id"]) # Use unique id from original data as the doc_id

                # The "contents" will be the "name_abbreviation" (case name abbreviation), 
                # "decision_date", "head_matter", "opinions", "name" (full case name)
                name_abbreviation = data.get("name_abbreviation", "")
                decision_date = data.get("decision_date", "")
                head_matter = data.get("casebody", {}).get("head_matter", "")
                name = data.get("name", "")
                opinion_text = ""
                opinions = data.get("casebody", {}).get("opinions", [])
                if opinions and "text" in opinions[0]:
                    opinion_text = opinions[0]["text"].strip()

                # skip file if all sections are empty
                if not any([name_abbreviation, decision_date, head_matter, opinion_text, name]):
                    print(f"Skipping {file_path} due to lack of usable content.")
                    continue

                contents = (
                    f"{name_abbreviation} "
                    f"{decision_date} "
                    f"{head_matter} "
                    f"{opinion_text} "
                    f"{name}"
                )

                converted = {"id": doc_id, "contents": contents}

                output_path = os.path.join(output_dir, f"{doc_id}.json")

                with open(output_path, "w", encoding = "utf-8") as out_f:
                    json.dump(converted, out_f)
            
            except Exception as e:
                print(f"Skipping {file_path} due to error: {e}")

# next, run in terminal while still in bm25 folder directory
#
# python -m pyserini.index.lucene \
#   --collection JsonCollection \
#   --input indexed_case_corpus_vol_1-640_for_pyserini \
#   --index indexes_640 \
#   --generator DefaultLuceneDocumentGenerator \
#   --threads 4 \
#   --storePositions --storeDocvectors --storeRaw