import pytest
import yaml
from compare import load_yaml, compare_dicts, compare_lists

# Sample data for testing
def sample_data(file_name):
    with open(f'tests/{file_name}', 'r') as file:
        return yaml.safe_load(file)

def test_compare_dicts():
    dict1 = sample_data('test_file1.yaml')
    dict2 = sample_data('test_file2.yaml')
    
    added, removed, modified = compare_dicts(dict1, dict2)
    
    assert added == {'containers[container3]': {'name': 'container3', 'image': 'image3'}}
    assert removed == {'containers[container2]': {'name': 'container2', 'image': 'image2'}}
    assert modified == {}

def test_compare_lists():
    list1 = sample_data('test_file1.yaml')['containers']
    list2 = sample_data('test_file2.yaml')['containers']
    
    added, removed, modified = compare_lists(list1, list2, 'containers')
    
    assert added == {'containers[container3]': {'name': 'container3', 'image': 'image3'}}
    assert removed == {'containers[container2]': {'name': 'container2', 'image': 'image2'}}
    assert modified == {}


def dicts_equal(d1, d2):
    if isinstance(d1, dict) and isinstance(d2, dict):
        if d1.keys() != d2.keys():
            return False
        return all(dicts_equal(d1[k], d2[k]) for k in d1)
    elif isinstance(d1, tuple) and isinstance(d2, tuple):
        if len(d1) != len(d2):
            return False
        return all(dicts_equal(a, b) for a, b in zip(d1, d2))
    else:
        return d1 == d2



def test_compare_dicts_modified():
    dict1 = sample_data('test_file1.yaml')
    dict2 = sample_data('test_file3.yaml')

    added, removed, modified = compare_dicts(dict1, dict2)
    
    assert added == {}
    assert removed == {'containers[container2]': {'name': 'container2', 'image': 'image2'}}
    assert dicts_equal(modified, {'containers[container1].image': ('image1', 'image1_updated')})
