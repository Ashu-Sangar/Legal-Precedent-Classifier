# Count the number of cases ("rows") from a specific portion of the bulk data download

import os
import json

filecount = 0

for volume in range (1, 51): # Only loops over first 50 volumes of PA state data
    volume_path = os.path.join("..", "data", "Caselaw_Pennsylvania_State_Reports_1845-2017", str(volume), "json")
    if not os.path.isdir(volume_path):
        continue

    for file in os.listdir(volume_path):
        if not file.endswith(".json"):
            continue

        file_path = os.path.join(volume_path, file)

        with open(file_path, "r", encoding = "utf-8") as f:
            try:
                data = json.load(f)
                doc_id = str(data["id"]) # Use unique id from original data as the doc_id
                filecount += 1
            
            except Exception as e:
                print(f"Skipping {file_path} due to error: {e}")

print(filecount)