# -*- coding:utf-8 -*-

from __future__ import division
from math import sqrt

# A dictionary of movie critics and their ratings of a small
# set of movies
critics = {'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
                         'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
                         'The Night Listener': 3.0},
           'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
                            'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 3.5},
           'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                                'Superman Returns': 3.5, 'The Night Listener': 4.0},
           'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                            'The Night Listener': 4.5, 'Superman Returns': 4.0,
                            'You, Me and Dupree': 2.5},
           'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                            'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 2.0},
           'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                             "The Night Listener": 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
           'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0, 'Superman Returns': 4.0}}


def sim_distance(prefs, person1, person2):
    """ 用于计算两人偏好的欧式距离

    :param prefs: 偏好数据
    :param person1: 第一人名字
    :param person2: 第二人名字
    :return: 欧式距离
    """
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    if len(si) == 0:
        return 0

    # 计算所有差值的平方和
    sum_of_square = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                         for item in si])

    return 1 / (1 + sqrt(sum_of_square))


def sim_pearson(prefs, person1, person2):
    """ 计算两人的皮尔逊相关度

    :param prefs: 偏好数据
    :param person1: 第一人名字
    :param person2: 第二人名字
    :return: 皮尔逊相关度
    """
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    n = len(si)
    if n == 0:
        return 1

    sum1 = sum(prefs[person1][it] for it in si)
    sum2 = sum(prefs[person2][it] for it in si)

    sum1Sq = sum(pow(prefs[person1][it], 2) for it in si)
    sum2Sq = sum(pow(prefs[person2][it], 2) for it in si)

    pSum = sum([prefs[person1][it] * prefs[person2][it] for it in si])

    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0:
        return 0
    return num / den


def sim_jaccard(prefs, person1, person2):
    """计算两人的Jaccard系数

    :param prefs: 偏好数据
    :param person1: 第一人名字
    :param person2: 第二人名字
    :return: Jaccard系数
    """
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    n = len(si)
    if n == 0:
        return 0

    return n / (len(person1) + len(person2) - n)


def top_matches(prefs, person, n=5, similarity=sim_pearson):
    score = [(similarity(prefs, person, other), other) for other in prefs if other != person]

    score.sort()
    score.reverse()
    return score[0:n]


def get_recommendations(prefs, person, similarity = sim_pearson):
    totals = {}
    sim_sum = {}

    for other in prefs:
        if other == person:
            continue

        sim = similarity(prefs, person, other)

        # 只保留正数评价
        if sim <= 0:
            continue

        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                sim_sum.setdefault(item, 0)
                sim_sum[item] += sim

        rankings = [(total / sim_sum[item], item) for item, total in totals.items()]

        rankings.sort()
        rankings.reverse()
        return rankings


if __name__ == "__main__":
    # 测试欧式距离用例
    print sim_distance(critics, "Lisa Rose", "Gene Seymour")

    # 测试皮尔逊相关度用例
    print sim_pearson(critics, "Lisa Rose", "Gene Seymour")

    # 测试Jaccard系数
    print sim_jaccard(critics, "Lisa Rose", "Gene Seymour")

    # 最佳匹配测试
    print top_matches(critics, 'Toby', n=10)

    # 测试推荐系统
    print get_recommendations(critics, 'Toby')
