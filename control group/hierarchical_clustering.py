from sklearn.cluster import AgglomerativeClustering
import subsetGen
import dataset_split
import tensorDecom

PATH = "/home/yikang/Documents/dataset/hetrec2011-lastfm-2k/"
STORED_PATH = PATH + "subset/"
clusers = 10
mp = dict()

with open(STORED_PATH + 'tfSim.dat') as rf:
    matrix = []
    while True:
        line = rf.readline()
        if not line:
            break
        cap = line.strip().split('\t')
        matrix.append(cap)
sc = AgglomerativeClustering(clusers, affinity='precomputed', linkage='average')
sc.fit(matrix)
labels = sc.labels_
print(labels)
with open(STORED_PATH + 'clusters_map.dat', 'w') as wf1:
    with open(STORED_PATH + 'clusters_statistic.dat', 'w') as wf2:
        not_first = False
        cnt = 0
        for term in labels:
            cnt += 1
            wf1.write(str(cnt) + '\t')
            wf1.write(str(term + 1) + '\n')
        for i in labels:
            if i not in mp:
                mp[i] = 0
            mp[i] += 1
        for i in range(0, clusers):
            print(str(mp[i]) + '\n')
            wf2.write(str(mp[i]) + '\n')
subsetGen.map_triple_by_tuple(STORED_PATH + 'clusters_map.dat', STORED_PATH + 'u_i_t_fin.dat',
                              STORED_PATH + 'u_i_t_clustered.dat', 2)
dataset_split.go(STORED_PATH + 'u_i_t_clustered.dat', STORED_PATH + 'u_i_t_test.dat', STORED_PATH + 'u_i_t_train.dat')
tensorDecom.go(subsetGen.get_len(0), subsetGen.get_len(1), clusers)
