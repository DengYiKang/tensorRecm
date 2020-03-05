import re
import random
import linecache

# relations(old u-i-t) stored in .../old_triple.dat
# relations(new tag id-old tag id) stored in .../tag_map.dat
# relations(new tag id-tag value) stored in .../tags.dat
# relations(new user id-old user id) stored in .../user_map.dat
# relations(new item id-old item id) stored in .../item_map.dat
# relations(new u-i-t) stored in .../new_triple.dat
PATH = "/home/yikang/Documents/dataset/hetrec2011-delicious-2k/"
STORED_PATH = PATH + "subset-100/"
# [u-f,i-f,t-f],default [-1,-1,-1]
LEN_FILE = "len.txt"


def init():
    with open(STORED_PATH + LEN_FILE, 'w') as wf:
        wf.write(str(-1) + '\t' + str(-1) + '\t' + str(-1) + '\n')


def get_len(which):
    """
    get the len in LEN_FILE
    :param which: user-0, item-1, tag-2
    :return: integer. the len of which
    """
    value = ''
    with open(STORED_PATH + LEN_FILE) as rf:
        value = int(rf.readline().strip().split('\t')[which])
    return value


def update_len(which, value):
    """
    update the file len.txt which stores the length of files like u-f, i-f, t-f...
    :param which: user-0, item-1, tag-2
    :param value: new value
    :return:
    """
    tmp = list()
    with open(STORED_PATH + LEN_FILE) as rf:
        tmp = rf.readline().strip().split('\t')
    tmp[which] = str(value)
    with open(STORED_PATH + LEN_FILE, 'w') as wf:
        wf.write(str(tmp[0]) + '\t' + str(tmp[1]) + '\t' + str(tmp[2]) + '\n')


def statistic(file_in, file_out, which, min_f):
    """
    count the frequency of "which" in file file_in, and output the id whose frequency > min_f
    :param file_in:
    :param file_out:
    :param which:integer value:'user'-0;'item'-1;'tag'-2
    :param min_f:
    :return:
    """
    m = dict()
    count = 0
    with open(PATH + file_in) as rf:
        while True:
            line = rf.readline()
            if not line:
                break
            data = line.strip().split('\t')
            key = data[which]
            if key in m:
                m[key] += 1
            else:
                m[key] = 1
    with open(STORED_PATH + file_out, 'w') as wf:
        for k, v in m.items():
            if v >= min_f:
                wf.write(str(k) + '\t' + str(v) + '\n')
                count += 1
    update_len(which, count)


def select(file_in, file_out, which, n):
    """
    select n tuples randomly, and update len.txt
    :param file_in: format is ?-frequency
    :param file_out: format is ?-frequency
    :param which:user-0;item-1;tag-2
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
    with open(STORED_PATH + file_out, 'w') as wf:
        times = 0
        while times < n:
            row = random.randint(0, len)
            if row in visited:
                continue
            else:
                visited.add(row)
            tmp_list = linecache.getline(STORED_PATH + file_in, row).strip().split('\t')
            wf.write(str(tmp_list[0]) + '\t' + str(tmp_list[1]) + '\n')
            times += 1
    update_len(which, n)


def tag_filter(t_f_path, t_v_path, t_f_out, t_v_out):
    """
    drop the illegal tags whose value is not a single word
    :param t_f_path: tag-frequency file
    :param t_v_path: tagId-value file
    :param t_f_out: output file that stored t-f
    :param t_v_out: output file that stored t-v
    :return:
    """
    pattern = re.compile(r'[^?!@#$%\^&*()\+\/\[\]]+$')
    f1 = open(STORED_PATH + t_f_path)
    f2 = open(PATH + t_v_path)
    f3 = open(STORED_PATH + t_f_out, 'w')
    f4 = open(STORED_PATH + t_v_out, 'w')
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


def select_3_triple(triple_in, tuple_in, triple_out, which):
    """
    select triples by t-f relations in file t_f_in
    :param triple_in: stores triples
    :param tuple_in: stores t-f relations
    :param triple_out: output extracted triples
    :param which: user-0,item-1,tag-2
    :return:
    """
    f1 = open(triple_in)
    f2 = open(tuple_in)
    f3 = open(triple_out, 'w')
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
                break
            else:
                continue
    f3.close()
    f2.close()
    f1.close()


def select_tuple_by_triple(tuple_in, triple_in, tuple_out):
    # todo(yikang):function which select t-f and t-v by u-i-t
    pass


def map_tuple(tuple_in, tuple_out, map_out):
    # todo(yikang):function which map the id in file tuple_in to the consistent ids, store the map in file map_out
    pass


def final_triple(user_map, item_map, tag_map, triple_in, triple_out):
    # todo(yikang):function which generate the final dataset(triple) after the mapping
    pass


def test():
    init()
    statistic('user_tag_bookmark_utf8.dat', 'tag_f.dat', 2, 10)
    select('tag_f.dat', 'tag_f_100.dat', 2, 300)
    tag_filter('tag_f_100.dat', 'tags_utf8.dat', 't_f_filtered.dat', 't_v_filtered.dat')
    select_3_triple(PATH + 'user_tag_bookmark_utf8.dat', STORED_PATH + 't_f_filtered.dat',
                    STORED_PATH + 'u_i_t_filtered.dat')
    cnt = 0
    with open(STORED_PATH + 't_f_filtered.dat') as rf:
        while True:
            line = rf.readline()
            if not line:
                break
            cnt += 1
    print('lines of tag_f_filtered.dat: ' + str(cnt))
    print('the third value in len.txt: ' + str(get_len(2)))
    cnt = 0
    with open(STORED_PATH + 'u_i_t_filtered.dat') as rf:
        while True:
            line = rf.readline()
            if not line:
                break
            cnt += 1
    print('number of new triples: ' + str(cnt))


test()
