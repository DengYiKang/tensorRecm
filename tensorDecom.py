from tensorly.decomposition import tucker
from tensorly import tucker_to_tensor
import numpy as np
import subsetGen
import operator

PATH = "/home/yikang/Documents/dataset/ml-20m/"
STORED_PATH = PATH + "subset/"
U_LEN = subsetGen.get_len(0)
I_LEN = subsetGen.get_len(1)
T_LEN = 10
x = np.zeros([U_LEN, I_LEN, T_LEN])
with open(STORED_PATH + 'u_i_t_train.dat') as rf:
    while True:
        line = rf.readline()
        if not line:
            break
        cap = line.strip().split('\t')
        user = int(cap[0])
        item = int(cap[1])
        tag = int(cap[2])
        x[user - 1, item - 1, tag - 1] = 1.0

core, factors = tucker(x, [int(U_LEN * 0.19), int(I_LEN * 0.2), int(T_LEN)])
mx = tucker_to_tensor((core, factors))
# read test data
mp_tag = dict()  # user-tag
mp_set = dict()  # user-item set
# evaluation
Prec = list()
Recall = list()
for i in range(0, T_LEN):
    Prec.append(0.0)
    Recall.append(0.0)
with open(STORED_PATH + 'u_i_t_test.dat') as rf:
    while True:
        line = rf.readline()
        if not line:
            break
        cap = line.strip().split('\t')
        user = int(cap[0]) - 1
        item = int(cap[1]) - 1
        tag = int(cap[2]) - 1
        if user not in mp_tag:
            mp_tag[user] = tag
        if user not in mp_set:
            mp_set[user] = set()
        mp_set[user].add(item)

for top in range(1, T_LEN + 1):
    for user, tag in mp_tag.items():
        u_t_list = mx[user, :, tag].tolist()
        tmp_list = list()  # [[value, index],...]
        cnt = 0
        for i in u_t_list:
            tmp_list.append([i, cnt])
            cnt += 1
        sorted_list = sorted(tmp_list, key=operator.itemgetter(0), reverse=True)
        tmp_set = set()
        for i in range(0, top):
            tmp_set.add(sorted_list[i][1])
        z = tmp_set.intersection(mp_set[user])
        Prec[top - 1] += float(len(z) / top)
        Recall[top - 1] += float(len(z) / len(mp_set[user]))
    Prec[top - 1] /= U_LEN
    Recall[top - 1] /= U_LEN
print(Prec)
print(Recall)
