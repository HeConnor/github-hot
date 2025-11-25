#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/11/18
# @USER    : Shengji He
# @File    : storage.py.py
# @Software: PyCharm
# @Version  : Python-
# @TASK:
from typing import List, Dict, Any
import pandas as pd
import re


def create_markdown(date, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("## " + date + " Github Trending\n")


def save_to_md(ds, filename, language, topk=5):
    df = pd.DataFrame(ds, columns=['title', 'url', 'description', 'star', 'fork', 'new_star'])
    df.sort_values(by=['new_star', 'star', 'fork'], ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df = df.head(topk)
    with open(filename, "a", encoding="utf-8") as f:
        f.write('\n### {language}\n'.format(language=language))

        for i in range(len(df)):
            title = df.iloc[i]['title']
            url = df.iloc[i]['url']
            description = df.iloc[i]['description']
            star = df.iloc[i]['star']
            fork = df.iloc[i]['fork']
            new_star = df.iloc[i]['new_star']

            out = "* [{title}]({url}): {description} ***Star:{stars} Fork:{fork} Today stars:{new_star}***\n".format(
                title=title, url=url, description=description, stars=star, fork=fork, new_star=new_star)
            f.write(out)


def save_to_str(ds, language, topk=5):
    df = pd.DataFrame(ds, columns=['title', 'url', 'description', 'star', 'fork', 'new_star'])
    df.sort_values(by=['new_star', 'star', 'fork'], ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df = df.head(topk)
    msg = '\n### {language}\n'.format(language=language)

    for i in range(len(df)):
        title = df.iloc[i]['title']
        url = df.iloc[i]['url']
        description = df.iloc[i]['description']
        star = df.iloc[i]['star']
        fork = df.iloc[i]['fork']
        new_star = df.iloc[i]['new_star']

        out = "* [{title}]({url}): {description} ***Star:{stars} Fork:{fork} Today stars:{new_star}***\n".format(
            title=title, url=url, description=description, stars=star, fork=fork, new_star=new_star)
        msg += out
    return msg


def md_string_to_data(markdown_string: str) -> Dict[str, Any]:
    """
    将Markdown字符串转换回原始数据结构

    Args:
        markdown_string: Markdown格式的字符串

    Returns:
        dict: 包含各语言数据的字典
    """
    # 解析日期
    date_match = re.search(r'## (.+) Github Trending', markdown_string)
    matched_date = date_match.group(1) if date_match else "Unknown Date"

    # 按语言分割内容
    language_sections = re.split(r'\n### ', markdown_string)
    if date_match:
        language_sections = language_sections[1:]  # 跳过第一个空字符串或日期部分
    result = {}

    for section in language_sections:
        if not section.strip():
            continue

        # 提取语言名称
        language_match = re.match(r'(.+?)\n', section)
        if not language_match:
            language = ''
            # continue
        else:
            language = language_match.group(1).strip()
        if language in result:
            print(f'WARNING: existed language: {language}, skipped')
            continue

        # 提取每个项目
        items = re.findall(
            r'\*\s*\[(.+?)\]\((.+?)\):\s*(.+?)\s*\*\*\*Star:(\d+)\s*Fork:(\d+)\s*Today stars:(\d+)\*\*\*', section)
        cur_items = []
        for title, url, description, star, fork, new_star in items:
            cur_items.append([
                title.strip(),
                url.strip(),
                description.strip(),
                int(star),
                int(fork),
                int(new_star),
            ])
        result[language] = cur_items
    return result
