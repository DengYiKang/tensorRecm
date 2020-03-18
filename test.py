import orin_format
import subsetGen

# procedure:
# u-i-t=>t-f
# t-f=>n of t-f
# t-f,t-v=>filtered t-f,t-v
# t-f,u-i-t=>u-i-t
# u-i-t=>u-f
# u-f=>n of u-f
# u-f,u-i-t=>u-i-t
# u-i-t=>i-f
# i-f=>n of i-f
# i-f,u-i-f=>u-i-f
# u-i-f,t-f,t-v=>t-f,t-v
# map
# statistic
PATH = "/home/yikang/Documents/dataset/ml-20m/"
STORED_PATH = PATH + "subset/"
# [u-f,i-f,t-f],default [-1,-1,-1]
LEN_FILE = "len.txt"
USER_ITEM_TAG_PATH = STORED_PATH + 'user_item_tag_format.dat'
TAG_VALUE_PATH = STORED_PATH + 'tags_format.dat'

subsetGen.init()
orin_format.go()
subsetGen.count_f_ge_minf(USER_ITEM_TAG_PATH, STORED_PATH + 't_f_1.dat', 2, 50)
subsetGen.select_top(STORED_PATH + 't_f_1.dat', STORED_PATH + 't_f_2.dat', 2, 500)
subsetGen.select_triple_by_tuple(USER_ITEM_TAG_PATH, STORED_PATH + 't_f_2.dat', STORED_PATH + 'u_i_t_1.dat', 2)
subsetGen.count_f_ge_minf(STORED_PATH + 'u_i_t_1.dat', STORED_PATH + 'u_f_1.dat', 0, 10)
subsetGen.select_top(STORED_PATH + 'u_f_1.dat', STORED_PATH + 'u_f_2.dat', 0, 100)
subsetGen.select_triple_by_tuple(STORED_PATH + 'u_i_t_1.dat', STORED_PATH + 'u_f_2.dat', STORED_PATH + 'u_i_t_2.dat', 0)
subsetGen.count_f_ge_minf(STORED_PATH + 'u_i_t_2.dat', STORED_PATH + 'i_f_1.dat', 1, 10)
subsetGen.select_top(STORED_PATH + 'i_f_1.dat', STORED_PATH + 'i_f_2.dat', 1, 100)
subsetGen.select_triple_by_tuple(STORED_PATH + 'u_i_t_2.dat', STORED_PATH + 'i_f_2.dat', STORED_PATH + 'u_i_t_3.dat', 1)
subsetGen.select_tuple_by_triple(STORED_PATH + 't_f_2.dat', STORED_PATH + 'u_i_t_3.dat', STORED_PATH + 't_f_3.dat')
subsetGen.select_tuple_by_tuple(STORED_PATH + 't_f_3.dat', TAG_VALUE_PATH, STORED_PATH + 't_v.dat')
subsetGen.map_triple(STORED_PATH + 'u_i_t_3.dat', STORED_PATH + 'u_i_t_fin.dat', STORED_PATH + 'tag_map.dat')
subsetGen.map_tag(STORED_PATH + 'tag_map.dat', STORED_PATH + 't_v.dat', STORED_PATH + 't_v_2.dat')
subsetGen.sort_tuple(STORED_PATH+'t_v_2.dat', STORED_PATH+'t_v_fin.dat', 0)
subsetGen.statistic(STORED_PATH+'u_i_t_fin.dat', STORED_PATH+'statistic.dat')