from tensorly.decomposition import tucker
from tensorly import tucker_to_tensor
import numpy as np
import subsetGen
import operator

PATH = "/home/yikang/Documents/dataset/ml-20m/"
STORED_PATH = PATH + "subset/"


# U_LEN = subsetGen.get_len(0)
# I_LEN = subsetGen.get_len(1)
# T_LEN = 10
# TOP = 20


# x = np.zeros([U_LEN, I_LEN, T_LEN])
# with open(STORED_PATH + 'u_i_t_train.dat') as rf:
#     while True:
#         line = rf.readline()
#         if not line:
#             break
#         cap = line.strip().split('\t')
#         user = int(cap[0])
#         item = int(cap[1])
#         tag = int(cap[2])
#         x[user - 1, item - 1, tag - 1] = 1.0

# core, factors = tucker(x, [int(U_LEN * 0.19), int(I_LEN * 0.2), int(T_LEN)])
# mx = tucker_to_tensor((core, factors))
# read test data
# mp_tag = dict()  # user-tag
# mp_set = dict()  # user-item set
# evaluation
# Prec = list()
# Recall = list()
# F1 = list()
# for i in range(0, TOP):
#     Prec.append(0.0)
#     Recall.append(0.0)
#     F1.append(0.0)
# with open(STORED_PATH + 'u_i_t_test.dat') as rf:
#     while True:
#         line = rf.readline()
#         if not line:
#             break
#         cap = line.strip().split('\t')
#         user = int(cap[0]) - 1
#         item = int(cap[1]) - 1
#         tag = int(cap[2]) - 1
#         if user not in mp_tag:
#             mp_tag[user] = tag
#         if user not in mp_set:
#             mp_set[user] = set()
#         mp_set[user].add(item)

# for top in range(1, TOP + 1):
#     for user, tag in mp_tag.items():
#         u_t_list = mx[user, :, tag].tolist()
#         tmp_list = list()  # [[value, index],...]
#         cnt = 0
#         for i in u_t_list:
#             tmp_list.append([i, cnt])
#             cnt += 1
#         sorted_list = sorted(tmp_list, key=operator.itemgetter(0), reverse=True)
#         tmp_set = set()
#         for i in range(0, top):
#             tmp_set.add(sorted_list[i][1])
#         z = tmp_set.intersection(mp_set[user])
#         Prec[top - 1] += float(len(z) / top)
#         Recall[top - 1] += float(len(z) / len(mp_set[user]))
#     Prec[top - 1] /= U_LEN
#     Recall[top - 1] /= U_LEN
#     F1[top - 1] = 2 * Prec[top - 1] * Recall[top - 1] / (Prec[top - 1] + Recall[top - 1])
# print(F1)


def init_tensor(ulen, ilen, tlen):
    """

    :param ulen: length of users
    :param ilen: length of items
    :param tlen: length of tags
    :return: ndarray
    """
    x = np.zeros([ulen, ilen, tlen])
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
    return x


def init_test():
    """
    read test data
    :return:
    """
    mp_tag = dict()  # user-tag
    mp_set = dict()  # user-item set
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
    return mp_tag, mp_set


def go(ulen, ilen, tlen):
    """
    make alsTucker from input file:'u_i_t_train.dat', make recommendation and evaluation
    :param ulen:
    :param ilen:
    :param tlen:
    :return:
    """
    Prec = list()
    Recall = list()
    F1 = list()
    TOP = 20
    for i in range(0, TOP):
        Prec.append(0.0)
        Recall.append(0.0)
        F1.append(0.0)
    x = init_tensor(ulen, ilen, tlen)
    core, factors = tucker(x, [int(ulen * 0.19), int(ilen * 0.2), int(tlen)])
    mx = tucker_to_tensor((core, factors))
    mp_tag, mp_set = init_test()
    for top in range(1, TOP + 1):
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
        Prec[top - 1] /= ulen
        Recall[top - 1] /= ulen
        F1[top - 1] = 2 * Prec[top - 1] * Recall[top - 1] / (Prec[top - 1] + Recall[top - 1])
    print(Prec)
    print(F1)
