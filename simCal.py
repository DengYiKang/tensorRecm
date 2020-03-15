from nltk.corpus import wordnet as wn
import numpy as np
import math

PATH = "/home/yikang/Documents/dataset/ml-20m/"
STORED_PATH = PATH + "subset/"
LEN_PATH = STORED_PATH + 'len.txt'


# a = wn.synsets('dog')[0]
# b = wn.synsets('cat')[0]
# print(a.wup_similarity(b))


def matrix_output(matrix_in, file_out):
    f = open(file_out, 'w')
    for i in range(0, T_LEN):
        for j in range(0, T_LEN):
            if j != 0:
                f.write('\t')
            f.write(str(matrix_in[i, j]))
        f.write('\n')
    f.close()


def find_sim(a, b):
    for i in a:
        for j in b:
            result = str(i.wup_similarity(j))
            if result is None:
                continue
            else:
                return result
    return '0'


# cosine similarity
triple = np.loadtxt(STORED_PATH + 'u_i_t_fin.dat')
with open(LEN_PATH) as rf:
    cap = rf.readline().strip().split('\t')
    U_LEN = int(cap[0])
    I_LEN = int(cap[1])
    T_LEN = int(cap[2])
orin_tensor = np.zeros([U_LEN, I_LEN, T_LEN])
for tmp in triple:
    u = int(tmp[0])
    i = int(tmp[1])
    t = int(tmp[2])
    orin_tensor[u - 1, i - 1, t - 1] = 1
cosim_matrix = np.zeros([T_LEN, T_LEN])
for i in range(0, T_LEN):
    for j in range(0, T_LEN):
        x = (orin_tensor[:, :, i] * orin_tensor[:, :, j]).sum()
        y = math.sqrt((orin_tensor[:, :, i] ** 2).sum()) * math.sqrt((orin_tensor[:, :, j] ** 2).sum())
        cosim_matrix[i, j] = float(x / y)
matrix_output(cosim_matrix, STORED_PATH + 'cosim.dat')

# semantic similarity
wupsim_matrix = np.zeros([T_LEN, T_LEN])
mp = dict()
with open(STORED_PATH + 't_v_fin.dat') as rf:
    while True:
        line = rf.readline()
        if not line:
            break
        cap = line.strip().split('\t')
        mp[int(cap[0]) - 1] = cap[1]
for i in range(0, T_LEN):
    for j in range(0, T_LEN):
        if i == j:
            wupsim_matrix[i, j] = 1
            continue
        if i > j: continue
        try:
            a = wn.synsets(mp[i])
            b = wn.synsets(mp[j])
            wupsim_matrix[i, j] = float(find_sim(a, b))
        except:
            wupsim_matrix[i, j] = 0
for i in range(0, T_LEN):
    for j in range(0, T_LEN):
        if i > j:
            wupsim_matrix[i, j] = wupsim_matrix[j, i]
        else:
            break
matrix_output(wupsim_matrix, STORED_PATH + 'wupsim.dat')

# final similarity
fin_sim = (cosim_matrix * 0.5 + wupsim_matrix * 0.5).copy()
matrix_output(fin_sim, STORED_PATH + 'fin_sim.dat')
