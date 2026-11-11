# XD_learn · 线性代数知识库

纯静态、零依赖构建的线性代数学习站点（HTML / CSS / 原生 JS），参照 [C_learn](https://github.com/YJH9999/C_learn) 的架构复刻，UI 换用 iOS 简洁风 + 数学衬线标题。

## ✨ 功能

| 功能 | 说明 |
|---|---|
| 📖 四章知识体系 | 按《线性代数（第 2 版）》目录：矩阵和线性方程组 / 向量 / 线性变换与矩阵相似 / 二次型，共 34 个章节页 |
| 🧮 公式渲染 | KaTeX 本地化（`assets/katex/`），1100+ 公式离线渲染，无需网络 |
| 🔍 全文搜索 | Ctrl K 搜索所有标题与正文摘要，跳转后关键词自动标黄 |
| ⭐ 收藏 | 标题旁星标收藏薄弱知识点，侧栏集中复习 |
| ⚡ 冲刺模式 | 考前筛选：只看易错点 / 只看高频考点 / 只看例题 |
| 📝 备考中心 | club_exam 式组卷：**1214 题**五题型题库（判断 17 / 选择 160 / 填空 210 / 计算 615 / 证明 212，默认题量 = 江南大学期末卷结构），含**同济版《线性代数》习题一～六全六章 237 题**逐页转录（`src="教材习题"`，源题号见 `srcNo`）、快速套卷预设、章节/来源筛选、客观题自动判分、主观题对照参考答案自评、错题本（localStorage 持久化）、四章考点速览 |
| 🌗 明暗主题 | 浅色 / 深色一键切换，跟随记忆 |
| 📱 响应式 | 桌面三栏布局，移动端抽屉目录 + 底部工具栏 |

## 📂 目录结构

```
XD_learn/
├── index.html            # 知识库主页（SPA）
├── exam.html             # 备考中心
├── assets/
│   ├── style.css         # iOS 简洁风主题
│   ├── exam.css          # 备考中心样式
│   ├── app.js            # 知识库逻辑（懒加载/搜索/收藏/冲刺）
│   ├── exam_app.js       # 组卷与判分逻辑
│   ├── manifest.js       # 章节清单（tools/build_index.py 生成）
│   ├── search-index.js   # 搜索索引（同上生成）
│   ├── content/          # 34 个章节内容片段
│   ├── exam/             # 题库（theory_bank.js / review_data.js）
│   ├── katex/            # KaTeX 0.16.11 本地化
│   └── fonts/            # Noto Sans SC / JetBrains Mono 子集
└── tools/build_index.py  # 索引构建脚本
```

## 🚀 本地运行

正文按章节分文件加载，**必须通过 HTTP 访问**（直接双击 index.html 无法加载）：

```bash
cd XD_learn
python -m http.server 8000
# 打开 http://localhost:8000
```

## 📦 修改内容后重建索引

```bash
python tools/build_index.py
```

## 📚 内容来源

- 学校教材《线性代数（第 2 版）》章节体系
- 《线性代数学习指导》典型例题（行列式 / 矩阵 / 向量 / 线性方程组 / 特征值 / 二次型）
- 知乎知识点整理与公开资料
- 全部例题解答均经过独立验算

## 🔗 相关

- C 语言版：[YJH9999/C_learn](https://github.com/YJH9999/C_learn)
