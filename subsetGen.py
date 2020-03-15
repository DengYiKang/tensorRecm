import re
import random
import linecache
import operator

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


def init():
    with open(STORED_PATH + LEN_FILE, 'w') as wf:
        wf.write(str(-1) + '\t' + str(-1) + '\t' + str(-1) + '\t' + str(-1) + '\n')


def get_len(which):
    """
    get the len in LEN_FILE
    :param which: user-0, item-1, tag-2, the len of triples-3
    :return: integer. the len of which
    """
    value = 0
    with open(STORED_PATH + LEN_FILE) as rf:
        value = int(rf.readline().strip().split('\t')[which])
    return value


def update_len(which, value):
    """
    update the file len.txt which stores the length of files like u-f, i-f, t-f...
    :param which: user-0, item-1, tag-2, triple-3
    :param value: new value
    :return:
    """
    tmp = list()
    with open(STORED_PATH + LEN_FILE) as rf:
        tmp = rf.readline().strip().split('\t')
    tmp[which] = str(value)
    with open(STORED_PATH + LEN_FILE, 'w') as wf:
        wf.write(str(tmp[0]) + '\t' + str(tmp[1]) + '\t' + str(tmp[2]) + '\t' + str(tmp[3]) + '\n')


def count_f_ge_minf(file_in, file_out, which, min_f):
    """
    count the frequency of "which" in file file_in, and output the id whose frequency > min_f and sorted by frequency
    :param file_in: triples
    :param file_out:
    :param which:integer value:'user'-0;'item'-1;'tag'-2
    :param min_f:
    :return:
    """
    m = dict()
    count = 0
    with open(file_in) as rf:
        while True:
            line = rf.readline()
            if not line:
                break
            data = line.strip().split('\t')
            if which >= len(data):
                continue
            key = data[which]
            if key in m:
                m[key] += 1
            else:
                m[key] = 1
    sorted_m = sorted(m.items(), key=operator.itemgetter(1), reverse=True)
    with open(file_out, 'w') as wf:
        for x, y in sorted_m:
            if int(y) < min_f: break
            wf.write(str(x) + '\t' + str(y) + '\n')
            count += 1
            if count == 154:
                xxx = 1 + 2
    update_len(which, count)
    print(file_out + ' has generated')


def select_top(file_in, file_out, which, n):
    """
    select top n ordered by frequency
    :param file_in: format with x-f
    :param file_out: format with x-f
    :param which: user-0;item-1;tag-2
    :param n:
    :return:
    """
    len = get_len(which)
    if n > len:
        n = len
    f1 = open(file_in)
    f2 = open(file_out, 'w')
    cnt = n
    while cnt != 0:
        line = f1.readline()
        cap = line.strip().split('\t')
        x = str(cap[0])
        frequency = str(cap[1])
        f2.write(x + '\t' + frequency + '\n')
        cnt -= 1
    f2.close()
    f1.close()
    update_len(which, n)
    print(file_out + ' has generated')


def select_random(file_in, file_out, which, n):
    """
    select n tuples randomly, and update len.txt
    :param file_in: format is ?-frequency
    :param file_out: format is ?-frequency
    :param which: user-0;item-1;tag-2
    :param n:
    :return:
    """
    len = get_len(which)
    if n > len:
        n = len
    visited = set()
    # with open(STORED_PATH + LEN_FILE) as rf:
    #     tmp = rf.readline().strip().split('\t')
    #     len = int(tmp[which])
    with open(file_out, 'w') as wf:
        times = 0
        while times < n:
            row = random.randint(1, len)
            if row in visited:
                continue
            else:
                visited.add(row)
            tmp_list = linecache.getline(file_in, row).strip().split('\t')
            wf.write(str(tmp_list[0]) + '\t' + str(tmp_list[1]) + '\n')
            times += 1
    update_len(which, n)
    print(file_out + ' has generated')


def tag_filter(t_f_path, t_v_path, t_f_out, t_v_out):
    """
    drop the illegal tags whose value is not a single word
    :param t_f_path: tag-frequency file
    :param t_v_path: tagId-value file
    :param t_f_out: output file that stored t-f
    :param t_v_out: output file that stored t-v
    :return:
    """
    pattern = re.compile(r'[^?!@#$%\^&*()\+\/\[\] ]+$')
    f1 = open(t_f_path)
    f2 = open(t_v_path)
    f3 = open(t_f_out, 'w')
    f4 = open(t_v_out, 'w')
    cnt = 0
    while True:
        line = f1.readline()
        if not line:
            break
        cap = line.strip().split('\t')
        tag_id = str(cap[0])
        frequency = str(cap[1])
        f2.seek(0)
        while True:
            row = f2.readline()
            if not row:
                break
            m_cap = row.strip().split('\t')
            m_tagid = str(m_cap[0])
            m_value = str(m_cap[1])
            if tag_id == m_tagid:
                if pattern.match(str(m_value)):
                    f3.write(tag_id + '\t' + frequency + '\n')
                    f4.write(m_tagid + '\t' + m_value + '\n')
                    cnt += 1
                    break
                else:
                    break
            else:
                continue
    f4.close()
    f3.close()
    f2.close()
    f1.close()
    update_len(2, cnt)
    print(t_f_out + ', ' + t_v_out + 'has generated')


def select_triple_by_tuple(triple_in, tuple_in, triple_out, which):
    """
    select triples by x-f relations in file x_f_version
    :param triple_in: stores triples
    :param tuple_in: stores tuples like t-f
    :param triple_out: output extracted triples
    :param which: user-0,item-1,tag-2
    :return:
    """
    f1 = open(triple_in)
    f2 = open(tuple_in)
    f3 = open(triple_out, 'w')
    triple_cnt = 0
    while True:
        line = f2.readline()
        if not line:
            break
        cap = line.strip().split('\t')
        x_id = str(cap[0])
        f1.seek(0)
        while True:
            row = f1.readline()
            if not row:
                break
            m_cap = row.strip().split('\t')
            m_user = str(m_cap[0])
            m_item = str(m_cap[1])
            m_tag_id = str(m_cap[2])
            if x_id == str(m_cap[which]):
                f3.write(m_user + '\t' + m_item + '\t' + m_tag_id + '\n')
                triple_cnt += 1
    f3.close()
    f2.close()
    f1.close()
    update_len(3, triple_cnt)
    print(triple_out + ' has generated')


def select_tuple_by_triple(tuple_in, triple_in, tuple_out):
    """
    select t-f or t-v by u-i-t
    :param tuple_in:
    :param triple_in:
    :param tuple_out:
    :return:
    """
    f1 = open(tuple_in)
    f2 = open(triple_in)
    f3 = open(tuple_out, 'w')
    visited = set()
    while True:
        line = f2.readline()
        if not line:
            break
        tag_id = str(line.strip().split('\t')[2])
        visited.add(tag_id)
    while True:
        line = f1.readline()
        if not line:
            break
        tag_id = str(line.strip().split('\t')[0])
        if tag_id in visited:
            f3.write(line)
    f3.close()
    f2.close()
    f1.close()
    print(tuple_out + ' has generated')


def select_tuple_by_tuple(by_file, selected_file, file_out):
    """
    select tuple by tuple.eg. select t-v by t-f
    :param by_file:
    :param selected_file:
    :param file_out:
    :return:
    """
    f1 = open(by_file)
    f2 = open(selected_file)
    f3 = open(file_out, 'w')
    visite = set()
    while True:
        line = f1.readline()
        if not line:
            break
        tag_id = str(line.strip().split('\t')[0])
        visite.add(tag_id)
    while True:
        line = f2.readline()
        if not line:
            break
        tag_id = str(line.strip().split('\t')[0])
        if tag_id in visite:
            f3.write(line)
    f3.close()
    f2.close()
    f1.close()
    print(file_out + ' has generated')


def map_triple(triple_in, triple_out, tag_map_out):
    """
    map the triple, directly map the user,item in triple_out, but stores tag_map in tag_map_out, also update len.txt
    the format of tag_map_out: old_id+'\t'+new_id+'\n'
    :param triple_in:
    :param triple_out:
    :param tag_map_out:
    :return:
    """
    map_u = dict()
    map_i = dict()
    map_t = dict()
    cnt_u = 1
    cnt_i = 1
    cnt_t = 1
    f1 = open(triple_in)
    f2 = open(triple_out, 'w')
    f3 = open(tag_map_out, 'w')
    while True:
        line = f1.readline()
        if not line:
            break
        cap = line.strip().split('\t')
        user = str(cap[0])
        item = str(cap[1])
        tag = str(cap[2])
        if user not in map_u:
            map_u[user] = cnt_u
            user = str(cnt_u)
            cnt_u += 1
        else:
            user = str(map_u[user])
        if item not in map_i:
            map_i[item] = cnt_i
            item = str(cnt_i)
            cnt_i += 1
        else:
            item = str(map_i[item])
        if tag not in map_t:
            map_t[tag] = cnt_t
            f3.write(tag + '\t' + str(cnt_t) + '\n')
            tag = str(cnt_t)
            cnt_t += 1
        else:
            tag = str(map_t[tag])
        f2.write(user + '\t' + item + '\t' + tag + '\n')
    f3.close()
    f2.close()
    f1.close()
    update_len(0, cnt_u - 1)
    update_len(1, cnt_i - 1)
    update_len(2, cnt_t - 1)
    print(triple_out + ', ' + tag_map_out + ' has generated')


def map_tag(tag_map_in, tuple_in, tuple_out):
    """
    map the tuple_in(t-f or t-v)
    :param tag_map_in: format with old_id+'\t'+new_id+'\n'
    :param tuple_in:
    :param tuple_out:
    :return:
    """
    f1 = open(tag_map_in)
    f2 = open(tuple_in)
    f3 = open(tuple_out, 'w')
    tag_map = dict()
    while True:
        line = f1.readline()
        if not line:
            break
        cap = line.strip().split('\t')
        tag_map[str(cap[0])] = str(cap[1])
    while True:
        line = f2.readline()
        if not line:
            break
        cap = line.strip().split('\t')
        old_id = str(cap[0])
        value = str(cap[1])
        new_id = tag_map[old_id]
        f3.write(new_id + '\t' + value + '\n')
    f3.close()
    f2.close()
    f1.close()
    print(tuple_out + ' has generated')


def final_triple(tag_map_in, triple_in, triple_out):
    """
    generate the final triples
    :param tag_map_in:
    :param triple_in: u-i-t
    :param triple_out:
    :return:
    """
    f1 = open(tag_map_in)
    f2 = open(triple_in)
    f3 = open(triple_out, 'w')
    tag_map = dict()
    while True:
        line = f1.readline()
        if not line:
            break
        cap = line.strip().split('\t')
        tag_map[str(cap[0])] = str(cap[1])
    while True:
        line = f2.readline()
        if not line:
            break
        cap = line.strip().split('\t')
        user = str(cap[0])
        item = str(cap[1])
        old_tag = str(cap[2])
        new_tag = tag_map[old_tag]
        f3.write(user + '\t' + item + '\t' + new_tag + '\n')
    f3.close()
    f2.close()
    f1.close()
    print(triple_out + ' has generated')


def statistic(triple_in, file_out):
    """
    statistics of some indices: the minimum frequency of u,i,t sets
    :param triple_in: final triple u-i-t
    :param file_out:
    :return:
    """
    # format str-integer
    dict_u = dict()
    dict_i = dict()
    dict_t = dict()
    f1 = open(triple_in)
    f2 = open(file_out, 'w')
    while True:
        line = f1.readline()
        if not line:
            break
        cap = line.strip().split('\t')
        user = str(cap[0])
        item = str(cap[1])
        tag = str(cap[2])
        if user not in dict_u:
            dict_u[user] = 1
        else:
            dict_u[user] += 1
        if item not in dict_i:
            dict_i[item] = 1
        else:
            dict_i[item] += 1
        if tag not in dict_t:
            dict_t[tag] = 1
        else:
            dict_t[tag] += 1
    min_u = find_min(dict_u)
    min_i = find_min(dict_i)
    min_t = find_min(dict_t)
    f2.write('statistics:\n')
    f2.write(str(get_len(0)) + 'users, ' + str(get_len(1)) + 'items, ' + str(get_len(2)) + 'tags\n')
    f2.write('the minimum frequency of users: ' + str(min_u) + '\n')
    f2.write('the minimum frequency of items: ' + str(min_i) + '\n')
    f2.write('the minimum frequency of tags: ' + str(min_t) + '\n')
    f2.close()
    f1.close()
    print(file_out + ' has generated')


def find_min(d):
    min_num = 0x7fffffff
    for k in d:
        min_num = min(min_num, d[k])
    return min_num


def sort_tuple(file_in, file_out, which):
    f1 = open(file_in)
    f2 = open(file_out, 'w')
    mp = dict()
    while True:
        line = f1.readline()
        if not line:
            break
        cap = line.strip().split('\t')
        if which == 0:
            mp[int(cap[0])] = str(cap[1])
        else:
            mp[str(cap[0])] = int(cap[1])
    sorted_mp = sorted(mp.items(), key=operator.itemgetter(which))
    for x, y in sorted_mp:
        f2.write(str(x) + '\t' + str(y) + '\n')
    f2.close()
    f1.close()

# def test():
#     init()
#     # u-i-t=>t-f
#     count_f_ge_minf(USER_ITEM_TAG_PATH, STORED_PATH + 't_f_1.dat', 2, 100)
#     # t-f=>n of t-f
#     select_random(STORED_PATH + 't_f_1.dat', STORED_PATH + 't_f_2.dat', 2, 500)
#     select_top(STORED_PATH + 't_f_1.dat', STORED_PATH + 't_f_2.dat', 2, 500)
#     # t-f,t-v=>filtered t-f,t-v
#     tag_filter(STORED_PATH + 't_f_2.dat', TAG_VALUE_PATH, STORED_PATH + 't_f_3.dat', STORED_PATH + 't_v_1.dat')
#     # t-f,u-i-t=>u-i-t
#     select_triple_by_tuple(USER_ITEM_TAG_PATH, STORED_PATH + 't_f_3.dat', STORED_PATH + 'u_i_t_1.dat', 2)
#
#     # u-i-t=>u-f
#     count_f_ge_minf(STORED_PATH + 'u_i_t_1.dat', STORED_PATH + 'u_f_1.dat', 0, 4)
#     # u-f=>n of u-f
#     select_top(STORED_PATH + 'u_f_1.dat', STORED_PATH + 'u_f_2.dat', 0, 100)
#     # u-f,u-i-t=>u-i-t
#     select_triple_by_tuple(STORED_PATH + 'u_i_t_1.dat', STORED_PATH + 'u_f_2.dat', STORED_PATH + 'u_i_t_2.dat', 0)
#
#     # u-i-t=>i-f
#     count_f_ge_minf(STORED_PATH + 'u_i_t_1.dat', STORED_PATH + 'i_f_1.dat', 1, 4)
#     # i-f=>n of i-f
#     select_top(STORED_PATH + 'i_f_1.dat', STORED_PATH + 'i_f_2.dat', 1, 100)
#     # i-f,u-i-f=>u-i-f
#     select_triple_by_tuple(STORED_PATH + 'u_i_t_2.dat', STORED_PATH + 'i_f_2.dat', STORED_PATH + 'u_i_t_3.dat', 1)
#
#     # u-i-f,t-f,t-v=>t-f,t-v
#     select_tuple_by_triple(STORED_PATH + 't_f_3.dat', STORED_PATH + 'u_i_t_3.dat', STORED_PATH + 't_f_4.dat')
#     select_tuple_by_tuple(STORED_PATH + 't_f_4.dat', STORED_PATH + 't_v_1.dat', STORED_PATH + 't_v_2.dat')
#     # map
#     map_triple(STORED_PATH + 'u_i_t_3.dat', STORED_PATH + 'u_i_t_4.dat', STORED_PATH + 'tag_map.dat')
#     map_tag(STORED_PATH + 'tag_map.dat', STORED_PATH + 't_f_4.dat', STORED_PATH + 't_f_5.dat')
#     map_tag(STORED_PATH + 'tag_map.dat', STORED_PATH + 't_v_2.dat', STORED_PATH + 't_v_3.dat')
#     # statistic
#     statistic(STORED_PATH + 'u_i_t_4.dat', STORED_PATH + 'STATISTIC.dat')
#
#
# test()
