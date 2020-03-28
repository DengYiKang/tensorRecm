import numpy as np
import subsetGen
import math

PATH = "/home/yikang/Documents/dataset/hetrec2011-lastfm-2k/"
STORED_PATH = PATH + "subset/"
LEN_PATH = STORED_PATH + 'len.txt'


def matrix_output(matrix_in, file_out, tlen):
    f = open(file_out, 'w')
    for i in range(0, tlen):
        for j in range(0, tlen):
            if j != 0:
                f.write('\t')
            f.write(str(matrix_in[i, j]))
        f.write('\n')
    f.close()


triple = np.loadtxt(STORED_PATH + 'u_i_t_fin.dat')
U_LEN = subsetGen.get_len(0)
I_LEN = subsetGen.get_len(1)
T_LEN = subsetGen.get_len(2)
A = [np.zeros(I_LEN) for _ in range(T_LEN)]
tfSim = np.zeros([T_LEN, T_LEN])
tot_cnt = 0
for tmp in triple:
    user = int(tmp[0]) - 1
    item = int(tmp[1]) - 1
    tag = int(tmp[2]) - 1
    A[tag][item] += 1
    tot_cnt += 1
for term in A:
    term /= tot_cnt
for i in range(T_LEN):
    for j in range(T_LEN):
        if i > j:
            tfSim[i, j] = (A[i] * A[j]).sum()
            tfSim[i, j] /= math.sqrt((A[i] ** 2).sum()) * math.sqrt((A[j] ** 2).sum())
        if i == j:
            tfSim[i, j] = 1.0
for i in range(T_LEN):
    for j in range(T_LEN):
        if i < j:
            tfSim[i, j] = tfSim[j, i]
tfSim = 1 - tfSim
matrix_output(tfSim, STORED_PATH + 'tfSim.dat', T_LEN)
