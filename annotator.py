#генеим маску разметку и сохраняем датасет ввиде: x, ann

import os
import json
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt

path_to_file = "./delineation.json"
folder_with_raw_dataset = 'C:\\ecg_new'

# Порядок отведений не менять!! он соответствует 1-12
leads = ['i', 'ii', 'iii', 'avr', 'avl', 'avf', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6']
for i in range(len(leads)):
    leads[i]= 'lead_'+ leads[i]

tables_ids = ['qrs', 't', 'p']

def generate_mask_for_ecg(data, raw_ecg_id, lead_id):
    pass

def draw_ecg_and_mask(ecg, mask, filename):
    pass

def print_data(data):
    print(data.keys())  # айдишники пациентов
    print(data['2731'].keys()) # айдишники отведений
    print(data['2731']['lead_v2'].keys()) #айдишники триплетов

def handle_data(data):
    cases = 0
    for file in os.listdir(folder_with_raw_dataset):
        filename = os.fsdecode(file)
        if filename.endswith(".edf"):
            case_id = filename[0:-len(".edf")]
            if case_id in data.keys():
                cases +=1
    print ("нашлись аннотации для " + str(cases) + " пациентов нашего датасета " + folder_with_raw_dataset)

with open(path_to_file, 'r') as f:
    data = json.load(f)
    handle_data(data)


