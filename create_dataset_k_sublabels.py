# -*- coding: utf-8 -*
#
# создать датасет: на вход - k множеств диагнозов, на выход датасет вида [x, y1, …, yk]
import os
import json
from raw_dataset_to_pandas_frame import get_pandas_dataframe

def get_diagnosis_groups(diagnosis_hierarchy_json):
    filename = os.fsdecode(diagnosis_hierarchy_json)
    if os.path.isfile(filename):
        with open(filename) as json_file:
            json_dict = json.load(json_file)
            print(str(json_dict))

def generate_dataset(groups_of_diagnoses, folder_with_raw_dataset):
    folder_with_files = 'C:\\ecg'  # путь к папке с исходными файлами .edf, .json
    df = get_pandas_dataframe(folder_with_raw_dataset)
    dataset = {}



if __name__ == "__main__":
    path_to_summary = 'C:\\Users\\neuro\\Desktop\\diagnosis.json'
    groups = get_diagnosis_groups(path_to_summary)


