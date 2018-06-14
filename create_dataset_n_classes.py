# -*- coding: utf-8 -*
#
# создать датасет: на вход - n диагнозов, на выход датасет вида [x, y] где len(y[i]) = n
import os

from raw_dataset_to_pandas_frame import get_pandas_dataframe


def generate_dataset(list_of_diagnoses, folder_with_raw_dataset, name_pkl):
    df = get_pandas_dataframe(folder_with_raw_dataset)
    selection = df[list_of_diagnoses]





if __name__ == "__main__":
    folder_with_raw_dataset = 'C:\\ecg'  # путь к папке с исходными файлами .edf, .json
    list_of_diagnoses = ["regular_normosystole", "sinus_tachycardia", "sinus_bradycardia", "sinus_arrhythmia"]
    name_for_dataset_file = 'SINUS_RYTHM.pkl'
    generate_dataset(list_of_diagnoses, folder_with_raw_dataset, name_for_dataset_file)



