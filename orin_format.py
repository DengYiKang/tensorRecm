import re
import subsetGen

PATH = '/home/yikang/Documents/dataset/ml-20m/'
STORED_PATH = PATH + 'subset/'
pattern = re.compile(r'[^?!@#$%\^&*()\+\/\[\]\\\. ]+$')


def format_triple(triple_in, triple_out):
    """
    unify the format with user+'\t'+item+'\t'+tag+'\n', and filter the tag field
    :param triple_in:
    :param triple_out:
    :return:
    """
    f1 = open(triple_in)
    f2 = open(triple_out, 'w')
    f1.readline()
    while True:
        line = f1.readline()
        if not line:
            break
        cap = line.strip().split(',')
        try:
            user = str(cap[0])
            item = str(cap[1])
            tag = str(cap[2])
            if pattern.match(tag):
                f2.write(user + '\t' + item + '\t' + tag + '\n')
        except Exception:
            print('format_triple ERROR:\n\t' + line)
    f2.close()
    f1.close()


def format_tuple(tuple_in, tuple_out):
    """
    unity the format with key+'\t'+value+'\n', and filter the value field
    :param tuple_in:
    :param tuple_out:
    :return:
    """
    f1 = open(tuple_in)
    f2 = open(tuple_out, 'w')
    f1.readline()
    while True:
        line = f1.readline()
        if not line:
            break
        cap = line.strip().split(',')
        try:
            x = str(cap[0])
            y = str(cap[1])
            if pattern.match(y):
                f2.write(x + '\t' + y + '\n')
        except Exception:
            print('format_tuple ERROR:\n\t' + line)
    f2.close()
    f1.close()


def gen_u_i_t_orgin(triple_in, tuple_in, triple_out, which):
    """
    which-pos value in triples is presented as non-id, to change it by the relationships in tuple_in
    :param triple_in:
    :param tuple_in:
    :param triple_out:
    :param which: user-0, item-1, tag-2
    :return:
    """
    f1 = open(triple_in)
    f2 = open(tuple_in)
    f3 = open(triple_out, 'w')
    mp = dict()
    triple_cnt=0
    while True:
        line = f2.readline()
        if not line:
            break
        cap = line.strip().split('\t')
        mp[str(cap[1])] = str(cap[0])
    while True:
        line = f1.readline()
        if not line:
            break
        cap = line.strip().split('\t')
        tmp_list = list()
        try:
            tmp_list = [str(cap[0]), str(cap[1]), str(cap[2])]
        except Exception:
            # print('gen_u_i_t_orgin ERROR: ' + '\n\t' + str(tmp_list))
            pass
        try:
            tmp_list[which] = mp[tmp_list[which]]
            f3.write(tmp_list[0] + '\t' + tmp_list[1] + '\t' + tmp_list[2] + '\n')
            triple_cnt+=1
        except Exception:
            continue
    subsetGen.update_len(3, triple_cnt)
    f3.close()
    f2.close()
    f1.close()


def go():
    format_triple(PATH + 'tags.csv', STORED_PATH + 'user_item_tag.dat')
    format_tuple(PATH + 'genome-tags.csv', STORED_PATH + 'tags_format.dat')
    gen_u_i_t_orgin(STORED_PATH + 'user_item_tag.dat', STORED_PATH + 'tags_format.dat',
                    STORED_PATH + 'user_item_tag_format.dat', 2)
