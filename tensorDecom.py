from tensorly.decomposition import tucker
from tensorly import tucker_to_tensor
import numpy as np
import subsetGen
import operator

PATH = "/home/yikang/Documents/dataset/ml-20m/"
STORED_PATH = PATH + "subset/"
U_LEN = subsetGen.get_len(0)
I_LEN = subsetGen.get_len(1)
T_LEN = 7
x = np.zeros([U_LEN, I_LEN, T_LEN])
with open(STORED_PATH + 'u_i_t_clustered.dat') as rf:
    while True:
        line = rf.readline()
        if not line:
            break
        cap = line.strip().split('\t')
        user = int(cap[0])
        item = int(cap[1])
        tag = int(cap[2])
        x[user - 1, item - 1, tag - 1] = 1.0

core, factors = tucker(x, [U_LEN / 2, I_LEN / 2, T_LEN])
mx = tucker_to_tensor((core, factors))
print("reconstructed tensor:\n%s" % str(mx))
# read test data
mp_item = dict()  # user-item
mp_set = dict()  # user-tag set
# evaluation
Prec = list()
Recall = list()
for i in range(0, 10):
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
        if user not in mp_item:
            mp_item[user] = item
        if user not in mp_set:
            mp_set[user] = set()
        mp_set[user].add(tag)

for top in range(1, 11):
    for user, item in mp_item.items():
        u_i_list = mx[user, item, :].tolist()
        tmp_list = list()  # [[value, index],...]
        cnt = 0
        for i in u_i_list:
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
