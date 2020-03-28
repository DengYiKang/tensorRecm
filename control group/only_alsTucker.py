from tensorly.decomposition import tucker
from tensorly import tucker_to_tensor
import numpy as np
import subsetGen
import dataset_split
import tensorDecom

# only use alsTucker

PATH = "/home/yikang/Documents/dataset/hetrec2011-lastfm-2k/"
STORED_PATH = PATH + "subset/"
dataset_split.go(STORED_PATH + 'u_i_t_fin.dat', STORED_PATH + 'u_i_t_test.dat', STORED_PATH + 'u_i_t_train.dat')
tensorDecom.go(subsetGen.get_len(0), subsetGen.get_len(1), subsetGen.get_len(2))
