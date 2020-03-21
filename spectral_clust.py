from sklearn.cluster import SpectralClustering
import subsetGen
import dataset_split
import tensorDecom

PATH = "/home/yikang/Documents/dataset/ml-20m/"
STORED_PATH = PATH + "subset/"
clusers = 10
mp = dict()

f1 = open(STORED_PATH + 'fin_sim.dat')
f2 = open(STORED_PATH + 'clusters_map.dat', 'w')
f3 = open(STORED_PATH + 'clusters_statistic.dat', 'w')
matrix = []
while True:
    line = f1.readline()
    if not line:
        break
    cap = line.strip().split('\t')
    matrix.append(cap)
sc = SpectralClustering(clusers, affinity='precomputed', n_init=50)
sc.fit(matrix)
labels = sc.labels_
not_first = False
cnt = 0
for term in labels:
    cnt += 1
    f2.write(str(cnt) + '\t')
    f2.write(str(term + 1) + '\n')
for i in labels:
    if i not in mp:
        mp[i] = 0
    mp[i] += 1
for i in range(0, clusers):
    f3.write(str(mp[i]) + '\n')
f3.close()
f2.close()
f1.close()
subsetGen.map_triple_by_tuple(STORED_PATH + 'clusters_map.dat', STORED_PATH + 'u_i_t_fin.dat',
                              STORED_PATH + 'u_i_t_clustered.dat', 2)
dataset_split.go(STORED_PATH + 'u_i_t_clustered.dat', STORED_PATH + 'u_i_t_test.dat', STORED_PATH + 'u_i_t_train.dat')
tensorDecom.go(subsetGen.get_len(0), subsetGen.get_len(1), clusers)
