# -*- coding:utf-8 -*-

import numpy as np


def read_data():
    data_path = 'data\\data.txt'
    file = open(data_path, encoding='utf8')

    all_weibo_list = []
    a_weibo = []
    sentence_dict = {}
    phrase_list = []
    origin = ''

    line = file.readline()
    while line:
        # print(line)
        line = file.readline()

        if '---' in line:
            sentence_dict = {'origin': origin, 'phrase': phrase_list}
            origin = ''
            phrase_list = []
            a_weibo.append(sentence_dict)
            continue

        elif '===' in line:
            if len(phrase_list) != 0:
                sentence_dict = {'origin': origin, 'phrase': phrase_list}
                a_weibo.append(sentence_dict)
            if len(a_weibo) != 0:
                all_weibo_list.append(a_weibo)
            a_weibo = []
            origin = ''
            phrase_list = []

        else:
            if '*' in line:
                phrase_list.append(line.replace('*', '').replace('\n', ''))
            else:
                origin = line.replace('\n', '')

    print(all_weibo_list)
    np.save('data\\all_weibo_list', all_weibo_list)


if __name__ == '__main__':
    read_data()
    path = 'data\\all_weibo_list.npy'
    all_weibo_info = np.load(path)
    print(all_weibo_info)
    # list = []
    # print(len(list))
