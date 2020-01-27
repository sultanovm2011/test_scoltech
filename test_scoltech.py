import numpy as np
import pandas as pd
import argparse

# Набор переменных
parser = argparse.ArgumentParser()
parser.add_argument("file_to_read", type=str, help="Вы должны ввести название входного файла с данными, выходного файла для записи и параметры M, N и dt.")
parser.add_argument("file_to_write", type=str, help="Вы должны ввести название входного файла с данными, выходного файла для записи и параметры M, N и dt.")
parser.add_argument("M", type=int, help="Вы должны ввести название входного файла с данными, выходного файла для записи и параметры M, N и dt.")
parser.add_argument("N", type=int, help="Вы должны ввести название входного файла с данными, выходного файла для записи и параметры M, N и dt.")
parser.add_argument("dt", type=float, help="Вы должны ввести название входного файла с данными, выходного файла для записи и параметры M, N и dt.")
args = parser.parse_args()

pd.options.mode.chained_assignment = None
M = args.M
N = args.N
dT = args.dt
FILE_TOREAD = args.file_to_read
FILE_TO_WRITE = args.file_to_write
# Функция подсчета нужных инцидентов
def count_inc(M, N, dT, FILE_TOREAD, FILE_TO_WRITE):
    df_incidents = pd.read_csv(FILE_TOREAD,
            dtype ={'id':'uint32','feature1':'uint8','feature2':'uint8','time':'float16'})
    res = [0 for i in range(N)]
    c = 0
    for i in range(M):
    # Отбор по признакам feature1, feature2
        df_incidents_i = df_incidents[(df_incidents.feature1 == i)]
        for j in range(M):
            df_incidents_j = df_incidents_i[(df_incidents_i.feature2 == j)]
            df_incidents_j['id'] = df_incidents_j.index
            df_incidents_j_time = df_incidents_j[['time','id']]
            df_incidents_j_time = df_incidents_j_time.sort_values('time', ascending=True)

    # Отбор по признакам time
            numpyMatrix = df_incidents_j_time.values
            n = numpyMatrix.shape
            for idx in range(n[0]-1):
                kk =  numpyMatrix[idx+1, 0]
                jdx = idx
                while jdx >= 0:
                    jj = numpyMatrix[jdx, 0]
                    if 0 < (kk-dT) < jj  :
                        c += 1
                    else: break
                    jdx -= 1
                if c > 0:
                    res[int(numpyMatrix[idx+1, 1])] = c
                c = 0

    df_res = pd.DataFrame(res)
    df_res.columns = ['count']
# Запись в файл
    df_res.to_csv(FILE_TO_WRITE, index_label='id', header = True)

count_inc(M, N, dT, FILE_TOREAD, FILE_TO_WRITE)
