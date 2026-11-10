# -*- coding: utf-8 -*-
"""合并转录批件到题库：去重 → 分配新 id → 重建 theory_bank.js / solve_bank.js"""
import json, os, re, glob, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kp_map import KP_MAP, SRC_MAP, norm_src, norm_kp

BATCH_DIR = r"D:\Web\XD_learn\tools\batch"
CUR = r"D:\Web\XD_learn\tools\bank_current.json"
TYS = ["judge", "choice", "blank", "solve", "proof"]
TY_PREFIX = {"judge": "j", "choice": "c", "blank": "b", "solve": "s", "proof": "p"}
TY_SCORE = {"solve": 10, "proof": 8}

def norm(q):
    """题目文本归一化：去 HTML 标签、空白、全部标点，仅保留 CJK/字母/数字"""
    s = re.sub(r"<[^>]+>", "", q or "")
    s = re.sub(r"\\\\[a-zA-Z]+", "", s)      # LaTeX 命令
    s = re.sub(r"[^0-9a-zA-Z\u4e00-\u9fff]", "", s)
    return s

def escape_lt_in_math(s):
    """数学模式（\\(...\\) 与 $$...$$）内出现 <字母 会被 innerHTML 当标签吞掉，统一转义为 &lt;"""
    if not s or "<" not in s:
        return s
    parts, out, pos = [], [], 0
    for m in re.finditer(r"\\\(.*?\\\)|\$\$.*?\$\$", s, re.S):
        out.append(s[pos:m.start()])
        seg = re.sub(r"<(?=[a-zA-Z])", "&lt;", m.group(0))
        out.append(seg)
        pos = m.end()
    out.append(s[pos:])
    return "".join(out)

def load_current():
    with open(CUR, encoding="utf-8") as f:
        data = json.load(f)
    banks = {ty: list(data.get(ty, [])) for ty in TYS}
    # 存量条目全量净化（历史遗留的数学模式未转义 <字母 等）+ 知识点/来源归一化
    fixed = 0
    kp_norm = 0
    for ty in TYS:
        for q in banks[ty]:
            for k in ("q", "sol", "ans"):
                if isinstance(q.get(k), str):
                    s2 = escape_lt_in_math(q[k])
                    if s2 != q[k]:
                        q[k] = s2
                        fixed += 1
            if isinstance(q.get("opts"), list):
                q["opts"] = [escape_lt_in_math(str(o)) if isinstance(o, str) else o for o in q["opts"]]
            if "src" in q:
                s2 = norm_src(q.get("src"))
                if s2 != q.get("src"):
                    q["src"] = s2
            if "kp" in q:
                s2 = norm_kp(q.get("kp"))
                if s2 != q.get("kp"):
                    q["kp"] = s2
                    kp_norm += 1
    if fixed:
        print(f"存量题库净化: 修复 {fixed} 个字段")
    if kp_norm:
        print(f"知识点归一化: {kp_norm} 条 kp 已规范化")
    return banks

def clean_entry(e, src_default):
    """校验并规范化单条转录条目，失败返回 None"""
    ty = (e.get("ty") or "").strip().lower()
    ty_map = {"判断": "judge", "选择": "choice", "单选": "choice", "填空": "blank",
              "解答": "solve", "计算": "solve", "证明": "proof", "solution": "solve"}
    ty = ty_map.get(ty, ty)
    if ty not in TYS:
        return None
    q = (e.get("q") or "").strip()
    sol = (e.get("sol") or "").strip()
    if not q or len(q) < 5:
        return None
    if not sol:
        sol = "解析：见答案。" if e.get("ans") else "解析待补充。"
    entry = {"ty": ty, "ch": int(e.get("ch") or 1), "kp": norm_kp(e.get("kp")) or "综合",
             "src": norm_src(e.get("src") or src_default), "diff": min(max(int(e.get("diff") or 2), 1), 3),
             "q": escape_lt_in_math(q), "sol": escape_lt_in_math(sol)}
    if ty == "choice":
        opts = e.get("opts") or []
        if len(opts) < 3:
            return None
        entry["opts"] = [escape_lt_in_math(str(o)) for o in opts]
        ans = e.get("ans")
        idx = None
        if isinstance(ans, int):
            idx = ans
        elif isinstance(ans, str):
            a = ans.strip().upper()
            if a in "ABCD" and len(a) == 1:
                idx = "ABCD".index(a)
            elif a.isdigit() and int(a) < len(opts):
                idx = int(a)
        if idx is None or idx >= len(opts):
            return None
        entry["ans"] = idx
    elif ty == "judge":
        a = str(e.get("ans") or "").strip()
        if a in ("√", "T", "对", "对错", "true", "Y"):
            entry["ans"] = "√"
        elif a in ("×", "X", "F", "错", "false", "N"):
            entry["ans"] = "×"
        else:
            return None
    elif ty == "blank":
        entry["ans"] = escape_lt_in_math(str(e.get("ans") or "").strip())
        if not entry["ans"]:
            return None
    else:
        sc = e.get("score") or TY_SCORE[ty]
        try:
            sc = int(sc)
        except Exception:
            sc = TY_SCORE[ty]
        entry["score"] = sc
    return entry

def main():
    banks = load_current()
    seen = {}
    dup_count = 0
    sol_upgraded = 0
    for ty in TYS:
        for q in banks[ty]:
            k = norm(q.get("q"))
            if k:
                seen[k] = q
    batch_files = sorted(glob.glob(os.path.join(BATCH_DIR, "*.json")))
    report = []
    for bf in batch_files:
        name = os.path.basename(bf)
        try:
            with open(bf, encoding="utf-8-sig") as f:
                arr = json.load(f)
        except Exception as ex:
            report.append(f"[跳过] {name}: JSON 解析失败 {ex}")
            continue
        if not isinstance(arr, list):
            report.append(f"[跳过] {name}: 不是数组")
            continue
        ok = bad = dup = 0
        for e in arr:
            src_default = "学习指导" if name.startswith("guide") else ("课本复习题" if name.startswith("keben") else "期末试卷")
            c = clean_entry(e, src_default)
            if c is None:
                bad += 1
                continue
            k = norm(c["q"])
            if k and k in seen:
                # 重复题：保留已入库条目，但若新解答明显更完整则升级 sol（如书版解答覆盖自写解答）
                old = seen[k]
                if len(c.get("sol", "")) > len(old.get("sol", "")) * 1.2:
                    old["sol"] = c["sol"]
                    sol_upgraded += 1
                dup += 1
                dup_count += 1
                continue
            banks[c["ty"]].append(c)
            if k:
                seen[k] = c
            ok += 1
        report.append(f"[{name}] 收录 {ok} · 重复跳过 {dup} · 无效跳过 {bad}")

    # 分配 id：按现有最大序号顺延
    for ty in TYS:
        pref = TY_PREFIX[ty]
        mx = 0
        for q in banks[ty]:
            m = re.match(rf"^{pref}(\d+)$", str(q.get("id") or ""))
            if m:
                mx = max(mx, int(m.group(1)))
        n = mx
        for q in banks[ty]:
            if not q.get("id"):
                n += 1
                q["id"] = f"{pref}{n}"

    # 重建 JS 文件（json.dumps 保证转义正确，双引号字符串是合法 JS）
    def js_section(ty, items):
        out = [f"window.XDBANK_OBJ.{ty} = ["]
        for q in items:
            out.append(json.dumps(q, ensure_ascii=False) + ",")
        out.append("];")
        return "\n".join(out)

    head_t = """/* ============================================================
   XD_learn 题库 · 客观题部分（判断 / 选择 / 填空）
   由 tools/merge_bank.py 自动生成，请勿手工拼接编辑
   ============================================================ */
window.XDBANK_OBJ = window.XDBANK_OBJ || {};
"""
    head_s = """/* ============================================================
   XD_learn 题库 · 主观题部分（解答 / 证明）
   由 tools/merge_bank.py 自动生成，请勿手工拼接编辑
   ============================================================ */
window.XDBANK_OBJ = window.XDBANK_OBJ || {};
"""
    with open(r"D:\Web\XD_learn\assets\exam\theory_bank.js", "w", encoding="utf-8", newline="\n") as f:
        f.write(head_t)
        for ty in ("judge", "choice", "blank"):
            f.write(js_section(ty, banks[ty]) + "\n\n")
    with open(r"D:\Web\XD_learn\assets\exam\solve_bank.js", "w", encoding="utf-8", newline="\n") as f:
        f.write(head_s)
        for ty in ("solve", "proof"):
            f.write(js_section(ty, banks[ty]) + "\n\n")

    total = sum(len(banks[ty]) for ty in TYS)
    print("\n".join(report))
    print(f"\n批内重复跳过合计: {dup_count} · sol 择优升级: {sol_upgraded}")
    print("最终题库:", " ".join(f"{ty}:{len(banks[ty])}" for ty in TYS), f"TOTAL {total}")

if __name__ == "__main__":
    main()
