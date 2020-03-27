import numpy as np
import matplotlib.pyplot as plt

PATH = "/home/yikang/Documents/dataset/ml-20m/"
STORED_PATH = PATH + "subset/"
TOP = 10
mx = [i + 1 for i in range(TOP)]
x = np.asarray(mx)
y = [np.zeros([1, TOP]) for _ in range(4)]

with open(STORED_PATH + 'precision.dat') as rf:
    line_cnt = 0
    while True:
        line = rf.readline()
        if not line:
            break
        cap = line.strip().split('\t')
        tmp = np.asarray(cap, dtype=np.float64)
        y[line_cnt] = np.around(tmp, decimals=2)
        print(y[line_cnt])
        line_cnt += 1
# plt.plot([1, 2, 3], [3, 5, 9])
plt.plot(x, y[3], 'ro', label='only_alsTucker')
plt.plot(x, y[3], 'r')
plt.plot(x, y[2], 'bs', label='hierarchical_clst')
plt.plot(x, y[2], 'b')
plt.plot(x, y[1], 'y^', label='LOTD')
plt.plot(x, y[1], 'y')
plt.plot(x, y[0], 'gd', label='clustHOSVD')
plt.plot(x, y[0], 'g')
plt.legend()
plt.xlabel('Top')
plt.ylabel('Precision')
plt.title('ml-20m')
# plt.savefig(STORED_PATH + "precision_compared.png")
