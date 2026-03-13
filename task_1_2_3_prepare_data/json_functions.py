import json
import glob


# Merge all json files from a folder into one json file.
def merge_json_files(folder_path, output_file):
    merged_objects = []

    # Collect all JSON objects:
    for filename in glob.glob(folder_path + '/*.json'):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            merged_objects.extend(data)

    # Write the merged list to a new JSON file:
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(merged_objects, outfile, ensure_ascii=False, indent=4)


# Removes offers that have identical features but different prices, due to parameters that were not scraped (such as the existence of balcony).
def remove_duplicates(json_file):
    cnt_removed = 0

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    keys_to_group = [k for k in data[0].keys() if k != 'price']
    unique_objects = {}

    # Go through a file object by object, and save only first occurrences of identical objects:
    for obj in data:
        key = tuple((k, obj[k]) for k in keys_to_group)  # Creates a tuple key based on all fields except price.

        if key not in unique_objects:
            unique_objects[key] = obj
        else:
            cnt_removed += 1

    # Save the filtered data into a new JSON file:
    filtered_data = list(unique_objects.values())
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=4)

    print(f"Removed {cnt_removed} duplicates.")