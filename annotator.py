#генеим маску разметку и сохраняем датасет ввиде: x, ann

import os
import json
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import pyedflib
import numpy as np

path_to_file = "./delineation.json"
folder_with_raw_dataset = 'C:\\ecg_new'

# Порядок отведений не менять!! он соответствует 1-12
leads = ['i', 'ii', 'iii', 'avr', 'avl', 'avf', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6']
for i in range(len(leads)):
    leads[i]= 'lead_'+ leads[i]

tables_names = ['qrs', 't', 'p']
MAX=5000

def generate_mask_for_ecg_lead_by_one_table(data, raw_ecg_id, lead_name, table_name):
    mask =[0]*MAX #забиваем сначала маску нулями
    qrs_table = data[raw_ecg_id][lead_name][table_name]
    for triplet in qrs_table:
        start = triplet[0]
        end = triplet[2]
        for i in range(start, end,1):
            mask[i] = 1
    return mask

def zero_to_nan(values):
    """Replace every 0 with 'nan' and return a copy."""
    return [float('nan') if x==0 else x for x in values]

def draw_masks_for_ecg_lead(masks, masks_names, ecg_case, lead_name):
    signal = get_ecg_by_lead_name(ecg_case, lead_name)
    if signal is None:
        return
    figname = ecg_case+"_"+lead_name+".png"
    plt.plot(signal)

    for mask in masks:
        mask_with_nons = zero_to_nan(mask)# не будем рисовать зануленную часть маски
        plt.plot(mask_with_nons)

    plt.title('mask visualisation')
    plt.ylabel('masks and ecg')
    plt.xlabel('time')
    plt.legend(['signal']+masks_names, loc='upper left')
    plt.savefig(figname)


def get_ecg_by_lead_name(ecg_case, lead_name):
    filename_edf = os.path.join(folder_with_raw_dataset, ecg_case + ".edf")
    channel_index = leads.index(lead_name)
    try:
        f = pyedflib.EdfReader(filename_edf)
        n = f.signals_in_file
        assert n >= channel_index
        signal = f.readSignal(channel_index)
        f._close()
        del f
        return signal
    except Exception as  exeption:
        print("какая-то фигня с файлом кардиограммы " + filename_edf)
        return None

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

def generate_masks_for_ecg_lead(data, ecg_case, lead_name):
    masks = []
    for table_name in tables_names:
        mask = generate_mask_for_ecg_lead_by_one_table(data,
                                                   raw_ecg_id=ecg_case,
                                                   lead_name=lead_name,
                                                   table_name=table_name)
        masks.append(mask)
    return masks, tables_names

def test(data):
    i = 0
    lead_name = leads[0]
    for ecg_case in data.keys():
        i+=1
        masks, masks_names = generate_masks_for_ecg_lead(data, ecg_case, lead_name)
        draw_masks_for_ecg_lead(masks=masks,
                            masks_names=masks_names,
                            ecg_case=ecg_case,
                            lead_name=lead_name)
        plt.clf()
        if i>5:
            break

with open(path_to_file, 'r') as f:
    data = json.load(f)
    #handle_data(data)
    test(data)


