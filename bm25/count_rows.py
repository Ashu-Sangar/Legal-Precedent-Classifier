# Count the number of cases ("rows") from a specific portion of the bulk data download

import os
import json

file_count = 0
num_vols = 0

expected_vols = set(range(1, 640)) # volumes 1 through 639 of PA state data (all volumes)
identified_vols = set()

for volume in expected_vols:
    num_vols += 1
    volume_path = os.path.join("..", "data", "Caselaw_Pennsylvania_State_Reports_1845-2017", str(volume), "json")
    if not os.path.isdir(volume_path):
        continue

    identified_vols.add(volume)

    for file in os.listdir(volume_path):
        if not file.endswith(".json"):
            continue

        file_path = os.path.join(volume_path, file)

        with open(file_path, "r", encoding = "utf-8") as f:
            try:
                data = json.load(f)
                doc_id = str(data["id"]) # Use unique id from original data as the doc_id
                file_count += 1
            
            except Exception as e:
                print(f"Skipping {file_path} due to error: {e}")


missing_vols = expected_vols - identified_vols

print('number of volumes: ' + str(num_vols))
print('number of cases: ' + str(file_count))
print(f'missing volumes: {sorted(missing_vols)}')