#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by xzw on 2015/2/8

__author__ = 'xzw'

import os
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool


def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            # filter out keep-alive new chunks
            if chunk:
                f.write(chunk)
                f.flush()

    return local_filename

headers = {                                         #伪装浏览器
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/32.0.1700.76 Safari/537.36'
}

root_link = r"http://www.cs.princeton.edu/~wayne/kleinberg-tardos/"


def main():

    req = requests.get(root_link, headers=headers)

    if req.status_code == 200:
        soup = BeautifulSoup(req.text)
        # print soup.prettify()
        links = soup.find_all('a')
        links = [root_link + l.get('href') for l in links if l.get('href')]
        pdf_links = [l for l in links if l.endswith(".pdf")]

        pool = Pool(8)
        results = pool.map(download_file, pdf_links)

        print "all download finished\n"


if __name__ == '__main__':
    main()



