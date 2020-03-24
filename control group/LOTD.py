import tensorDecom
import subsetGen
import dataset_split
import numpy as np

# low order tensor decomposition

PATH = "/home/yikang/Documents/dataset/ml-20m/"
STORED_PATH = PATH + "subset/"
TOP = 20
U_LEN = subsetGen.get_len(0)
I_LEN = subsetGen.get_len(1)
T_LEN = subsetGen.get_len(2)
LEN = [U_LEN, I_LEN, T_LEN]
iteration = 500
tolerance = 0.001
X = tensorDecom.init_tensor(U_LEN, I_LEN, T_LEN)
Y = [np.zeros([U_LEN, I_LEN, T_LEN]) for _ in range(iteration + 1)]
Omega = list()
with open(STORED_PATH + 'u_i_t_train.dat') as rf:
    while True:
        line = rf.readline()
        if not line:
            break
        cap = line.strip().split('\t')
        Omega.append([int(cap[0]) - 1, int(cap[1]) - 1, int(cap[2]) - 1])


def cal_u(index, tensor, u, v):
    result = u[index[0]][index[1]][index[2]]
    if result != -1.0:
        return result
    zero_cnt = 0
    for term in index:
        if term == 0:
            zero_cnt += 1
    if zero_cnt == 1:
        if index[0] == 0:
            result = tensor[:, index[1] - 1, index[2] - 1].sum()
        elif index[1] == 0:
            result = tensor[index[0] - 1, :, index[2] - 1].sum()
        else:
            result = tensor[index[0] - 1, index[1] - 1, :].sum()
    elif zero_cnt == 2:
        if index[0] != 0:
            result = tensor[index[0] - 1, :, :].sum()
        elif index[1] != 0:
            result = tensor[:, index[1] - 1, :].sum()
        else:
            result = tensor[:, :, index[2] - 1].sum()
    else:
        result = tensor.sum()
    u[index[0]][index[1]][index[2]] = result
    return result


def cal_v(index, tensor, u, v):
    result = v[index[0]][index[1]][index[2]]
    if result != -1.0:
        return result
    zero_cnt = 0
    for term in index:
        if term == 0:
            zero_cnt += 1
    if zero_cnt == 1:
        if index[0] == 0:
            result = cal_u(index, tensor, u, v) / LEN[0]
        elif index[1] == 0:
            result = cal_u(index, tensor, u, v) / LEN[1]
        else:
            result = cal_u(index, tensor, u, v) / LEN[2]
    elif zero_cnt == 2:
        if index[0] != 0:
            result = cal_u(index, tensor, u, v) / (LEN[1] * LEN[2])
        elif index[1] != 0:
            result = cal_u(index, tensor, u, v) / (LEN[0] * LEN[2])
        else:
            result = cal_u(index, tensor, u, v) / (LEN[0] * LEN[1])
    else:
        result = cal_u(index, tensor, u, v) / (LEN[0] * LEN[1] * LEN[2])
    v[index[0]][index[1]][index[2]] = result
    return result


def cal_y(index, tensor, u, v):
    result = cal_v([0, 0, 0], tensor, u, v)
    result -= cal_v([index[0], 0, 0], tensor, u, v)
    result -= cal_v([0, index[1], 0], tensor, u, v)
    result -= cal_v([0, 0, index[2]], tensor, u, v)
    result += cal_v([index[0], index[1], 0], tensor, u, v)
    result += cal_v([index[0], 0, index[2]], tensor, u, v)
    result += cal_v([0, index[1], index[2]], tensor, u, v)
    return result


def cal_tolerance(x, y):
    result = 0.0
    for index in Omega:
        tmp = x[index[0], index[1], index[2]] - y[index[0], index[1], index[2]]
        tmp = tmp ** 2
        result += tmp
    return result


Y[0] = X.copy()
for times in range(iteration):
    u = [[[-1.0 for i in range(T_LEN + 1)] for j in range(I_LEN + 1)] for k in range(U_LEN + 1)]
    v = [[[-1.0 for i in range(T_LEN + 1)] for j in range(I_LEN + 1)] for k in range(U_LEN + 1)]
    for i in range(U_LEN):
        for j in range(I_LEN):
            for k in range(T_LEN):
                Y[times + 1][i, j, k] = cal_y([i + 1, j + 1, k + 1], Y[times], u, v)
    if cal_tolerance(Y[times], Y[times + 1]) < tolerance:
        Y_FIN = Y[times + 1].copy()
        break
mp_tag, mp_set = tensorDecom.init_test()
dataset_split.go(STORED_PATH + 'u_i_t_fin.dat', STORED_PATH + 'u_i_t_test.dat', STORED_PATH + 'u_i_t_train.dat')
tensorDecom.evaluation(Y_FIN, mp_tag, mp_set, U_LEN, I_LEN, T_LEN)
