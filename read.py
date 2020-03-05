import csv
import re

with open('/home/yikang/Documents/dataset/hetrec2011-delicious-2k/user_tag_bookmark_utf8.dat') as f:
    cnt = 0
    tot = 0
    pattern = re.compile(r'[^?!@#$%\^&*()\+\/]+$')
    while True:
        line = f.readline()
        if not line: break
        cap = line.strip().split('\t')
        if not pattern.match(cap[1]): continue
        cnt += 1
        if cnt == 10: break
        print(cap)
