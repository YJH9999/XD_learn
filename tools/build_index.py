#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""XD_learn 索引构建脚本：扫描 assets/content/，生成 manifest.js 与 search-index.js。
用法：python tools/build_index.py"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "assets", "content")

# 章节顺序（文件名 = id + .html）
ORDER = [
    "第-0-篇-总览与速查",
    "第-1-篇-矩阵和线性方程组",
    "1-1-矩阵概述", "1-2-逆矩阵和行列式", "1-3-行列式的性质与应用",
    "1-4-矩阵的初等变换", "1-5-矩阵的秩和线性方程组", "1-6-分块矩阵",
    "1-7-矩阵应用举例", "复习题-1",
    "第-2-篇-向量与线性方程组",
    "2-1-向量及其线性相关性", "2-2-向量空间", "2-3-线性方程组解的结构",
    "2-4-简单最小二乘问题", "复习题-2",
    "第-3-篇-线性变换与矩阵相似",
    "3-1-基变换和坐标变换", "3-2-线性变换", "3-3-相似矩阵",
    "3-4-矩阵的特征值和特征向量", "3-5-正交矩阵和正交变换",
    "3-6-矩阵相似对角化的简单应用", "复习题-3",
    "第-4-篇-二次型",
    "4-1-二次型及其标准形", "4-2-正定二次型", "4-3-二次型的简单应用", "复习题-4",
    "附录篇-速查与精选",
    "附录-a-公式速查卡", "附录-b-易错点总清单", "附录-c-典型例题精选", "结语",
]

TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")

def clean(s):
    return WS_RE.sub(" ", TAG_RE.sub("", s)).strip()

def main():
    manifest, titles, headmap, search = [], {}, {}, []
    missing = []
    for i, cid in enumerate(ORDER):
        fname = cid + ".html"
        path = os.path.join(CONTENT, fname)
        if not os.path.exists(path):
            missing.append(fname); continue
        manifest.append({"id": cid, "f": fname})
        html = open(path, encoding="utf-8").read()
        # 收集标题（去掉 fav 按钮部分）
        html = re.sub(r'<button class="fav".*?</button>', "", html, flags=re.S)
        for m in re.finditer(r"<(h[1-4])[^>]*id=\"([^\"]+)\"[^>]*>(.*?)</\1>",
                             html, flags=re.S):
            tag, hid, inner = m.group(1), m.group(2), m.group(3)
            inner = re.sub(r"<span class=\"rkchip.*?</span>", "", inner, flags=re.S)
            title = clean(inner)
            titles[hid] = title
            headmap[hid] = i
            text = ""
            # 提取该标题到下一个标题之间的正文片段
            nxt = re.search(r"<h[1-4][^>]*>", html[m.end():])
            body = html[m.end(): m.end() + (nxt.start() if nxt else len(html[m.end():]))]
            text = clean(body)[:400]
            search.append({"id": hid, "t": title, "s": text,
                           "lv": int(tag[1])})
    if missing:
        print("缺失文件:", missing); sys.exit(1)

    with open(os.path.join(ROOT, "assets", "manifest.js"), "w", encoding="utf-8") as f:
        f.write("window.CK_MANIFEST=" + json.dumps(manifest, ensure_ascii=False)
                + ";\nwindow.CK_HEADMAP=" + json.dumps(headmap, ensure_ascii=False)
                + ";\nwindow.CK_TITLES=" + json.dumps(titles, ensure_ascii=False) + ";\n")
    with open(os.path.join(ROOT, "assets", "search-index.js"), "w", encoding="utf-8") as f:
        f.write("window.CK_SEARCH=" + json.dumps(search, ensure_ascii=False) + ";\n")
    print(f"OK: {len(manifest)} 个章节, {len(search)} 个标题已索引")

if __name__ == "__main__":
    main()
