import json 


def add_json_entry(entry, file_path):
    with open(file_path, 'a') as file:
        json.dump(JSON(entry), file)
        file.write('\n')