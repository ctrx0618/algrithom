# -*- coding:utf-8 -*-

import feedparser
import re


def get_word_count(url):

    # 解析订阅源
    d = feedparser.parse(url)
    wc = {}

    for e in d.entries:
        if 'summary' in e :
            summary = e.summary
        else:
            summary = e.description
