from tensorly.decomposition import tucker
from tensorly import tucker_to_tensor
import numpy as np
import subsetGen
import operator

PATH = "/home/yikang/Documents/dataset/ml-20m/"
STORED_PATH = PATH + "subset/"


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
    nnz = np.count_nonzero(x) / (ulen * ilen * tlen)
    print('NNZ of new dataset:' + str(nnz))
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


def evaluation(mx, mp_tag, mp_set, ulen, ilen, tlen):
    TOP = 10
    Precision = [0.0 for _ in range(TOP)]
    Recall = [0.0 for _ in range(TOP)]
    F1 = [0.0 for _ in range(TOP)]
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
            Precision[top - 1] += float(len(z) / top)
            Recall[top - 1] += float(len(z) / len(mp_set[user]))
        Precision[top - 1] /= ulen
        Recall[top - 1] /= ulen
        F1[top - 1] = 2 * Precision[top - 1] * Recall[top - 1] / (Precision[top - 1] + Recall[top - 1])
    print(Precision)
    print(F1)
    with open(STORED_PATH + 'precision.dat', 'a') as wf:
        wf.write(str(Precision[0]))
        for i in range(TOP):
            if i == 0:
                continue
            wf.write('\t' + str(Precision[i]))
        wf.write('\n')
    with open(STORED_PATH + 'f1.dat', 'a') as wf:
        wf.write(str(F1[0]))
        for i in range(TOP):
            if i == 0:
                continue
            wf.write('\t' + str(F1[i]))
        wf.write('\n')
    with open(STORED_PATH + 'recall.dat', 'a') as wf:
        wf.write(str(Recall[0]))
        for i in range(TOP):
            if i == 0:
                continue
            wf.write('\t' + str(Recall[i]))
        wf.write('\n')


def go(ulen, ilen, tlen):
    """
    make alsTucker from input file:'u_i_t_train.dat', make recommendation and evaluation
    :param ulen:
    :param ilen:
    :param tlen:
    :return:
    """
    x = init_tensor(ulen, ilen, tlen)
    core, factors = tucker(x, [int(ulen * 0.19), int(ilen * 0.2), int(tlen)])
    mx = tucker_to_tensor((core, factors))
    mp_tag, mp_set = init_test()
    evaluation(mx, mp_tag, mp_set, ulen, ilen, tlen)
