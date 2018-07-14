# для новой сземы обучения (генералиатор- дискриминатор)

# мы генерим датасет здоровых (т.е. электрооось = нормал и ристм нормосистолический)
# потом генерим датасет больных одной какой-то болезнью
# при этом внутри экземпляров одной болезни педсатвлены ОДНОВРЕМЕННЫЕ с ней болезни!
# поэтому внутри датасета больных болезнью посортируем больных по кол-ву одновременных болезней (сумма единиц

import os
from tabulate import tabulate
import pickle as pkl

from raw_dataset_to_pandas_frame import (
    get_pandas_dataframe, get_n_most_freq_names
)

from create_dataset_n_classes import (
    _get_signal_from_file
)

folder_with_raw_dataset = 'C:\\ecg'  # путь к папке с исходными файлами .edf, .json
folder_name = 'all_datasets_fish'

def _get_subframe_with_removed(nessesary_indicators, nessesary_zeros):
    df_selected = _get_subframe_with_ilnesses(nessesary_indicators, others_zeros=False)
    criteria = []
    for diagnos_name in nessesary_zeros:
        criteria.append(diagnos_name + ' == 0')

    str_query = ''
    for i in range(len(criteria)):
        str_query = str_query + criteria[i]
        if i < len(criteria) - 1:
            str_query = str_query + " & "
    df_selected = df_selected.query(str_query)
    return df_selected

def _get_subframe_with_ilnesses(list_of_diagnoses,  others_zeros):
    """

    :param list_of_diagnoses: это те диагнозы, на против которого у пациента должны быть нули
    :param pkl_name:
    :param others_zeros: если тру, то во всех остальных диагнозах должен быть ноль (т.е. он болен ТОЛЬКО этими диагнозами и больше никакими)
    :return:
    """
    # выделяем только такие х-ы, у которых одновременно единица в диагнозе во всех болезнях из списка

    df = get_pandas_dataframe(folder_with_raw_dataset)

    col_list = list(df)
    for name in list_of_diagnoses:
        col_list.remove(name)
    col_list.remove('edf_file')
    col_list.remove('case_id')
    df['diversity'] = df[col_list].sum(axis=1)

    criteria = []
    for diagnos_name in list_of_diagnoses:
        criteria.append(diagnos_name + ' == 1')

    str_query = ''
    for i in range(len(criteria)):
        str_query=str_query + criteria[i]
        if i < len(criteria) -1:
            str_query= str_query+ " & "
    df_selected = df.query(str_query)

    #print(col_list)
    if others_zeros:
        df_selected = df_selected.query('diversity == 0')

    #print(tabulate(df_selected, headers='keys', tablefmt='psql'))
    return df_selected

def get_ill_xy(nessesary_indicators, pkl_name, zero_indicators=None):
    if zero_indicators == None:
        df_selected = _get_subframe_with_ilnesses(nessesary_indicators, others_zeros=False)
    else:
        df_selected = _get_subframe_with_removed(nessesary_indicators, zero_indicators)
    df_selected = df_selected.sort_values(by=['diversity'], ascending=True) # первыми будут самые чистые
    x = []
    y = []
    errors = []
    for index, row in df_selected.iterrows():
        edf_file = row['edf_file']
        signal = _get_signal_from_file(edf_file)
        if signal is None:
            errors.append(edf_file)
            continue
        x.append(signal)
        y.append(row['diversity'])
    assert len(x) == len(y)
    print("нашлось больных этим + другим: " + str(len(x)))
    dict = {'x': x, 'div': y, 'summary': nessesary_indicators}
    outfile = open(pkl_name, 'wb')
    pkl.dump(dict, outfile)
    outfile.close()
    print("датасет сохранен в файл, количество записей = " + str(len(x)))
    if (len(errors) != 0):
        print("не удалось добавить в датасет файлы: " + str(errors))

def get_ill_x(nessesary_indicators, pkl_name):
    df_selected = _get_subframe_with_ilnesses(nessesary_indicators, others_zeros=True)
    x = []
    errors = []
    for index, row in df_selected.iterrows():
        edf_file = row['edf_file']
        signal = _get_signal_from_file(edf_file)
        if signal is None:
            errors.append(edf_file)
            continue
        x.append(signal)

    print("нашлось больных ТОЛЬКО этим: " + str(len(x)))
    dict = {'x': x, 'summary': nessesary_indicators}
    outfile = open(pkl_name, 'wb')
    pkl.dump(dict, outfile)
    outfile.close()
    print("датасет сохранен в файл")
    if (len(errors) != 0):
        print("не удалось добавить в датасет файлы: " + str(errors))

def make_2_dsets(nessesary_indicators, name):
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    pkl_name_only = os.path.join(folder_name, "ONLY_"+name)
    pkl_name_not_only = os.path.join(folder_name, name)
    get_ill_xy(nessesary_indicators,  pkl_name_not_only)
    get_ill_x(nessesary_indicators, pkl_name_only)

def make_n_dsets(one_group, second_group, name):
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    pkl_name_zn = os.path.join(folder_name, "ZN(both)_"+name)
    pkl_name_z_no_n = os.path.join(folder_name, "z_no_n_" + name)
    pkl_name_n_no_z = os.path.join(folder_name, "n_no_z_" + name)
    print("!!!---" +str(one_group) + "---NOT: "+ str(second_group))
    get_ill_xy(nessesary_indicators=one_group, zero_indicators=second_group, pkl_name=pkl_name_z_no_n)
    print("!!!---" + str(second_group) + "---NOT: " + str(one_group))
    get_ill_xy(nessesary_indicators=second_group, zero_indicators=one_group, pkl_name=pkl_name_n_no_z)
    print("!!!------BOTH: " + str(second_group+one_group))
    get_ill_xy(nessesary_indicators=second_group+one_group, zero_indicators=None, pkl_name=pkl_name_zn)


if __name__ == "__main__":
    name = 'healthy.pkl'


    nessesary_indicators1 = ['normal', 'regular_normosystole']
    nessesary_indicators2 = ['normal', 'regular_normosystole', 'left_ventricular_hypertrophy']
    nessesary_indicators3 = ['normal', 'regular_normosystole', 'extension_left_atrium']
    nessesary_indicators4 = ['extension_left_atrium', 'left_ventricular_hypertrophy'] #0

    #make_2_dsets(nessesary_indicators4, name)
    make_n_dsets(['extension_left_atrium'], ['left_ventricular_hypertrophy'], name)