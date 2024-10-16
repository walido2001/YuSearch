import json 


def add_json_entry(entry, file_path):
    with open(file_path, 'a') as file:
        json.dump(entry, file)
        file.write('\n')

def count_lines_in_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        return len(lines)