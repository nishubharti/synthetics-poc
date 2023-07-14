#!/usr/bin/env python3

import os
import json
import tempfile
from git import Repo

def find_repeat_value(data):
    repeat = None

    if isinstance(data, dict):
        if "repeat" in data:
            repeat = data["repeat"]
        else:
            for value in data.values():
                repeat = find_repeat_value(value)
                if repeat:
                    break
    elif isinstance(data, list):
        for item in data:
            repeat = find_repeat_value(item)
            if repeat:
                break

    return repeat

def get_relative_path(file_path, base_dir):
    return os.path.relpath(file_path, base_dir)

def create_config(github_url):
    config = {}

    with tempfile.TemporaryDirectory() as temp_dir:
        repo = Repo.clone_from(github_url, temp_dir)

        for root, dirs, files in os.walk(temp_dir):
            for filename in files:
                if filename.endswith(".json"):
                    file_path = os.path.join(root, filename)
                    with open(file_path, "r") as file:
                        data = json.load(file)
                        repeat = find_repeat_value(data)

                        if repeat:
                            if repeat not in config:
                                config[repeat] = {
                                    "Github": github_url,
                                    "paths": []
                                }
                            relative_path = get_relative_path(file_path, temp_dir)
                            config[repeat]["paths"].append(relative_path)

    with open("config.json", "w") as file:
        json.dump(config, file, indent=4)

    print("config.json created successfully!")

github_url = "https://github.ibm.com/Nishu-Bharti1/Sc123"
create_config(github_url)