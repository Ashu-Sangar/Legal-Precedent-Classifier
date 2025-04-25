import os
import json
from pyserini.search.lucene import LuceneSearcher

index_path = "indexes_640"
corpus_path = "indexed_case_corpus_vol_1-640_for_pyserini"

searcher = LuceneSearcher(index_path)

print('Welcome to the Legal Precedent Search (BM25) Demo!')

while True:
    case_id = input('\nEnter case ID (or "exit", "quit"): ').strip()
    if case_id.lower() in ['exit', 'quit']:
        break

    json_path = os.path.join(corpus_path, f"{case_id}.json")
    if not os.path.exists(json_path):
        print("Case ID not found.")
        continue

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            query_text = data.get("contents", "").strip()
            tokens = query_text.split()
            truncated_query = ' '.join(tokens[:1024])
    except Exception as e:
        print(f"Error reading document: {e}")
        continue

    hits = searcher.search(truncated_query, k=100)

    print("\nPreview of top 15 retrieved documents:\n" + "-" * 50)
    for i, hit in enumerate(hits[:15]):
        doc = searcher.doc(hit.docid)
        raw = doc.raw()
        print(f"{i+1}. case_id: {hit.docid}, score: {hit.score:.4f}")

        print(raw[:1000] + "\n...")
        # formatted_raw = raw[:1000].replace("\\n", " ").replace("\\t", " ")
        # print(formatted_raw + "\n...")

        print("-" * 50)
    top_doc_ids = [hit.docid for hit in hits]
    print("\nList of top 100 retrieved documents:")
    print(top_doc_ids)