# -*- coding:utf-8 -*-

'''
author: Xinhua Cheng
email: 931736813@qq.com
'''

import re
import requests
from tqdm import tqdm
import os
import argparse


def find_url(start_page, end_page, keyword):
    url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + keyword + '&pn='
    img_url_list = []
    for cur_page in tqdm(range(start_page - 1, end_page)):
        try:
            result = requests.get(url + str(cur_page), timeout=10)
        except BaseException:
            print("Error in visiting page " + str(cur_page + 1))
            continue
        else:
            result = result.text
            img_url_list += re.findall('"objURL":"(.*?)",', result, re.S)
    return img_url_list


def download_img(img_url_list, file_path, img_name):
    index = 1
    for item in tqdm(img_url_list):
        try:
            if item is not None:
                img = requests.get(item, timeout=10)
            else:
                continue
        except BaseException:
            print('Error in downloading image ' + str(index))
            continue
        else:
            string = file_path + '/' + img_name + '_' + str(index) + '.jpg'
            fp = open(string, 'wb')
            fp.write(img.content)
            fp.close()
            index += 1
    return


def img_crawler(start_page, end_page, keyword, img_name, file_path):
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    print("Parsing images url...")
    img_url_list = find_url(start_page, end_page, keyword)
    print("Downloading...")
    download_img(img_url_list, file_path, img_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("keyword", type=str, help="search keyword")
    parser.add_argument("-f", "--file_path", type=str, default="data/", help="path of save file")
    parser.add_argument("-n", "--img_name", type=str, default="data", help="name of images")
    parser.add_argument("-s", "--start_page", type=int, default=1, help="index of start page")
    parser.add_argument("-e", "--end_page", type=int, default=1, help="index of end page")
    arg = parser.parse_args()
    img_crawler(arg.start_page, arg.end_page, arg.keyword, arg.img_name, arg.file_path)
