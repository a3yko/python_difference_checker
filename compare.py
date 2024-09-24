import yaml
import sys
from collections import OrderedDict

def load_yaml(filename):
    with open(filename, 'r') as file:
        return yaml.safe_load(file)

def compare_dicts(dict1, dict2, path=''):
    added = {}   # Stores keys present in dict2 but not in dict1
    removed = {} # Stores keys present in dict1 but not in dict2
    modified = {}# Stores keys present in both but with different values

    # Collect all unique keys from both dictionaries
    all_keys = set(dict1.keys()).union(set(dict2.keys()))

    for key in all_keys:
        # Track the current path for nested keys
        current_path = f'{path}.{key}' if path else key

        if key not in dict1:
            # Key is in dict2 but not dict1 (added)
            added[current_path] = dict2[key]
        elif key not in dict2:
            # Key is in dict1 but not dict2 (removed)
            removed[current_path] = dict1[key]
        else:
            # Key exists in both, so compare values
            value1 = dict1[key]
            value2 = dict2[key]

            if isinstance(value1, dict) and isinstance(value2, dict):
                # Recursively compare nested dictionaries
                sub_added, sub_removed, sub_modified = compare_dicts(value1, value2, current_path)
                added.update(sub_added)
                removed.update(sub_removed)
                modified.update(sub_modified)
            elif isinstance(value1, list) and isinstance(value2, list):
                # Compare lists (assuming compare_lists function exists)
                list_added, list_removed, list_modified = compare_lists(value1, value2, current_path)
                added.update(list_added)
                removed.update(list_removed)
                modified.update(list_modified)
            elif value1 != value2:
                # Values differ, so mark as modified
                modified[current_path] = (dict1[key], dict2[key])

    return added, removed, modified


def compare_lists(list1, list2, path):
    added = {}   # Stores items present in list2 but not in list1
    removed = {} # Stores items present in list1 but not in list2
    modified = {}# Stores items that are different between the two lists

    # Convert both lists into dictionaries using the first key of each item as the unique key
    dict1 = {item[list(item.keys())[0]]: item for item in list1}
    dict2 = {item[list(item.keys())[0]]: item for item in list2}

    # Get all unique keys from both dictionary representations of the lists
    all_keys = set(dict1.keys()).union(set(dict2.keys()))

    for key in all_keys:
        # Track the current path in the list for changes
        current_path = f'{path}[{key}]'

        if key not in dict1:
            # Item is in list2 but not in list1 (added)
            added[current_path] = dict2[key]
        elif key not in dict2:
            # Item is in list1 but not in list2 (removed)
            removed[current_path] = dict1[key]
        else:
            # Item exists in both, so compare the values
            value1 = dict1[key]
            value2 = dict2[key]

            if isinstance(value1, dict) and isinstance(value2, dict):
                # If the items are dictionaries, compare them recursively
                sub_added, sub_removed, sub_modified = compare_dicts(value1, value2, current_path)
                added.update(sub_added)
                removed.update(sub_removed)
                modified.update(sub_modified)
            else:
                # If the items differ, mark them as modified
                if value1 != value2:
                    modified[current_path] = (value1, value2)

    return added, removed, modified


def print_differences(file1, file2, added, removed, modified):
    print(f'Comparing {file1} vs {file2}')
    if added:
        print('Added:')
        for path, value in added.items():
            print(f'  {path}: {value}')
    if removed:
        print('Removed:')
        for path, value in removed.items():
            print(f'  {path}: {value}')
    if modified:
        print('Modified:')
        for path, (value1, value2) in modified.items():
            print(f'  {path}: {value1} -> {value2}')
    print()

def main():
    if len(sys.argv) != 4:
        print('Usage: python compare_yaml.py <file1> <file2> <file3>')
        sys.exit(1)

    file1, file2, file3 = sys.argv[1:4]
    
    data1 = load_yaml(file1)
    data2 = load_yaml(file2)
    data3 = load_yaml(file3)

    # Corrected unpacking
    for current_file, new_file, current_data, new_data in [(file1, file2, data1, data2), (file2, file3, data2, data3), (file1, file3, data1, data3)]:
        added, removed, modified = compare_dicts(current_data, new_data)
        print_differences(current_file, new_file, added, removed, modified)

if __name__ == '__main__':
    main()
