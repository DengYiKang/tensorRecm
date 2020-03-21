import random

PATH = "/home/yikang/Documents/dataset/ml-20m/"
STORED_PATH = PATH + "subset/"
mp = dict()
test_line = set()
with open(STORED_PATH + 'u_i_t_clustered.dat') as rf:
    lineCnt = 0
    while True:
        line = rf.readline()
        if not line:
            break
        lineCnt += 1
        cap = line.strip().split('\t')
        user = int(cap[0])
        item = int(cap[1])
        tag = int(cap[2])
        if user not in mp:
            mp[user] = dict()
        if tag not in mp[user]:
            mp[user][tag] = list()
        mp[user][tag].append(lineCnt)
for key, value in mp.items():
    index = random.randint(0, len(value) - 1)
    for v in value.values():
        if index == 0:
            test_line.update(v)
            break
        index -= 1
with open(STORED_PATH + 'u_i_t_test.dat', 'w') as wf1:
    with open(STORED_PATH + 'u_i_t_train.dat', 'w') as wf2:
        with open(STORED_PATH + 'u_i_t_clustered.dat') as rf:
            lineCnt = 0
            while True:
                line = rf.readline()
                if not line:
                    break
                lineCnt += 1
                if lineCnt in test_line:
                    wf1.write(line)
                else:
                    wf2.write(line)
