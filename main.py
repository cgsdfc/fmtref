"""
[2]Benkedjouh T, Medjaher K, Zerhouni N, et al. Remaining Useful Life Estimation Based on Nonlinear Feature Reduction and Support Vector Regression[J]. Engineering Applications of Artificial Intelligence, 2013, 26(7): 1751-1760.
英文期刊文献：序号└┘作者. 文章名[J]. 学术刊物名, 出版年, 卷(期): 起止页码.
注：作者姓先名后，多于三位加“, et al.”，文章名和期刊名中所有实词首字母大写。

[10]Su H, Zhang X. Cognitive Radio Based Multi-channel MAC Protocols for Wireless Ad Hoc Networks[C]. IEEE Global Telecommunications Conference, Washington, D.C., USA, 2007: 4857-4861.
学术会议文献：序号└┘作者. 文章名[C]. 会议名称, 会议地址, 年份: 引用部分起止页码.
"""
import bibtexparser
from pprint import pprint
from pathlib import Path as P
import doctest
from titlecase import titlecase
import re


def preprocess_string(s: str):
    """
    >>> preprocess_string(r'{-}')
    '-'
    >>> preprocess_string('a\\nb')
    'a b'
    """
    s = re.sub(r"[{}]", "", s)
    s = re.sub("\n", " ", s)
    return s


def deal_author_name(s: str):
    """
    >>> deal_author_name('Jing Zhao')
    'Zhao J'
    >>> deal_author_name('Xijiong Xie')
    'Xie X'
    """
    name_list = s.split(" ")
    *ming, xing = name_list
    xing = xing.capitalize()
    ming = [x[0].upper() for x in ming]
    res = " ".join([xing] + ming)
    return res


def deal_author(s: str):
    """
    >>> deal_author('Jing Zhao and Xijiong Xie and Xin Xu and Shiliang Sun')
    'Zhao J, Xie X, Xu X, et al'
    >>> deal_author('Jing Zhao and Xijiong Xie')
    'Zhao J, Xie X'
    """
    author_list = s.split(" and ")
    author_list = list(map(deal_author_name, author_list))
    if len(author_list) > 3:
        author_list = author_list[:3]
        author_list.append("et al")
    res = ", ".join(author_list)
    return res


def deal_title(s: str):
    """
    >>> deal_title('Multi-view learning overview: Recent progress and new challenges')
    'Multi-View Learning Overview: Recent Progress and New Challenges'
    """
    res = titlecase(s)
    return res


def isallcap(s: str):
    return all(x.isupper() and x.isascii() for x in s)


def deal_booktitle(x: str):
    x = x.split(", ")
    loc_list = [xx for xx in x if isallcap(xx)]
    loc_list = ", ".join(loc_list)
    name = max(x, key=len)
    return name, loc_list


def format_entry(entry: dict, idx: int):
    entry = {key: preprocess_string(val) for key, val in entry.items()}

    ENTRYTYPE = entry["ENTRYTYPE"]

    author = entry["author"]
    author = deal_author(author)
    title = entry["title"]
    title = deal_title(title)
    year = entry["year"]
    pages = entry["pages"]

    if ENTRYTYPE == "article":
        journal = entry["journal"]
        journal = titlecase(journal)
        # vol全称是Volume，就是卷，No是期。
        volume = entry["volume"]
        # 卷(期): 起止页码.
        if "number" in entry:
            number = entry["number"]
            vnp = f"{volume}({number}): {pages}"
        else:
            vnp = f"{volume}: {pages}"
        # 作者. 文章名[J]. 学术刊物名, 出版年, 卷(期): 起止页码.
        res = f"{author}. {title}[J]. {journal}, {year}, {vnp}."

    elif ENTRYTYPE == "inproceedings":
        booktitle = entry["booktitle"]
        name, loc_list = deal_booktitle(booktitle)
        # 作者. 文章名[C]. 会议名称, 会议地址, 年份: 引用部分起止页码.
        res = f"{author}. {title}[C]. {name}, {loc_list}, {year}: {pages}."
    else:
        raise ValueError(ENTRYTYPE)

    res = f"[{idx}] {res}"

    return res


def process_bibfile(bibfile: P):
    database = bibtexparser.load(bibfile.open())
    for idx, entry in enumerate(database.entries, 1):
        print(format_entry(entry, idx))


if __name__ == "__main__":
    doctest.testmod()
    # exit()

    bibfile = P("conf-jnl.bib")
    process_bibfile(bibfile)