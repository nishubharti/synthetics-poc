import os
import json
from collections import defaultdict

def find_repeat(data):
    repeat = data.get("repeat")
    if repeat:
        return repeat
    else:
        for value in data.values():
            if isinstance(value, dict):
                repeat = find_repeat(value)
                if repeat:
                    return repeat
    return None

def create_config(folder_path):
    config = []
    entries_by_repeat = defaultdict(list) 
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if filename.endswith(".json") and os.path.isfile(file_path):
            with open(file_path, "r") as file:
                data = json.load(file)         
                repeat = find_repeat(data)
                path = file_path

               
                if not repeat:
                    continue


                entries_by_repeat[repeat].append(path)

    for repeat, paths in entries_by_repeat.items():
        config_entry = {
            "repeat": repeat,
            "paths": paths
        }
        print("**type of config_entry here is**",type(config_entry))
        config.append(config_entry)

    with open("config.json", "w") as file:
        json.dump(config, file, indent=4)

    print("config.json created successfully!")

folder_path = "/Users/nishubharti/go/src/github.ibm.com/Nishu-Bharti1/Sc123/test-groups/ping"
create_config(folder_path)