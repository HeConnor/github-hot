# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""

import requests
from pyquery import PyQuery

from storage import save_to_md, save_to_str


def scrape(language, filename, topk=5):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }

    url = 'https://github.com/trending/{language}'.format(language=language)
    r = requests.get(url, headers=HEADERS)
    assert r.status_code == 200

    d = PyQuery(r.content)
    items = d('div.Box article.Box-row')
    ds = []
    for item in items:
        i = PyQuery(item)
        title = i(".lh-condensed a").text()
        description = i("p.col-9").text()
        url = i(".lh-condensed a").attr("href")
        url = "https://github.com" + url
        star_fork = i(".f6 a").text().strip()
        star, fork = star_fork.split()
        new_star = i(".f6 svg.octicon-star").parent().text().strip().split()[1]
        star = int(star.replace(',', ''))
        fork = int(fork.replace(',', ''))
        new_star = int(new_star.replace(',', ''))
        ds.append([title, url, description, star, fork, new_star])
    if filename is None:
        return save_to_str(ds, language, topk)
    else:
        return save_to_md(ds, filename, language, topk)
