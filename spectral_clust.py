from sklearn.cluster import SpectralClustering

PATH = "/home/yikang/Documents/dataset/ml-20m/"
STORED_PATH = PATH + "subset/"
clusers = 7
mp = dict()

f = open(STORED_PATH + 'fin_sim.dat')
matrix = []
while True:
    line = f.readline()
    if not line:
        break
    cap = line.strip().split('\t')
    matrix.append(cap)
f.close()
sc = SpectralClustering(clusers, affinity='precomputed', n_init=50)
sc.fit(matrix)
labels = sc.labels_
print(labels)
for i in labels:
    if i not in mp:
        mp[i] = 0
    mp[i] += 1
for i in range(0, clusers):
    print(mp[i])
