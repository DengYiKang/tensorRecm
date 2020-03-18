from tensorly.decomposition import tucker
from tensorly import tucker_to_tensor
import numpy as np
import subsetGen

PATH = "/home/yikang/Documents/dataset/ml-20m/"
STORED_PATH = PATH + "subset/"
U_LEN = subsetGen.get_len(0)
I_LEN = subsetGen.get_len(1)
T_LEN = 7
# x = np.random.random([3, 3])
# core, factors = tucker(x, [1, 1])
# mx = tucker_to_tensor((core, factors))
# print("orin_tensor:\n%s" % str(x))
# print("reconstructed tensor:\n%s" % str(mx))
# print("core:\n%s" % str(core))
# print("factors:\n%s" % str(factors))
x = np.zeros([U_LEN, I_LEN, T_LEN])
f1 = open(STORED_PATH + 'u_i_t_clustered.dat')
while True:
    line = f1.readline()
    if not line:
        break
    cap = line.strip().split('\t')
    user = int(cap[0])
    item = int(cap[1])
    tag = int(cap[2])
    x[user - 1, item - 1, tag - 1] = 1.0
f1.close()
core, factors = tucker(x)
mx = tucker_to_tensor((core, factors))
print("orin_tensor:\n%s" % str(x))
print("reconstructed tensor:\n%s" % str(mx))
print("core:\n%s" % str(core))
print("factors:\n%s" % str(factors))
print(core.shape)
