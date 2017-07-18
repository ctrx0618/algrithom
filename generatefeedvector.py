# -*- coding:utf-8 -*-

import feedparser
import re


def getwords(html):
    # 去掉HTML标记
    txt = re.compile(r'<[^>]+>').sub('', html)

    # 利用所有非字母字符拆分出单词
    words = re.compile(r'[^A-Z^a-z]+').split(txt)

    # 转化成小写
    return [word.lower() for word in words if word != '']


def get_word_count(url):

    # 解析订阅源
    d = feedparser.parse(url)
    wc = {}

    for e in d.entries:
        if 'summary' in e :
            summary = e.summary
        else:
            summary = e.description

        words = getwords(e.title + ' ' + summary)
        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1

    return d.feed.title, wc
