# -*- coding: utf-8 -*-
"""题库公式格式净化库（被 merge_bank.py 调用）
规则：< 转义、$…$ 改 \\(…\\)、\\[2mm] 行距补反斜杠、控制字符还原、\\汉字 转 \\text{}
"""
import re

CJK = '\u4e00-\u9fff'

# ---------------------------------------------------------------- 扫描器
def scan(s):
    """返回 [(kind, start, end, body)]；正确跳过 \\\\ 行内换行转义"""
    out, i, n = [], 0, len(s)
    while i < n:
        if s[i] == '$' and i + 1 < n and s[i + 1] == '$':
            j = s.find('$$', i + 2)
            if j > i:
                out.append(('$$', i, j + 2, s[i + 2:j])); i = j + 2; continue
            i += 2; continue
        if s[i] == '\\' and i + 1 < n and s[i + 1] in '([':
            ch = ')' if s[i + 1] == '(' else ']'
            j, k = -1, i + 2
            while k < n - 1:
                if s[k] == '\\':
                    if s[k + 1] == '\\':
                        k += 2; continue
                    if s[k + 1] == ch:
                        j = k; break
                    k += 2; continue
                k += 1
            if j > i:
                out.append(('\\' + s[i + 1], i, j + 2, s[i + 2:j])); i = j + 2; continue
            i += 2; continue
        i += 1
    return out

# ---------------------------------------------------------------- 单条规则
def r_fix_fullwidth_delim(s):
    n0 = s
    s = s.replace('\\）', '\\)').replace('\\（', '\\(')
    return s, (1 if s != n0 else 0)

def r_fix_rowbreak(s):
    """\\[2mm] / \\[4pt] 这类行距应为 \\\\[..]（双反斜杠）"""
    def rep(m):
        return '\\\\[' + m.group(1) + ']'
    s2, c = re.subn(r'(?<!\\)\\\[(\d+(?:\.\d+)?\s*(?:mm|cm|pt|em|ex|in|baselineskip))\]', rep, s)
    return s2, c

def r_escape_lt(s):
    """数学模式内 <字母/< / </<! 会被 innerHTML 当标签"""
    s2, c = re.subn(r'<(?=[A-Za-z/!?])', '&lt;', s)
    return s2, c

def r_backslash_cjk(s):
    """\\即 之类：反斜杠后直接跟汉字，KaTeX 视为未定义命令"""
    def rep(m):
        return '\\ \\text{' + m.group(1) + '}\\ '
    s2, c = re.subn(r'\\(' + '[' + CJK + ']' + ')', rep, s)
    return s2, c

def r_ctrl(s):
    """JSON 转义被吃掉形成的控制字符：\\f 变 0x0C 之类"""
    n = 0
    for bad, good in (('\x0c', '\\f'), ('\x08', '\\b'), ('\x0b', '\\v'), ('\x07', '\\a')):
        if bad in s:
            n += s.count(bad)
            s = s.replace(bad, good)
    s2 = re.sub(r'[\x00-\x06\x0e-\x1f]', '', s)
    n += len(s) - len(s2)
    return s2, n

def r_single_dollar(s):
    """把 $公式$ 改成 \\(公式\\)（$$…$$ 保持不动）"""
    out, i, n, cnt = [], 0, len(s), 0
    while i < n:
        if s[i] == '$' and i + 1 < n and s[i + 1] == '$':
            j = s.find('$$', i + 2)
            if j > i:
                out.append(s[i:j + 2]); i = j + 2; continue
            out.append('$$'); i += 2; continue
        if s[i] == '$':
            j = s.find('$', i + 1)
            if 0 < j and j > i + 1 and '\n' not in s[i:j]:
                out.append('\\(' + s[i + 1:j] + '\\)'); i = j + 1; cnt += 1; continue
        out.append(s[i]); i += 1
    return ''.join(out), cnt

def r_matrix_rowbreak(s):
    """矩阵/数组里的换行 \\\\ 被写成单个 \\，表现为 \\3 / \\0 / \\-15 这类非法命令"""
    def rep(m):
        return '\\\\' + m.group(1)
    s2, c = re.subn(r'(?<!\\)\\(?!\\)([0-9])', rep, s)
    # 换行后紧跟负数：2\-15 这类（用函数替换，避开替换模板对 \\ 的二次转义）
    s2b, c2 = re.subn(r'(?<=[0-9&])\\(?=-[0-9])', lambda m: '\\\\', s2)
    return s2b, c + c2

RULES_TEXT = [r_fix_fullwidth_delim, r_fix_rowbreak, r_ctrl, r_single_dollar]
RULES_MATH = [r_matrix_rowbreak, r_escape_lt, r_fix_rowbreak, r_backslash_cjk]

def fix(s):
    """返回 (新串, {规则名: 次数})"""
    if not isinstance(s, str) or not s:
        return s, {}
    st = {}
    for f in RULES_TEXT:
        s, c = f(s)
        if c: st[f.__name__] = st.get(f.__name__, 0) + c
    # 逐段修数学模式内容
    segs = scan(s)
    if segs:
        parts, pos = [], 0
        for kind, a, b, body in segs:
            parts.append(s[pos:a])
            nb, bc = body, {}
            for f in RULES_MATH:
                nb, c = f(nb)
                if c: bc[f.__name__] = bc.get(f.__name__, 0) + c
            for k, v in bc.items():
                st[k] = st.get(k, 0) + v
            off = 2 if kind == '$$' else 2
            parts.append(s[a:a + off] + nb + s[b - off:b])
            pos = b
        parts.append(s[pos:])
        s = ''.join(parts)
    return s, st
