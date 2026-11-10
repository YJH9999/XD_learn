# -*- coding: utf-8 -*-
"""构建 keben_k2.json：课本复习题2/3/4 转录。LaTeX 用原始字符串，json.dump 负责转义。"""
import json

B = r"\underline{\hspace{2em}}"  # 填空空位

def fml(expr):
    return '<div class="fml">$$' + expr + '$$</div>'

items = []

def add(srcNo, ty, ch, kp, diff, q, ans, sol, opts=None):
    if isinstance(sol, list) and isinstance(opts, str):  # 调用时 opts/sol 顺序颠倒的自动纠正
        sol, opts = opts, sol
    d = {"src": "课本复习题", "srcNo": srcNo, "ty": ty, "ch": ch, "kp": kp,
         "diff": diff, "score": 8, "q": q}
    if opts is not None:
        d["opts"] = opts
    d["ans"] = ans
    d["sol"] = sol
    items.append(d)

# ============ 复习题2 证明题 (p008) ch2 ============

add("复习题2证明3", "proof", 2, "向量组秩的证明", 3,
    r"已知向量组（I）\(\alpha_1,\alpha_2,\alpha_3\)；（II）\(\alpha_1,\alpha_2,\alpha_3,\alpha_4\)；（III）\(\alpha_1,\alpha_2,\alpha_3,\alpha_5-\alpha_4\)。如果各向量组的秩分别为 \(r(\mathrm{I})=r(\mathrm{II})=3\)，\(r(\mathrm{III})=4\)，证明：向量组 \(\alpha_1,\alpha_2,\alpha_3,\alpha_5-\alpha_4\) 的秩为 4。",
    "向量组 \\(\\alpha_1,\\alpha_2,\\alpha_3,\\alpha_5-\\alpha_4\\) 线性无关，秩为 4",
    '<p>由 \\(r(\\mathrm{I})=3\\) 知 \\(\\alpha_1,\\alpha_2,\\alpha_3\\) 线性无关；由 \\(r(\\mathrm{II})=3\\) 知 \\(\\alpha_4\\) 可由 \\(\\alpha_1,\\alpha_2,\\alpha_3\\) 线性表示，设 \\(\\alpha_4=t_1\\alpha_1+t_2\\alpha_2+t_3\\alpha_3\\)。</p>'
    '<p>设有数 \\(k_1,k_2,k_3,k_4\\) 使 \\(k_1\\alpha_1+k_2\\alpha_2+k_3\\alpha_3+k_4(\\alpha_5-\\alpha_4)=0\\)。若 \\(k_4\\neq 0\\)，则 \\(\\alpha_5\\) 可由 \\(\\alpha_1,\\alpha_2,\\alpha_3,\\alpha_4\\) 线性表示，而 \\(\\alpha_4\\) 又可由 \\(\\alpha_1,\\alpha_2,\\alpha_3\\) 表示，于是 \\(\\alpha_5\\) 可由 \\(\\alpha_1,\\alpha_2,\\alpha_3\\) 表示，从而 \\(r(\\mathrm{III})\\leq 3\\)，与 \\(r(\\mathrm{III})=4\\) 矛盾。故 \\(k_4=0\\)。</p>'
    '<p>于是 \\(k_1\\alpha_1+k_2\\alpha_2+k_3\\alpha_3=0\\)，由 \\(\\alpha_1,\\alpha_2,\\alpha_3\\) 线性无关得 \\(k_1=k_2=k_3=0\\)。所以 \\(\\alpha_1,\\alpha_2,\\alpha_3,\\alpha_5-\\alpha_4\\) 线性无关，秩为 4。</p>'
    '<p>点评：关键是利用“秩为 3 的组中第 4 个向量可由前三个表示”传递表示关系，再用秩的条件排除 \\(k_4\\neq 0\\)。</p>')

add("复习题2证明4", "proof", 2, "列向量组线性无关", 2,
    r"设 \(A\) 是 \(n\times m\) 矩阵，\(B\) 是 \(m\times n\) 矩阵，\(n&lt;m\)，若 \(AB=E\)，证明：\(B\) 的列向量组线性无关。",
    "\\(B\\) 的列向量组线性无关",
    '<p>设有 \\(x\\in\\R^n\\) 使 \\(Bx=0\\)。两边左乘 \\(A\\) 得 \\(ABx=0\\)，即 \\(Ex=0\\)，故 \\(x=0\\)。</p>'
    '<p>所以齐次方程组 \\(Bx=0\\) 只有零解，由列向量组线性无关的判定知 \\(B\\) 的 \\(n\\) 个列向量线性无关。</p>'
    '<p>点评：\\(AB=E\\) 说明 \\(B\\) 是单射的，直接把“向量组无关”转化为“方程组只有零解”。</p>')

add("复习题2证明5", "proof", 2, "格拉姆行列式判相关", 2,
    r"试证明 \(n\) 维列向量组 \(\alpha_1,\alpha_2,\cdots,\alpha_n\) 线性相关的充要条件是" + fml(r"D=\begin{vmatrix}\alpha_1^{\top}\alpha_1 & \alpha_1^{\top}\alpha_2 & \cdots & \alpha_1^{\top}\alpha_n\\ \alpha_2^{\top}\alpha_1 & \alpha_2^{\top}\alpha_2 & \cdots & \alpha_2^{\top}\alpha_n\\ \vdots & \vdots & & \vdots\\ \alpha_n^{\top}\alpha_1 & \alpha_n^{\top}\alpha_2 & \cdots & \alpha_n^{\top}\alpha_n\end{vmatrix}=0") + r"，其中 \(\alpha_i^{\top}\) 表示列向量 \(\alpha_i\) 的转置，\(i=1,2,\cdots,n\)。",
    "向量组线性相关 \\(\\Leftrightarrow D=0\\)",
    '<p>记 \\(A=(\\alpha_1,\\alpha_2,\\cdots,\\alpha_n)\\)，则 \\(D=\\det(A^{\\top}A)=\\det(A^{\\top})\\det(A)=|A|^2\\)。</p>'
    '<p>而 \\(n\\) 个 \\(n\\) 维向量 \\(\\alpha_1,\\cdots,\\alpha_n\\) 线性相关 \\(\\Leftrightarrow r(A)&lt;n\\Leftrightarrow|A|=0\\Leftrightarrow|A|^2=0\\)，即 \\(D=0\\)。命题得证。</p>'
    '<p>点评：\\(A^{\\top}A\\) 就是该向量组的格拉姆（Gram）矩阵，其行列式为零刻画了线性相关性。</p>')

add("复习题2证明6", "proof", 2, "循环和向量组相关性", 3,
    r"已知向量组 \(\alpha_1,\alpha_2,\cdots,\alpha_r\)（\(r&gt;2\)）线性无关，设 \(\beta_1=\alpha_1+\alpha_2,\ \beta_2=\alpha_2+\alpha_3,\ \cdots,\ \beta_{r-1}=\alpha_{r-1}+\alpha_r,\ \beta_r=\alpha_r+\alpha_1\)，求证：当且仅当 \(r\) 为奇数时，\(\beta_1,\beta_2,\cdots,\beta_r\) 线性无关。",
    "当且仅当 \\(r\\) 为奇数时线性无关",
    '<p>设 \\(k_1\\beta_1+k_2\\beta_2+\\cdots+k_r\\beta_r=0\\)，整理得 \\((k_1+k_r)\\alpha_1+(k_1+k_2)\\alpha_2+\\cdots+(k_{r-1}+k_r)\\alpha_r=0\\)。由 \\(\\alpha_1,\\cdots,\\alpha_r\\) 线性无关得</p>'
    + fml(r"k_i+k_{i-1}=0\quad(i=1,2,\cdots,r,\ k_0:=k_r)") +
    '<p>由此依次得 \\(k_2=-k_1,\\ k_3=k_1,\\ k_4=-k_1,\\cdots\\)，即 \\(k_i=(-1)^{i+1}k_1\\)。代入 \\(k_r+k_1=0\\) 得 \\(\\big(1+(-1)^{r+1}\\big)k_1=0\\)。</p>'
    '<p>当 \\(r\\) 为奇数时 \\(1+(-1)^{r+1}=2\\)，故 \\(k_1=0\\)，从而全部 \\(k_i=0\\)，\\(\\beta_1,\\cdots,\\beta_r\\) 线性无关；当 \\(r\\) 为偶数时 \\(1+(-1)^{r+1}=0\\)，任取 \\(k_1=1\\) 即得非零解，故线性相关。</p>'
    '<p>点评：该过渡矩阵的行列式为 \\(1+(-1)^{r+1}\\)，正是“模 2 循环”结构决定相关性。</p>')

add("复习题2证明7", "proof", 2, "幂序列向量组无关", 3,
    r"设 \(A\) 是 \(n\) 阶矩阵，若存在正整数 \(k\)，使线性方程组 \(A^k x=0\) 有解向量 \(\alpha\)，且 \(A^{k-1}\alpha\neq 0\)。证明：向量组 \(\alpha,A\alpha,\cdots,A^{k-1}\alpha\) 线性无关。",
    "向量组线性无关",
    '<p>设 \\(c_0\\alpha+c_1A\\alpha+\\cdots+c_{k-1}A^{k-1}\\alpha=0\\)。用 \\(A^{k-1}\\) 左乘两边：由 \\(A^k\\alpha=0\\) 知当 \\(i\\geq 1\\) 时 \\(A^{k-1+i}\\alpha=A^{i-1}(A^k\\alpha)=0\\)，故只剩 \\(c_0A^{k-1}\\alpha=0\\)。又 \\(A^{k-1}\\alpha\\neq 0\\)，所以 \\(c_0=0\\)。</p>'
    '<p>再用 \\(A^{k-2}\\) 左乘原式，同理得 \\(c_1=0\\)；依次用 \\(A^{k-3},\\cdots,A\\) 左乘，逐个得 \\(c_2=\\cdots=c_{k-1}=0\\)。</p>'
    '<p>故只有零解，向量组 \\(\\alpha,A\\alpha,\\cdots,A^{k-1}\\alpha\\) 线性无关。</p>'
    '<p>点评：逐次用 \\(A\\) 的幂左乘，把系数一个一个“剥离”出来，这是处理幂序列无关性的标准手法。</p>')

# ============ 复习题3 选择题 (p009, p010) ch3 ============

add("复习题3选择1", "choice", 3, "相似矩阵的性质", 2,
    r"设 \(A,B\) 均为可逆矩阵，若 \(A\) 与 \(B\) 相似，则下列结论错误的是（" + B + r"）。",
    "2",
    ['\\(A\\) \\(A^{\\top}\\) 与 \\(B^{\\top}\\) 相似',
     '\\(A\\) \\(A^{-1}\\) 与 \\(B^{-1}\\) 相似',
     '\\(A\\) \\(A+A^{\\top}\\) 与 \\(B+B^{\\top}\\) 相似',
     '\\(A\\) \\(A-A^{-1}\\) 与 \\(B-B^{-1}\\) 相似'],
    '<p>设 \\(B=P^{-1}AP\\)。则 \\(B^{\\top}=P^{\\top}A^{\\top}(P^{\\top})^{-1}\\)，故 \\(A^{\\top}\\sim B^{\\top}\\)，A 正确；\\(B^{-1}=PA^{-1}P^{-1}\\)，故 \\(A^{-1}\\sim B^{-1}\\)，B 正确；对任意多项式（或有理式）\\(f\\) 有 \\(f(B)=P^{-1}f(A)P\\)，取 \\(f(x)=x-x^{-1}\\) 知 D 正确。</p>'
    '<p>而 \\(B+B^{\\top}=P^{-1}AP+P^{\\top}A^{\\top}(P^{\\top})^{-1}\\)，一般不能写成 \\(P^{-1}(A+A^{\\top})P\\) 的形式，故 \\(A+A^{\\top}\\) 与 \\(B+B^{\\top}\\) 不一定相似，C 错误。</p>'
    '<p>点评：相似对多项式、转置、逆都封闭，但对“与转置之和”这种不通过同一 \\(P\\) 的运算无保持性。</p>')

add("复习题3选择2", "choice", 3, "可对角化充要条件", 1,
    r"\(n\) 阶矩阵 \(A\) 具有 \(n\) 个不同的特征值是 \(A\) 与对角矩阵相似的（" + B + r"）。",
    "1",
    ['\\(A\\) 充要条件', '\\(A\\) 充分非必要条件', '\\(A\\) 必要非充分条件', '\\(A\\) 既非充分也非必要条件'],
    '<p>若 \\(A\\) 有 \\(n\\) 个互不相同的特征值，则属于不同特征值的特征向量线性无关，故 \\(A\\) 有 \\(n\\) 个线性无关的特征向量，可对角化，条件充分。</p>'
    '<p>反之，可对角化的矩阵未必有 \\(n\\) 个不同特征值，例如 \\(A=E\\) 特征值全为 1 仍可对角化，故不必要。</p>'
    '<p>所以是充分非必要条件，选 B。</p>')

add("复习题3选择3", "choice", 3, "相似对角化条件", 1,
    r"若 \(n\) 阶方阵 \(A\) 相似于对角阵，则（" + B + r"）。",
    "3",
    ['\\(A\\) \\(A\\) 为可逆矩阵', '\\(A\\) \\(A\\) 为实对称阵', '\\(A\\) \\(A\\) 有 \\(n\\) 个不同的特征值', '\\(A\\) \\(A\\) 有 \\(n\\) 个线性无关的特征向量'],
    '<p>\\(A\\) 可对角化的充要条件是 \\(A\\) 有 \\(n\\) 个线性无关的特征向量，故 D 正确。</p>'
    '<p>可对角化不能保证可逆（如特征值含 0）、不能保证是实对称阵、也不能保证有 \\(n\\) 个不同特征值（如 \\(E\\)），故 A、B、C 均不对。选 D。</p>')

add("复习题3选择4", "choice", 3, "正交矩阵的性质", 1,
    r"设 \(A\) 是正交矩阵，下列关于 \(A\) 的说法中不正确的是（" + B + r"）。",
    "0",
    ['\\(A\\) \\(|A|=1\\)', '\\(A\\) \\(A\\) 可逆', '\\(A\\) \\(A\\) 的列向量相互正交', '\\(A\\) \\(A\\) 的行向量相互正交'],
    '<p>由 \\(A^{\\top}A=E\\) 得 \\(|A|^2=1\\)，即 \\(|A|=\\pm 1\\)，故“\\(|A|=1\\)”不一定成立，例如 \\(A=\\begin{pmatrix}0&1\\\\1&0\\end{pmatrix}\\) 的行列式为 \\(-1\\)，A 不正确。</p>'
    '<p>\\(|A|=\\pm 1\\neq 0\\) 故 \\(A\\) 可逆，B 正确；\\(A^{\\top}A=E\\) 与 \\(AA^{\\top}=E\\) 分别说明列、行向量组是标准正交组，C、D 正确。选 A。</p>')

add("复习题3选择5", "choice", 3, "正交矩阵的判定", 1,
    r"下列矩阵中不是正交矩阵的是（" + B + r"）。",
    "3",
    ['\\(A\\) \\(\\begin{pmatrix}1&0\\\\0&-1\\end{pmatrix}\\)',
     '\\(A\\) \\(\\begin{pmatrix}0&-1\\\\1&0\\end{pmatrix}\\)',
     '\\(A\\) \\(\\begin{pmatrix}0&1\\\\1&0\\end{pmatrix}\\)',
     '\\(A\\) \\(\\begin{pmatrix}1&-1\\\\1&1\\end{pmatrix}\\)'],
    '<p>A、B、C 三个矩阵的行（列）向量都是长度为 1 且相互正交的向量，均满足 \\(A^{\\top}A=E\\)，是正交矩阵。</p>'
    '<p>D 的行向量 \\((1,-1)\\)、\\((1,1)\\) 的长度为 \\(\\sqrt{2}\\neq 1\\)，不满足 \\(AA^{\\top}=E\\)，故不是正交矩阵。选 D。</p>')

# ============ 复习题3 填空题 (p010) ch3 ============

add("复习题3填空1", "blank", 3, "相似矩阵行列式", 1,
    r"设三阶矩阵 \(A\) 和 \(B\) 相似，若 \(A\) 的特征值为 \(1,2,5\)，则 \(|B^{-1}|=\)" + B + r"。"+ "",
    "\\(\\dfrac{1}{10}\\)",
    '<p>相似矩阵有相同的特征值，故 \\(B\\) 的特征值也为 \\(1,2,5\\)，\\(|B|=1\\cdot 2\\cdot 5=10\\)。</p>'
    '<p>于是 \\(|B^{-1}|=\\dfrac{1}{|B|}=\\dfrac{1}{10}\\)。</p>')

add("复习题3填空2", "blank", 3, "正交变换保长度", 1,
    r"设 \(Q=\begin{pmatrix}-\dfrac{1}{\sqrt2}&-\dfrac{1}{\sqrt6}&\dfrac{1}{\sqrt3}\\ \dfrac{1}{\sqrt2}&-\dfrac{1}{\sqrt6}&\dfrac{1}{\sqrt3}\\ 0&\dfrac{2}{\sqrt6}&\dfrac{1}{\sqrt3}\end{pmatrix},\ x=\begin{pmatrix}1\\2\\2\end{pmatrix}\)，则向量 \(Qx\) 的范数 \(\|Qx\|=\)" + B + r"。"+ "",
    "3",
    '<p>逐列验证知 \\(Q\\) 的列向量是标准正交组，\\(Q\\) 为正交矩阵。正交变换保持向量长度：\\(\\|Qx\\|=\\|x\\|\\)。</p>'
    '<p>故 \\(\\|Qx\\|=\\sqrt{1^2+2^2+2^2}=\\sqrt{9}=3\\)。</p>')

add("复习题3填空3", "blank", 3, "旋转矩阵求逆", 1,
    r"已知矩阵 \(A=\begin{pmatrix}\cos\theta&-\sin\theta\\ \sin\theta&\cos\theta\end{pmatrix}\)，则 \(A^{-1}=\)" + B + r"。"+ "",
    "\\(\\begin{pmatrix}\\cos\\theta&\\sin\\theta\\\\-\\sin\\theta&\\cos\\theta\\end{pmatrix}\\)",
    '<p>\\(|A|=\\cos^2\\theta+\\sin^2\\theta=1\\neq 0\\)，故 \\(A\\) 可逆。二阶矩阵求逆：</p>'
    + fml(r"A^{-1}=\frac{1}{|A|}\begin{pmatrix}\cos\theta&\sin\theta\\ -\sin\theta&\cos\theta\end{pmatrix}=\begin{pmatrix}\cos\theta&\sin\theta\\ -\sin\theta&\cos\theta\end{pmatrix}") +
    '<p>即 \\(A^{-1}=A^{\\top}\\)，说明旋转矩阵是正交矩阵。</p>')

add("复习题3填空4", "blank", 3, "坐标变换求特征值", 2,
    r"设 \(A\) 为二阶矩阵，\(\alpha_1,\alpha_2\) 是线性无关的二维向量，若 \(A\alpha_1=0\)，\(A\alpha_2=2\alpha_1+\alpha_2\)，则 \(A\) 的特征值为" + B + r"。"+ "",
    "0 和 1",
    '<p>由 \\(A(\\alpha_1,\\alpha_2)=(A\\alpha_1,\\ A\\alpha_2)=(\\alpha_1,\\alpha_2)\\begin{pmatrix}0&2\\\\0&1\\end{pmatrix}\\)，且 \\(\\alpha_1,\\alpha_2\\) 线性无关，坐标矩阵可逆，故 \\(A\\) 相似于 \\(M=\\begin{pmatrix}0&2\\\\0&1\\end{pmatrix}\\)。</p>'
    '<p>\\(M\\) 为上三角矩阵，特征值为对角元 \\(0\\) 和 \\(1\\)，所以 \\(A\\) 的特征值为 0 和 1。</p>')

add("复习题3填空5", "blank", 3, "单位阵减秩一矩阵", 2,
    r"设 \(\alpha\) 是三维单位列向量，则矩阵 \(E-\alpha\alpha^{\top}\) 的秩为" + B + r"。"+ "",
    "2",
    '<p>\\(\\alpha\\alpha^{\\top}\\) 是秩 1 的实对称矩阵，且 \\((\\alpha\\alpha^{\\top})\\alpha=\\alpha(\\alpha^{\\top}\\alpha)=\\alpha\\)，故其特征值为 \\(1,0,0\\)（\\(\\alpha\\) 是属于 1 的特征向量）。</p>'
    '<p>于是 \\(E-\\alpha\\alpha^{\\top}\\) 的特征值为 \\(0,1,1\\)。它是对称矩阵必可对角化，秩等于非零特征值的个数，故 \\(r(E-\\alpha\\alpha^{\\top})=2\\)。</p>')

# ============ 复习题3 解答题 (p010, p011) ch3 ============

add("复习题3解答1", "solve", 3, "伴随矩阵特征值", 3,
    r"设矩阵 \(A=\begin{pmatrix}a&-1&c\\5&b&3\\1-c&0&-a\end{pmatrix}\)，其行列式 \(|A|=-1\)，又 \(A\) 的伴随矩阵 \(A^*\) 有一个特征值为 \(\lambda_0\)，对应的一个特征向量为 \(\alpha=(-1,-1,1)^{\top}\)，求 \(a,b,c\) 和 \(\lambda_0\)。",
    "\\(a=2,\\ b=-3,\\ c=2,\\ \\lambda_0=1\\)",
    '<p>由 \\(A^*\\alpha=\\lambda_0\\alpha\\)，两边左乘 \\(A\\)：\\(AA^*\\alpha=|A|E\\alpha=-\\alpha=\\lambda_0 A\\alpha\\)，即 \\(A\\alpha=-\\dfrac{1}{\\lambda_0}\\alpha\\)。记 \\(\\mu=-\\dfrac{1}{\\lambda_0}\\)，则 \\(\\alpha\\) 也是 \\(A\\) 的特征向量。</p>'
    '<p>计算：</p>'
    + fml(r"A\alpha=\begin{pmatrix}-a+1+c\\ -5-b+3\\ -(1-c)-a\end{pmatrix}=\begin{pmatrix}c-a+1\\ -b-2\\ c-a-1\end{pmatrix}=\mu\begin{pmatrix}-1\\-1\\1\end{pmatrix}") +
    '<p>比较第 1、3 个分量：\\(c-a+1=-(c-a-1)\\)，得 \\(c=a\\)；于是 \\(\\mu=c-a-1=-1\\)，\\(\\lambda_0=-\\dfrac{1}{\\mu}=1\\)；再由 \\(-b-2=-\\mu=1\\) 得 \\(b=-3\\)。</p>'
    '<p>把 \\(a=c\\) 代入行列式：</p>'
    + fml(r"|A|=\begin{vmatrix}a&-1&a\\5&-3&3\\1-a&0&-a\end{vmatrix}=3a^2+(-2a-3)+3a-3a^2=a-3=-1") +
    '<p>得 \\(a=2\\)，故 \\(a=c=2\\)。综上 \\(a=2,\\ b=-3,\\ c=2,\\ \\lambda_0=1\\)。</p>'
    '<p>点评：关键是利用 \\(AA^*=|A|E\\) 把伴随矩阵的特征值问题转回 \\(A\\) 本身。</p>')

add("复习题3解答2", "solve", 3, "逆矩阵特征向量", 2,
    r"已知向量 \(\alpha=(1,k,1)^{\top}\) 是矩阵 \(A=\begin{pmatrix}2&1&1\\1&2&1\\1&1&2\end{pmatrix}\) 的逆矩阵 \(A^{-1}\) 的特征向量，求常数 \(k\) 的值。",
    "\\(k=1\\) 或 \\(k=-2\\)",
    '<p>设 \\(A^{-1}\\alpha=\\lambda\\alpha\\)，两边左乘 \\(A\\) 得 \\(A\\alpha=\\dfrac{1}{\\lambda}\\alpha\\)，故 \\(\\alpha\\) 也是 \\(A\\) 的特征向量。</p>'
    + fml(r"A\alpha=\begin{pmatrix}2+k+1\\ 1+2k+1\\ 1+k+2\end{pmatrix}=\begin{pmatrix}k+3\\ 2k+2\\ k+3\end{pmatrix}") +
    '<p>设 \\(A\\alpha=\\mu\\alpha\\)，由第 1、3 分量自动相等，只需 \\(\\dfrac{k+3}{1}=\\dfrac{2k+2}{k}\\)（\\(k\\neq 0\\)），即 \\(k(k+3)=2k+2\\)，整理得 \\(k^2+k-2=0\\)，解得 \\(k=1\\) 或 \\(k=-2\\)。</p>'
    '<p>当 \\(k=1\\) 时 \\(A\\alpha=4\\alpha\\)，\\(\\lambda=\\dfrac14\\)；当 \\(k=-2\\) 时 \\(A\\alpha=1\\cdot\\alpha\\)，\\(\\lambda=1\\)，均满足要求。故 \\(k=1\\) 或 \\(k=-2\\)。</p>')

add("复习题3解答3", "solve", 3, "正交条件求伴随特征值", 2,
    r"设四阶矩阵 \(A\) 满足 \(|3E+A|=0\)，\(AA^{\top}=2E\)，\(|A|&lt;0\)，其中 \(E\) 是单位矩阵，求 \(A\) 的伴随矩阵 \(A^*\) 的一个特征值。",
    "\\(\\dfrac{4}{3}\\)",
    '<p>由 \\(|3E+A|=0\\) 知 \\(-3\\) 是 \\(A\\) 的一个特征值。</p>'
    '<p>由 \\(AA^{\\top}=2E\\) 取行列式：\\(|A|^2=|2E|=2^4=16\\)，又 \\(|A|&lt;0\\)，故 \\(|A|=-4\\)，\\(A\\) 可逆。</p>'
    '<p>若 \\(A\\alpha=\\lambda\\alpha\\)（\\(\\lambda=-3\\)），则 \\(A^*\\alpha=\\dfrac{|A|}{\\lambda}\\alpha\\)（由 \\(A^*=|A|A^{-1}\\)）。于是 \\(A^*\\) 的一个特征值为</p>'
    + fml(r"\frac{|A|}{\lambda}=\frac{-4}{-3}=\frac{4}{3}") +
    '<p>点评：\\(A^*=|A|A^{-1}\\) 把 \\(A\\) 的特征值直接映射为 \\(A^*\\) 的特征值。</p>')

add("复习题3解答4", "solve", 3, "矩阵方程与行列式", 3,
    r"设 \(A\) 和 \(B\) 均为三阶矩阵，\(a,b,c\) 是 \(A\) 的三个特征值，它们都不等于 \(\dfrac{1}{2}\)，且 \(A^2+2AB+A-B=E\)，求 \(\left|A^2+BA\right|\)。",
    "\\(\\dfrac{[(a-1)(b-1)(c-1)]^2\\,abc}{(2a-1)(2b-1)(2c-1)}\\)",
    '<p>把条件整理为 \\(2AB-B=E-A^2-A\\)，即 \\(B(2A-E)=E-A^2-A\\)。</p>'
    '<p>因 \\(A\\) 的特征值 \\(a,b,c\\) 都不等于 \\(\\dfrac12\\)，故 \\(2a-1,2b-1,2c-1\\) 都不为零，\\(2A-E\\) 可逆，于是 \\(B=(E-A^2-A)(2A-E)^{-1}\\)。</p>'
    '<p>计算 \\(A+B\\)：</p>'
    + fml(r"A+B=\big[A(2A-E)+(E-A^2-A)\big](2A-E)^{-1}=(A^2-2A+E)(2A-E)^{-1}=(A-E)^2(2A-E)^{-1}") +
    '<p>而 \\(A^2+BA=(A+B)A\\)，取行列式：</p>'
    + fml(r"\left|A^2+BA\right|=\frac{|A-E|^2\,|A|}{|2A-E|}=\frac{[(a-1)(b-1)(c-1)]^2\,abc}{(2a-1)(2b-1)(2c-1)}") +
    '<p>点评：特征值条件 \\(a,b,c\\neq\\dfrac12\\) 恰好保证 \\(2A-E\\) 可逆，是本题化简的前提。</p>')

add("复习题3解答5", "solve", 3, "相似分解求行列式", 2,
    r"已知三阶矩阵 \(A\) 与三维向量 \(\alpha\)，使得向量组 \(\alpha,\ A\alpha,\ A^2\alpha\) 线性无关，且 \(A^3\alpha=3A\alpha-2A^2\alpha\)。<br>① 记 \(P=(\alpha,A\alpha,A^2\alpha)\)，设 \(A=PBP^{-1}\)，求 \(B\)；<br>② 计算行列式 \(|A+E|\)。",
    "\\(B=\\begin{pmatrix}0&0&0\\\\1&0&3\\\\0&1&-2\\end{pmatrix}\\)；\\(|A+E|=-4\\)",
    '<p>① 由 \\(AP=(A\\alpha,\\ A^2\\alpha,\\ A^3\\alpha)\\)，把各列用 \\(\\alpha,A\\alpha,A^2\\alpha\\) 表示：</p>'
    + fml(r"A\alpha=0\cdot\alpha+1\cdot A\alpha+0\cdot A^2\alpha,\quad A^2\alpha=0\cdot\alpha+0\cdot A\alpha+1\cdot A^2\alpha,\quad A^3\alpha=0\cdot\alpha+3A\alpha-2A^2\alpha") +
    '<p>故 \\(AP=PB\\)，其中</p>'
    + fml(r"B=\begin{pmatrix}0&0&0\\1&0&3\\0&1&-2\end{pmatrix}") +
    '<p>② 求 \\(B\\) 的特征多项式：</p>'
    + fml(r"|\lambda E-B|=\lambda\begin{vmatrix}\lambda&-3\\-1&\lambda+2\end{vmatrix}=\lambda(\lambda^2+2\lambda-3)=\lambda(\lambda-1)(\lambda+3)") +
    '<p>\\(B\\) 的特征值为 \\(0,1,-3\\)。由 \\(A=PBP^{-1}\\) 知 \\(A\\) 与 \\(B\\) 相似，特征值相同，故 \\(|A+E|=(0+1)(1+1)(-3+1)=-4\\)。</p>')

add("复习题3解答6", "solve", 3, "实对称阵正交对角化", 2,
    r"设 \(A=\begin{pmatrix}0&-1&4\\-1&3&a\\4&a&0\end{pmatrix}\)，设正交阵 \(Q\) 使得 \(Q^{\top}AQ\) 为对角阵，若 \(Q\) 的第一列为 \(\left(\dfrac{1}{\sqrt6}(1,2,1)\right)^{\top}\)，求 \(a,Q\)。",
    "\\(a=-1\\)；\\(Q=\\left(\\dfrac{1}{\\sqrt6}(1,2,1)^{\\top},\\dfrac{1}{\\sqrt3}(1,-1,1)^{\\top},\\dfrac{1}{\\sqrt2}(1,0,-1)^{\\top}\\right)\\)，\\(Q^{\\top}AQ=\\mathrm{diag}(2,5,-4)\\)",
    '<p>记 \\(\\xi_1=\\dfrac{1}{\\sqrt6}(1,2,1)^{\\top}\\)，则 \\(A\\xi_1=\\lambda_1\\xi_1\\)。比较第 1 个分量：\\(0\\cdot 1-1\\cdot 2+4\\cdot 1=2=\\lambda_1\\)；比较第 2 个分量：\\(-1+6+a=2\\lambda_1=4\\)，得 \\(a=-1\\)。验证第 3 个分量：\\(4-2=2\\) 也吻合。</p>'
    '<p>此时 \\(A=\\begin{pmatrix}0&-1&4\\\\-1&3&-1\\\\4&-1&0\\end{pmatrix}\\)，特征多项式 \\(|\\lambda E-A|=-(\\lambda-2)(\\lambda-5)(\\lambda+4)\\)，特征值 \\(2,5,-4\\)。</p>'
    '<p>解 \\((A-5E)x=0\\) 得 \\(\\xi_2=(1,-1,1)^{\\top}\\)；解 \\((A+4E)x=0\\) 得 \\(\\xi_3=(1,0,-1)^{\\top}\\)。三者实对称阵不同特征值的特征向量，两两正交，单位化后得</p>'
    + fml(r"Q=\begin{pmatrix}\dfrac{1}{\sqrt6}&\dfrac{1}{\sqrt3}&\dfrac{1}{\sqrt2}\\[1mm]\dfrac{2}{\sqrt6}&-\dfrac{1}{\sqrt3}&0\\[1mm]\dfrac{1}{\sqrt6}&\dfrac{1}{\sqrt3}&-\dfrac{1}{\sqrt2}\end{pmatrix},\qquad Q^{\top}AQ=\mathrm{diag}(2,5,-4)"))

add("复习题3解答7", "solve", 3, "相似求参数与对角化", 3,
    r"设矩阵 \(A=\begin{pmatrix}0&2&-3\\-1&3&-3\\1&-2&a\end{pmatrix}\) 相似于矩阵 \(B=\begin{pmatrix}1&-2&0\\0&b&0\\0&3&1\end{pmatrix}\)。<br>① 求 \(a,b\) 的值；<br>② 求可逆矩阵 \(P\)，使 \(P^{-1}AP\) 为对角阵。",
    "\\(a=4,\\ b=5\\)；\\(P=(2,1,0)^{\\top}\\) 组合见解析，\\(P^{-1}AP=\\mathrm{diag}(1,1,5)\\)",
    '<p>① 相似矩阵有相同的特征多项式。\\(B\\) 按分块结构其特征多项式为 \\((1-\\lambda)^2(b-\\lambda)\\)；\\(A\\) 的特征多项式为 \\(-\\lambda^3+(a+3)\\lambda^2-(3a-1)\\lambda+2a-3\\)。比较 \\(-\\lambda^3+(b+2)\\lambda^2-(2b+1)\\lambda+b\\) 的系数：</p>'
    + fml(r"a+3=b+2,\quad 3a-1=2b+1,\quad 2a-3=b\ \Rightarrow\ a=4,\ b=5") +
    '<p>② \\(A\\) 的特征值为 \\(1,1,5\\)。解 \\((A-E)x=0\\)：\\(-x_1+2x_2-3x_3=0\\)，得两个线性无关的特征向量 \\(\\xi_1=(2,1,0)^{\\top}\\)，\\(\\xi_2=(-3,0,1)^{\\top}\\)；解 \\((A-5E)x=0\\) 得 \\(\\xi_3=(-1,-1,1)^{\\top}\\)。</p>'
    + fml(r"P=\begin{pmatrix}2&-3&-1\\1&0&-1\\0&1&1\end{pmatrix},\qquad P^{-1}AP=\mathrm{diag}(1,1,5)"))

add("复习题3解答8", "solve", 3, "矩阵高次幂计算", 3,
    r"已知矩阵 \(A=\begin{pmatrix}0&-1&1\\2&-3&0\\0&0&0\end{pmatrix}\)。<br>① 求 \(A^{99}\)；<br>② 设三阶矩阵 \(B=(\alpha_1,\alpha_2,\alpha_3)\) 满足 \(B^2=BA\)，记 \(B^{100}=(\beta_1,\beta_2,\beta_3)\)，将 \(\beta_1,\beta_2,\beta_3\) 分别表示成 \(\alpha_1,\alpha_2,\alpha_3\) 的线性组合。",
    "\\(A^{99}=\\begin{pmatrix}2^{99}-2&1-2^{99}&2-2^{98}\\\\2^{100}-2&1-2^{100}&2-2^{99}\\\\0&0&0\\end{pmatrix}\\)；\\(\\beta_1=(2^{99}-2)\\alpha_1+(2^{100}-2)\\alpha_2\\)，\\(\\beta_2=(1-2^{99})\\alpha_1+(1-2^{100})\\alpha_2\\)，\\(\\beta_3=(2-2^{98})\\alpha_1+(2-2^{99})\\alpha_2\\)",
    '<p>① \\(A\\) 的特征多项式 \\(|\\lambda E-A|=-\\lambda(\\lambda+1)(\\lambda+2)\\)，特征值 \\(0,-1,-2\\)，互异故可对角化。分别解得特征向量 \\(\\xi_0=(3,2,2)^{\\top}\\)，\\(\\xi_1=(1,1,0)^{\\top}\\)，\\(\\xi_2=(1,2,0)^{\\top}\\)。记 \\(P=(\\xi_0,\\xi_1,\\xi_2)\\)，可验证 \\(P^{-1}=\\dfrac12\\begin{pmatrix}0&0&1\\\\4&-2&-4\\\\-2&2&1\\end{pmatrix}\\)，且</p>'
    + fml(r"A=P\,\mathrm{diag}(0,-1,-2)\,P^{-1}\ \Rightarrow\ A^{99}=P\,\mathrm{diag}(0,(-1)^{99},(-2)^{99})\,P^{-1}") +
    '<p>计算 \\(P\\,\\mathrm{diag}(0,-1,-2^{99})\\) 再右乘 \\(P^{-1}\\)，得</p>'
    + fml(r"A^{99}=\begin{pmatrix}2^{99}-2&1-2^{99}&2-2^{98}\\2^{100}-2&1-2^{100}&2-2^{99}\\0&0&0\end{pmatrix}") +
    '<p>② 由 \\(B^2=BA\\) 归纳可证 \\(B^n=BA^{n-1}\\)：\\(B^{m+1}=B\\cdot B^m=B(BA^{m-1})=B^2A^{m-1}=(BA)A^{m-1}=BA^m\\)。故 \\(B^{100}=BA^{99}\\)。</p>'
    '<p>于是 \\(\\beta_j=B\\cdot(A^{99}\\text{ 的第 }j\\text{ 列})\\)，即 \\(A^{99}\\) 第 \\(j\\) 列的三个分量就是 \\(\\beta_j\\) 关于 \\(\\alpha_1,\\alpha_2,\\alpha_3\\) 的组合系数：</p>'
    + fml(r"\beta_1=(2^{99}-2)\alpha_1+(2^{100}-2)\alpha_2,\quad \beta_2=(1-2^{99})\alpha_1+(1-2^{100})\alpha_2,\quad \beta_3=(2-2^{98})\alpha_1+(2-2^{99})\alpha_2"))

add("复习题3解答9", "solve", 3, "抽象映射求矩阵", 2,
    r"设矩阵 \(A\) 满足：对任意 \(x_1,x_2,x_3\) 均有 \(A\begin{pmatrix}x_1\\x_2\\x_3\end{pmatrix}=\begin{pmatrix}x_1+x_2+x_3\\2x_1-x_2+x_3\\x_2-x_3\end{pmatrix}\)。<br>① 求 \(A\)；<br>② 求可逆矩阵 \(P\) 及对角矩阵 \(\Lambda\)，使得 \(P^{-1}AP=\Lambda\)。",
    "\\(A=\\begin{pmatrix}1&1&1\\\\2&-1&1\\\\0&1&-1\\end{pmatrix}\\)；\\(P=\\begin{pmatrix}4&1&0\\\\3&0&1\\\\1&-2&-1\\end{pmatrix}\\)，\\(\\Lambda=\\mathrm{diag}(2,-1,-2)\\)",
    '<p>① 分别取 \\(x=(1,0,0)^{\\top},(0,1,0)^{\\top},(0,0,1)^{\\top}\\)，得 \\(A\\) 的三个列向量：</p>'
    + fml(r"A=\begin{pmatrix}1&1&1\\2&-1&1\\0&1&-1\end{pmatrix}") +
    '<p>② 特征多项式 \\(|\\lambda E-A|=(\\lambda-2)(\\lambda+1)(\\lambda+2)\\)，特征值 \\(2,-1,-2\\)。分别解 \\((A-\\lambda E)x=0\\) 得特征向量 \\(\\xi_1=(4,3,1)^{\\top}\\)，\\(\\xi_2=(1,0,-2)^{\\top}\\)，\\(\\xi_3=(0,1,-1)^{\\top}\\)。</p>'
    + fml(r"P=\begin{pmatrix}4&1&0\\3&0&1\\1&-2&-1\end{pmatrix},\qquad P^{-1}AP=\Lambda=\mathrm{diag}(2,-1,-2)"))

add("复习题3解答10", "solve", 3, "求矩阵幂的对角元", 2,
    r"已知矩阵 \(A=\begin{pmatrix}2&0&0\\1&3&1\\-1&1&3\end{pmatrix}\)，\(A^{10}=\begin{pmatrix}b_{11}&b_{12}&b_{13}\\b_{21}&b_{22}&b_{23}\\b_{31}&b_{32}&b_{33}\end{pmatrix}\)，求 \(b_{22}\)。",
    "\\(b_{22}=2^9+2^{19}=524800\\)",
    '<p>特征多项式 \\(|\\lambda E-A|=(2-\\lambda)[(3-\\lambda)^2-1]=(2-\\lambda)^2(4-\\lambda)\\)，特征值 \\(2,2,4\\)。</p>'
    '<p>解 \\((A-2E)x=0\\)：\\(x_1+x_2+x_3=0\\)，得 \\(\\xi_1=(-1,1,0)^{\\top},\\ \\xi_2=(-1,0,1)^{\\top}\\)；解 \\((A-4E)x=0\\) 得 \\(\\xi_3=(0,1,1)^{\\top}\\)。记 \\(P=(\\xi_1,\\xi_2,\\xi_3)\\)，则 \\(P^{-1}=\\dfrac12\\begin{pmatrix}-1&1&-1\\\\-1&-1&1\\\\1&1&1\\end{pmatrix}\\)，且</p>'
    + fml(r"A^{10}=P\,\mathrm{diag}(2^{10},2^{10},4^{10})\,P^{-1}") +
    '<p>\\((A^{10})_{22}\\) 等于 \\(P\\,\\mathrm{diag}(2^{10},2^{10},4^{10})\\) 的第 2 行 \\((2^{10},0,4^{10})\\) 与 \\(P^{-1}\\) 第 2 列 \\(\\dfrac12(1,-1,1)\\) 的内积：</p>'
    + fml(r"b_{22}=\frac{2^{10}+4^{10}}{2}=2^9+2^{19}=512+524288=524800"))

add("复习题3解答11", "solve", 3, "秩一矩阵对角化", 3,
    r"设 \(n\) 阶矩阵 \(A=\alpha\beta^{\top}\)，其中 \(\alpha,\beta\) 均为 \(n\) 维非零向量，且 \(\alpha=(a_1,a_2,\cdots,a_n)^{\top}\)，\(\beta=(b_1,b_2,\cdots,b_n)^{\top}\)。<br>① 证明：\(A^2=cA\)，其中 \(c=\alpha^{\top}\beta\)；<br>② 求 \(A\) 的特征值和特征向量，并判断矩阵 \(A\) 是否可以相似对角化。",
    "特征值为 \\(c=\\alpha^{\\top}\\beta\\) 与 \\(0\\)（\\(n-1\\) 重）；\\(c\\neq 0\\) 时可对角化，\\(c=0\\) 时不可",
    '<p>① \\(A^2=\\alpha\\beta^{\\top}\\alpha\\beta^{\\top}=\\alpha(\\beta^{\\top}\\alpha)\\beta^{\\top}=(\\alpha^{\\top}\\beta)\\alpha\\beta^{\\top}=cA\\)（数 \\(\\beta^{\\top}\\alpha=\\alpha^{\\top}\\beta=c\\)）。</p>'
    '<p>② 因 \\(\\alpha,\\beta\\neq 0\\)，\\(A\\neq 0\\) 且 \\(r(A)=1\\)，故 0 至少是 \\(n-1\\) 重特征值；又 \\(\\mathrm{tr}(A)=\\sum a_ib_i=c\\)，故特征值为 \\(c\\)（单根）与 \\(0\\)（\\(n-1\\) 重）。</p>'
    '<p>属于 0 的特征向量是 \\(\\beta^{\\top}x=0\\) 的非零解，共 \\(n-1\\) 个线性无关；当 \\(c\\neq 0\\) 时由 ① 知 \\(A\\alpha=c\\alpha\\)，故 \\(\\alpha\\) 是属于 \\(c\\) 的特征向量，共 \\(n\\) 个线性无关的特征向量，\\(A\\) 可相似对角化；当 \\(c=0\\) 时特征值全为 0 且 \\(A^2=0\\)，线性无关特征向量最多 \\(n-1\\) 个，\\(A\\) 不可相似对角化。</p>'
    '<p>点评：秩 1 矩阵的特征值结构由迹与秩共同决定，“\\(c=\\mathrm{tr}(A)\\)”是核心。</p>')

add("复习题3解答12", "solve", 3, "解结构与特征值", 3,
    r"设三阶矩阵 \(A=(\alpha_1,\alpha_2,\alpha_3)\) 有 3 个不同的特征值，且 \(\alpha_3=\alpha_1+2\alpha_2\)。<br>① 证明：\(r(A)=2\)；<br>② 若 \(\beta=\alpha_1+\alpha_2+\alpha_3\)，求方程组 \(Ax=\beta\) 的通解。",
    "\\(x=(2,3,0)^{\\top}+k(1,2,-1)^{\\top}\\)，\\(k\\) 为任意常数",
    '<p>① 由 \\(\\alpha_3=\\alpha_1+2\\alpha_2\\) 知 \\(A\\) 的列向量线性相关，\\(|A|=0\\)，故 0 是 \\(A\\) 的特征值。又 \\(A\\) 有 3 个互异特征值，0 是单特征值，属于它的线性无关特征向量只有 1 个，即 \\(Ax=0\\) 的基础解系含 1 个向量，于是 \\(r(A)=3-1=2\\)。</p>'
    '<p>② \\(\\beta=\\alpha_1+\\alpha_2+\\alpha_3=\\alpha_1+\\alpha_2+(\\alpha_1+2\\alpha_2)=2\\alpha_1+3\\alpha_2+0\\cdot\\alpha_3\\)，故 \\(x_p=(2,3,0)^{\\top}\\) 满足 \\(Ax_p=\\beta\\)。</p>'
    '<p>由 \\(\\alpha_1+2\\alpha_2-\\alpha_3=0\\) 知 \\(\\xi=(1,2,-1)^{\\top}\\) 是 \\(Ax=0\\) 的解，且由 ① 它就是基础解系。故通解为</p>'
    + fml(r"x=(2,3,0)^{\top}+k(1,2,-1)^{\top}\quad(k\ \text{为任意常数})"))

add("复习题3解答13", "solve", 3, "相似变换矩阵构造", 2,
    r"设 \(A\) 为 2 阶矩阵，\(P=(\alpha,A\alpha)\)，\(\alpha\) 是非零向量且不是 \(A\) 的特征向量。<br>① 证明：矩阵 \(P\) 可逆；<br>② 若 \(A^2\alpha+A\alpha-6\alpha=0\)，求 \(P^{-1}AP\) 并判断 \(A\) 是否相似于对角矩阵。",
    "\\(P^{-1}AP=\\begin{pmatrix}0&6\\\\1&-1\\end{pmatrix}\\)；\\(A\\) 可相似对角化",
    '<p>① 若 \\(P\\) 不可逆，则 \\(\\alpha,A\\alpha\\) 线性相关，即存在数 \\(k\\) 使 \\(A\\alpha=k\\alpha\\)，与“\\(\\alpha\\) 不是 \\(A\\) 的特征向量”矛盾，故 \\(P\\) 可逆。</p>'
    '<p>② 由 \\(A^2\\alpha=-A\\alpha+6\\alpha\\)，</p>'
    + fml(r"AP=(A\alpha,\ A^2\alpha)=(\alpha,\ A\alpha)\begin{pmatrix}0&6\\1&-1\end{pmatrix}=P\begin{pmatrix}0&6\\1&-1\end{pmatrix}") +
    '<p>故 \\(P^{-1}AP=\\begin{pmatrix}0&6\\\\1&-1\\end{pmatrix}=M\\)。\\(|\\lambda E-M|=\\lambda^2+\\lambda-6=(\\lambda-2)(\\lambda+3)\\)，特征值 \\(2,-3\\) 互异，\\(M\\) 可对角化；而 \\(A\\) 与 \\(M\\) 相似，故 \\(A\\) 也相似于对角矩阵。</p>')

# ============ 复习题3 证明题 (p012) ch3 ============

add("复习题3证明1", "proof", 3, "AB与BA特征值", 2,
    r"设 \(A\) 和 \(B\) 均为 \(n\) 阶矩阵，证明：\(AB\) 和 \(BA\) 有相同的特征值。",
    "\\(AB\\) 与 \\(BA\\) 有相同的特征值",
    '<p>先证非零特征值相同。设 \\(\\lambda\\neq 0\\) 是 \\(AB\\) 的特征值，即存在 \\(x\\neq 0\\) 使 \\(ABx=\\lambda x\\)。令 \\(y=Bx\\)，则 \\(y\\neq 0\\)（否则 \\(\\lambda x=ABx=0\\)，矛盾），且 \\(BAy=BA(Bx)=B(ABx)=\\lambda Bx=\\lambda y\\)，故 \\(\\lambda\\) 也是 \\(BA\\) 的特征值。由对称性，反向亦然。</p>'
    '<p>再证零特征值：\\(0\\) 是 \\(AB\\) 的特征值 \\(\\Leftrightarrow|AB|=0\\Leftrightarrow|A||B|=0\\Leftrightarrow|BA|=0\\Leftrightarrow 0\\) 是 \\(BA\\) 的特征值。</p>'
    '<p>综上，\\(AB\\) 与 \\(BA\\) 有相同的特征值。</p>')

add("复习题3证明2", "proof", 3, "正交与线性无关", 2,
    r"已知 \(n\) 维向量 \(\alpha_1,\alpha_2\) 线性无关，\(\alpha_3,\alpha_4\) 线性无关，\(\alpha_1,\alpha_2\) 分别与 \(\alpha_3,\alpha_4\) 正交，证明：向量组 \(\alpha_1,\alpha_2,\alpha_3,\alpha_4\) 线性无关。",
    "向量组线性无关",
    '<p>设 \\(k_1\\alpha_1+k_2\\alpha_2+k_3\\alpha_3+k_4\\alpha_4=0\\)。记 \\(v=k_1\\alpha_1+k_2\\alpha_2=-(k_3\\alpha_3+k_4\\alpha_4)\\)。</p>'
    '<p>由题设，\\(\\alpha_1,\\alpha_2\\) 都与 \\(\\alpha_3,\\alpha_4\\) 正交，故 \\((v,\\ k_3\\alpha_3+k_4\\alpha_4)=0\\)，即 \\((v,v)=0\\)，于是 \\(v=0\\)。</p>'
    '<p>由 \\(k_1\\alpha_1+k_2\\alpha_2=0\\) 及 \\(\\alpha_1,\\alpha_2\\) 线性无关得 \\(k_1=k_2=0\\)；同理 \\(k_3\\alpha_3+k_4\\alpha_4=0\\) 及无关性得 \\(k_3=k_4=0\\)。</p>'
    '<p>故 \\(\\alpha_1,\\alpha_2,\\alpha_3,\\alpha_4\\) 线性无关。</p>'
    '<p>点评：正交性保证两个“子空间”内的组合取内积即分离系数，这是内积空间中判无关的典型技巧。</p>')

add("复习题3证明3", "proof", 3, "特征向量线性无关", 3,
    r"设三阶矩阵 \(A\) 有三个不同的特征值 \(\lambda_1,\lambda_2,\lambda_3\)，对应的特征向量分别为 \(\alpha_1,\alpha_2,\alpha_3\)，令 \(\beta=\alpha_1+\alpha_2+\alpha_3\)，证明：\(\beta,\ A\beta,\ A^2\beta\) 线性无关。",
    "\\(\\beta,\\ A\\beta,\\ A^2\\beta\\) 线性无关",
    '<p>由 \\(A\\alpha_i=\\lambda_i\\alpha_i\\) 得 \\(A\\beta=\\lambda_1\\alpha_1+\\lambda_2\\alpha_2+\\lambda_3\\alpha_3\\)，\\(A^2\\beta=\\lambda_1^2\\alpha_1+\\lambda_2^2\\alpha_2+\\lambda_3^2\\alpha_3\\)。</p>'
    '<p>设 \\(k_1\\beta+k_2A\\beta+k_3A^2\\beta=0\\)，按 \\(\\alpha_i\\) 整理（\\(\\alpha_1,\\alpha_2,\\alpha_3\\) 线性无关）：\\(k_1+k_2\\lambda_i+k_3\\lambda_i^2=0\\)，\\(i=1,2,3\\)。</p>'
    '<p>这是关于 \\(k_1,k_2,k_3\\) 的齐次线性方程组，系数行列式为范德蒙德行列式 \\(\\prod_{i&lt;j}(\\lambda_j-\\lambda_i)\\neq 0\\)（特征值互异），故只有零解 \\(k_1=k_2=k_3=0\\)。</p>'
    '<p>所以 \\(\\beta,A\\beta,A^2\\beta\\) 线性无关。</p>')

add("复习题3证明4", "proof", 3, "不同特征值向量无关", 2,
    r"设 \(\lambda_1,\lambda_2\) 是方阵 \(A\) 的两个不同的特征值，\(\alpha_1,\cdots,\alpha_s\) 与 \(\beta_1,\cdots,\beta_t\) 分别为 \(A\) 的属于 \(\lambda_1\) 与 \(\lambda_2\) 的线性无关的特征向量，证明：向量组 \(\alpha_1,\cdots,\alpha_s,\beta_1,\cdots,\beta_t\) 线性无关。",
    "向量组线性无关",
    '<p>设 \\(k_1\\alpha_1+\\cdots+k_s\\alpha_s+l_1\\beta_1+\\cdots+l_t\\beta_t=0\\)　①。</p>'
    '<p>用 \\(A\\) 左乘：\\(\\lambda_1(k_1\\alpha_1+\\cdots+k_s\\alpha_s)+\\lambda_2(l_1\\beta_1+\\cdots+l_t\\beta_t)=0\\)　②。</p>'
    '<p>② 减去 \\(\\lambda_2\\) 倍的 ①：\\((\\lambda_1-\\lambda_2)(k_1\\alpha_1+\\cdots+k_s\\alpha_s)=0\\)。因 \\(\\lambda_1\\neq\\lambda_2\\)，得 \\(k_1\\alpha_1+\\cdots+k_s\\alpha_s=0\\)，由无关性得 \\(k_1=\\cdots=k_s=0\\)。</p>'
    '<p>代回 ① 得 \\(l_1\\beta_1+\\cdots+l_t\\beta_t=0\\)，同理 \\(l_1=\\cdots=l_t=0\\)。故向量组线性无关。</p>')

add("复习题3证明5", "proof", 3, "矩阵多项式可逆", 2,
    r"设矩阵 \(A\) 满足 \(A^2=E\)，试证明：矩阵 \(3E-A\) 可逆。",
    "\\(3E-A\\) 可逆，且 \\((3E-A)^{-1}=\\dfrac{3E+A}{8}\\)",
    '<p>直接计算：</p>'
    + fml(r"(3E-A)(3E+A)=9E-A^2=9E-E=8E") +
    '<p>即 \\((3E-A)\\cdot\\dfrac{3E+A}{8}=E\\)，由可逆矩阵的定义知 \\(3E-A\\) 可逆，且 \\((3E-A)^{-1}=\\dfrac{3E+A}{8}\\)。</p>'
    '<p>点评：不需要求特征值，构造出显式逆矩阵是最简洁的证明方式。</p>')

add("复习题3证明6", "proof", 3, "抽象矩阵对角化", 3,
    r"设三阶矩阵 \(A\) 满足 \(A\alpha_1=0\)，\(A\alpha_2=2\alpha_1+\alpha_3\)，\(A\alpha_3=-\alpha_1+3\alpha_2-\alpha_3\)，其中 \(\alpha_1,\alpha_2,\alpha_3\) 是三维向量且线性无关。试证明：\(A\) 能相似对角化，并写出对应的对角矩阵。",
    "\\(A\\) 可相似对角化，对角矩阵为 \\(\\mathrm{diag}\\left(0,\\dfrac{-1+\\sqrt{13}}{2},\\dfrac{-1-\\sqrt{13}}{2}\\right)\\)",
    '<p>记 \\(P=(\\alpha_1,\\alpha_2,\\alpha_3)\\)，由 \\(\\alpha_1,\\alpha_2,\\alpha_3\\) 线性无关知 \\(P\\) 可逆。由条件：</p>'
    + fml(r"AP=(0,\ 2\alpha_1+\alpha_3,\ -\alpha_1+3\alpha_2-\alpha_3)=P\begin{pmatrix}0&2&-1\\0&0&3\\0&1&-1\end{pmatrix}=PM") +
    '<p>故 \\(A=PMP^{-1}\\)，\\(A\\) 与 \\(M\\) 相似。求 \\(M\\) 的特征多项式：</p>'
    + fml(r"|\lambda E-M|=-\lambda\begin{vmatrix}\lambda&-3\\-1&\lambda+1\end{vmatrix}=-\lambda(\lambda^2+\lambda-3)") +
    '<p>其根为 \\(\\lambda_1=0\\)，\\(\\lambda_{2,3}=\\dfrac{-1\\pm\\sqrt{13}}{2}\\)，三个特征值互不相同，故 \\(M\\) 可对角化，从而 \\(A\\) 能相似对角化，对应的对角矩阵为</p>'
    + fml(r"\Lambda=\mathrm{diag}\left(0,\ \frac{-1+\sqrt{13}}{2},\ \frac{-1-\sqrt{13}}{2}\right)"))

add("复习题3证明7", "proof", 3, "同时对角化证明", 3,
    r"设 \(n\) 阶实矩阵 \(A,B\) 满足 \(AB=A+B\)，且存在 \(n\) 阶可逆实矩阵 \(P\)，使得 \(P^{-1}AP\) 为对角矩阵。证明：\(P^{-1}BP\) 也为对角矩阵。",
    "\\(P^{-1}BP=E+(\\Lambda-E)^{-1}\\) 为对角矩阵",
    '<p>由 \\(AB=A+B\\) 得 \\(AB-A-B+E=E\\)，即 \\((A-E)(B-E)=E\\)。故 \\(A-E\\) 可逆，且 \\(B-E=(A-E)^{-1}\\)。</p>'
    '<p>由逆矩阵的可交换性，\\((B-E)(A-E)=E\\)，展开即 \\(BA=A+B=AB\\)，故 \\(A\\) 与 \\(B\\) 可交换。</p>'
    '<p>设 \\(P^{-1}AP=\\Lambda\\)（对角阵）。由 \\((A-E)B=A\\) 得 \\(B=(A-E)^{-1}A\\)，于是</p>'
    + fml(r"P^{-1}BP=(P^{-1}(A-E)P)^{-1}\,P^{-1}AP=(\Lambda-E)^{-1}\Lambda") +
    '<p>对角矩阵的逆与积仍是对角矩阵（\\(\\Lambda-E\\) 可逆，因 \\(A-E\\) 可逆），故 \\(P^{-1}BP=\\mathrm{diag}\\left(\\dfrac{\\lambda_i}{\\lambda_i-1}\\right)\\) 为对角矩阵。</p>'
    '<p>点评：\\(AB=A+B\\) 等价于 \\((A-E)(B-E)=E\\)，是处理“同时对角化”类问题的标准入手点。</p>')

# ============ 复习题4 填空题 (p013) ch4 ============

add("复习题4填空1", "blank", 4, "二次型与矩阵", 1,
    r"矩阵 \(A=\begin{pmatrix}2&4\\4&3\end{pmatrix}\) 所对应的二次型为" + B + r"。"+ "",
    "\\(f(x_1,x_2)=2x_1^2+8x_1x_2+3x_2^2\\)",
    '<p>\\(f=x^{\\top}Ax=(x_1,x_2)\\begin{pmatrix}2&4\\\\4&3\\end{pmatrix}\\begin{pmatrix}x_1\\\\x_2\\end{pmatrix}=2x_1^2+4x_1x_2+4x_2x_1+3x_2^2\\)。</p>'
    '<p>即 \\(f(x_1,x_2)=2x_1^2+8x_1x_2+3x_2^2\\)。</p>')

add("复习题4填空2", "blank", 4, "二次型矩阵还原", 1,
    r"二次型 \(f(x,y)=(x,y)\begin{pmatrix}1&4\\2&3\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix}\) 对应的矩阵为" + B + r"。"+ "",
    "\\(\\begin{pmatrix}1&3\\\\3&3\\end{pmatrix}\\)",
    '<p>展开：\\(f=x^2+4xy+2yx+3y^2=x^2+6xy+3y^2\\)。</p>'
    '<p>二次型的矩阵须为对称矩阵，交叉项系数 6 平分到对称位置：\\(a_{12}=a_{21}=3\\)，故矩阵为 \\(\\begin{pmatrix}1&3\\\\3&3\\end{pmatrix}\\)。</p>')

add("复习题4填空3", "blank", 4, "完全平方的矩阵", 1,
    r"二次型 \(f(x,y,z)=(x+y)^2\) 的矩阵为" + B + r"。"+ "",
    "\\(\\begin{pmatrix}1&1&0\\\\1&1&0\\\\0&0&0\\end{pmatrix}\\)",
    '<p>展开 \\(f=(x+y)^2=x^2+2xy+y^2\\)（不含 \\(z\\)）。</p>'
    '<p>故矩阵为 \\(\\begin{pmatrix}1&1&0\\\\1&1&0\\\\0&0&0\\end{pmatrix}\\)。</p>')

add("复习题4填空4", "blank", 4, "含参平方型矩阵", 1,
    r"二次型 \(f(x,y,z)=(ax+by+cz)^2\) 对应的矩阵是" + B + r"。"+ "",
    "\\(\\begin{pmatrix}a^2&ab&ac\\\\ab&b^2&bc\\\\ac&bc&c^2\\end{pmatrix}\\)",
    '<p>\\(f=a^2x^2+b^2y^2+c^2z^2+2ab\\,xy+2ac\\,xz+2bc\\,yz\\)。</p>'
    '<p>交叉项系数除以 2 放到对称位置，得矩阵 \\(\\begin{pmatrix}a^2&ab&ac\\\\ab&b^2&bc\\\\ac&bc&c^2\\end{pmatrix}\\)，它恰等于 \\(u u^{\\top}\\)，其中 \\(u=(a,b,c)^{\\top}\\)。</p>')

add("复习题4填空5", "blank", 4, "规范形与惯性指数", 1,
    r"设二次型 \(f(x_1,x_2,x_3,x_4)\) 的秩为 3，负惯性指数为 1，则 \(f(x_1,x_2,x_3,x_4)\) 的规范形为" + B + r"。"+ "",
    "\\(y_1^2+y_2^2-y_3^2\\)",
    '<p>秩为 3、负惯性指数为 1，故正惯性指数 \\(=3-1=2\\)。</p>'
    '<p>规范形的平方项系数只能取 \\(\\pm 1\\)，故规范形为 \\(y_1^2+y_2^2-y_3^2\\)。</p>')

add("复习题4填空6", "blank", 4, "正惯性指数计算", 1,
    r"二次型 \(f(x,y,z)=(x+2y+3z)^2\) 的正惯性指数为" + B + r"。"+ "",
    "1",
    '<p>\\(f=(x+2y+3z)^2=u u^{\\top}\\) 型二次型（\\(u=(1,2,3)^{\\top}\\)），矩阵秩为 1 且半正定（平方和 \\(\\geq 0\\)）。</p>'
    '<p>故正惯性指数为 1，负惯性指数为 0。</p>')

# ============ 复习题4 选择题 (p013, p014) ch4 ============

add("复习题4选择1", "choice", 4, "正定矩阵的运算", 2,
    r"已知 \(A,B\) 是正定矩阵，下面哪个矩阵可能不是正定矩阵（" + B + r"）。",
    "1",
    ['\\(A\\) \\(A+B\\)', '\\(A\\) \\(AB\\)', '\\(A\\) \\(A^{-1}+B^{-1}\\)', '\\(A\\) \\(A^{*}+B^{*}\\)'],
    '<p>正定矩阵之和 \\(A+B\\) 仍对称且 \\(x^{\\top}(A+B)x&gt;0\\)，正定；正定矩阵的逆、伴随仍正定（\\(A^*=|A|A^{-1}\\)），其和也正定。</p>'
    '<p>而 \\(AB\\) 一般不是对称矩阵（\\((AB)^{\\top}=BA\\neq AB\\)），且正定矩阵的乘积未必正定，故 \\(AB\\) 可能不是正定矩阵。选 B。</p>')

add("复习题4选择2", "choice", 4, "正定的对角元条件", 2,
    r"二次型 \(f(x_1,\cdots,x_n)=x^{\top}Ax\) 的矩阵 \(A\) 的所有对角元为正是二次型 \(f(x_1,\cdots,x_n)\) 正定的（" + B + r"）。",
    "1",
    ['\\(A\\) 充分但非必要条件', '\\(A\\) 必要但非充分条件', '\\(A\\) 充要条件', '\\(A\\) 既不充分也不必要条件'],
    '<p>若 \\(f\\) 正定，则取 \\(x=e_i\\) 得 \\(a_{ii}=f(e_i)&gt;0\\)，故对角元全为正是必要的。</p>'
    '<p>反之不然，例如 \\(A=\\begin{pmatrix}1&2\\\\2&1\\end{pmatrix}\\) 对角元为正，但 \\(f=x^2+4xy+y^2\\) 在 \\((1,-1)\\) 处取值 \\(-2&lt;0\\)，不正定。</p>'
    '<p>故是必要但非充分条件，选 B。</p>')

add("复习题4选择3", "choice", 4, "合同与惯性指数", 2,
    r"下列矩阵中与矩阵 \(\begin{pmatrix}1&2&0\\2&1&0\\0&0&1\end{pmatrix}\) 合同的是（" + B + r"）。",
    "2",
    ['\\(A\\) \\(\\begin{pmatrix}1&0&0\\\\0&1&0\\\\0&0&1\\end{pmatrix}\\)',
     '\\(A\\) \\(\\begin{pmatrix}1&0&0\\\\0&-1&0\\\\0&0&-1\\end{pmatrix}\\)',
     '\\(A\\) \\(\\begin{pmatrix}1&0&0\\\\0&1&0\\\\0&0&-1\\end{pmatrix}\\)',
     '\\(A\\) \\(\\begin{pmatrix}-1&0&0\\\\0&-1&0\\\\0&0&-1\\end{pmatrix}\\)'],
    '<p>实对称矩阵合同的充要条件是有相同的正、负惯性指数。所给矩阵的 2 阶主块 \\(\\begin{pmatrix}1&2\\\\2&1\\end{pmatrix}\\) 的特征值为 \\(3,-1\\)，第三个特征值为 \\(1\\)，故其正惯性指数为 2、负惯性指数为 1。</p>'
    '<p>四个选项中只有 \\(\\mathrm{diag}(1,1,-1)\\) 的惯性指数为 \\((2,1)\\)。选 C。</p>')

add("复习题4选择4", "choice", 4, "规范形与特征值", 1,
    r"设三阶实对称矩阵 \(A\) 的特征值分别是 \(5,-1,-2\)，则二次型 \(f(x)=x^{\top}Ax\) 的规范形为（" + B + r"）。",
    "1",
    ['\\(A\\) \\(5y_1^2-y_2^2-2y_3^2\\)', '\\(A\\) \\(y_1^2-y_2^2-y_3^2\\)', '\\(A\\) \\(y_1^2+y_2^2-y_3^2\\)', '\\(A\\) \\(y_1^2-y_2^2+y_3^2\\)'],
    '<p>规范形要求平方项系数只能是 \\(1\\) 或 \\(-1\\)。特征值 \\(5,-1,-2\\) 中正的有 1 个、负的有 2 个，故正惯性指数为 1、负惯性指数为 2。</p>'
    '<p>规范形为 \\(y_1^2-y_2^2-y_3^2\\)，选 B。（A 虽然是标准形，但系数不是 \\(\\pm 1\\)，不是规范形。）</p>')

add("复习题4选择5", "choice", 4, "正交相似的性质", 2,
    r"设 \(A\) 是 \(n\) 阶矩阵，\(C\) 是 \(n\) 阶正交矩阵，若 \(B=C^{\top}AC\)，则下列结论中不成立的是（" + B + r"）。",
    "3",
    ['\\(A\\) \\(A\\) 与 \\(B\\) 有相同的秩', '\\(A\\) \\(A\\) 与 \\(B\\) 有相同的迹', '\\(A\\) \\(A\\) 与 \\(B\\) 有相同的特征值', '\\(A\\) \\(A\\) 与 \\(B\\) 有相同的特征向量'],
    '<p>因 \\(C\\) 正交，\\(C^{\\top}=C^{-1}\\)，故 \\(B=C^{-1}AC\\) 是相似变换（同时也是合同变换）。相似保持秩、迹与特征值，故 A、B、C 都成立。</p>'
    '<p>但相似矩阵的特征向量一般不同：若 \\(Ax=\\lambda x\\)，则 \\(B(C^{\\top}x)=\\lambda C^{\\top}x\\)，特征向量一般要经过 \\(C^{\\top}\\) 变换，故“有相同的特征向量”不成立。选 D。</p>')

# ============ 复习题4 解答题 (p014) ch4 ============

add("复习题4解答1", "solve", 4, "含参二次型规范形", 3,
    r"设实二次型 \(f(x_1,x_2,x_3)=(x_1-x_2+x_3)^2+(x_2+x_3)^2+(x_1+ax_3)^2\)，其中 \(a\) 是参数。<br>① 求 \(f(x_1,x_2,x_3)=0\) 的解；<br>② 求 \(f(x_1,x_2,x_3)\) 的规范形。",
    "① \\(a\\neq 2\\) 时只有零解，\\(a=2\\) 时解为 \\(k(-2,-1,1)^{\\top}\\)；② \\(a\\neq 2\\) 时规范形 \\(y_1^2+y_2^2+y_3^2\\)，\\(a=2\\) 时为 \\(y_1^2+y_2^2\\)",
    '<p>① \\(f\\) 是三个实平方之和，\\(f=0\\Leftrightarrow\\) 每个平方为零：</p>'
    + fml(r"x_1-x_2+x_3=0,\qquad x_2+x_3=0,\qquad x_1+ax_3=0") +
    '<p>由后两式 \\(x_2=-x_3\\)，\\(x_1=-ax_3\\)，代入第一式得 \\((2-a)x_3=0\\)。</p>'
    '<p>当 \\(a\\neq 2\\) 时只有零解；当 \\(a=2\\) 时解为 \\(x=k(-2,-1,1)^{\\top}\\)。</p>'
    '<p>② 展开得 \\(f=2x_1^2+2x_2^2+(2+a^2)x_3^2-2x_1x_2+2(1+a)x_1x_3\\)，矩阵</p>'
    + fml(r"A=\begin{pmatrix}2&-1&1+a\\-1&2&0\\1+a&0&2+a^2\end{pmatrix},\qquad |A|=(a-2)^2") +
    '<p>当 \\(a\\neq 2\\) 时 \\(|A|&gt;0\\)，且顺序主子式 \\(2&gt;0\\)、\\(\\begin{vmatrix}2&-1\\\\-1&2\\end{vmatrix}=3&gt;0\\)，\\(f\\) 正定，规范形为 \\(y_1^2+y_2^2+y_3^2\\)；</p>'
    '<p>当 \\(a=2\\) 时 \\(|A|=0\\)，且 \\(f\\) 是平方和恒非负（半正定），\\(r(A)=2\\)，正惯性指数为 2，规范形为 \\(y_1^2+y_2^2\\)。</p>'
    '<p>点评：平方和结构给出 \\(f\\geq 0\\)，规范形由 \\(|A|\\) 是否为零按 \\(a\\) 分情况讨论。</p>')

add("复习题4解答2", "solve", 4, "正交标准形求参数", 3,
    r"设二次型 \(f(x_1,x_2,x_3)=2x_1^2-x_2^2+ax_3^2+2x_1x_2-8x_1x_3+2x_2x_3\) 在正交变换 \(X=QY\) 下的标准形为 \(\lambda_1y_1^2+\lambda_2y_2^2\)，求 \(a\) 的值及正交矩阵 \(Q\)。",
    "\\(a=2\\)；标准形为 \\(6y_1^2-3y_2^2\\)；\\(Q=\\left(\\dfrac{1}{\\sqrt2}(1,0,-1)^{\\top},\\dfrac{1}{\\sqrt3}(1,-1,1)^{\\top},\\dfrac{1}{\\sqrt6}(1,2,1)^{\\top}\\right)\\)",
    '<p>二次型的矩阵为 \\(A=\\begin{pmatrix}2&1&-4\\\\1&-1&1\\\\-4&1&a\\end{pmatrix}\\)。标准形只有两个平方项，说明 \\(r(A)=2\\)，故 \\(|A|=0\\)。</p>'
    + fml(r"|A|=2(-a-1)-1(a+4)-4(1-4)=-3a+6=0\ \Rightarrow\ a=2") +
    '<p>此时 \\(|\\lambda E-A|=\\lambda(\\lambda-6)(\\lambda+3)\\)，特征值 \\(6,-3,0\\)。分别解 \\((A-\\lambda E)x=0\\) 得特征向量 \\(\\xi_1=(1,0,-1)^{\\top}\\)（\\(\\lambda=6\\)），\\(\\xi_2=(1,-1,1)^{\\top}\\)（\\(\\lambda=-3\\)），\\(\\xi_3=(1,2,1)^{\\top}\\)（\\(\\lambda=0\\)），三者两两正交，单位化得</p>'
    + fml(r"Q=\left(\frac{1}{\sqrt2}(1,0,-1)^{\top},\ \frac{1}{\sqrt3}(1,-1,1)^{\top},\ \frac{1}{\sqrt6}(1,2,1)^{\top}\right)") +
    '<p>标准形为 \\(6y_1^2-3y_2^2\\)。</p>')

add("复习题4解答3", "solve", 4, "投影型二次型规范形", 3,
    r"已知二次型 \(f(x_1,x_2,\cdots,x_n)=\displaystyle\sum_{i=1}^{n}\left(x_i-\frac{x_1+x_2+\cdots+x_n}{n}\right)^2\)，求 \(f\) 的规范形。",
    "\\(y_1^2+y_2^2+\\cdots+y_{n-1}^2\\)",
    '<p>记 \\(\\bar{x}=\\dfrac{x_1+\\cdots+x_n}{n}\\)，\\(\\mathbf{1}=(1,1,\\cdots,1)^{\\top}\\)，则</p>'
    + fml(r"f=\sum_{i=1}^n x_i^2-2\bar{x}\sum_{i=1}^n x_i+n\bar{x}^2=x^{\top}x-\frac{1}{n}(x^{\top}\mathbf{1})^2=x^{\top}\Big(E-\frac{1}{n}\mathbf{1}\mathbf{1}^{\top}\Big)x") +
    '<p>矩阵 \\(B=E-\\dfrac{1}{n}\\mathbf{1}\\mathbf{1}^{\\top}\\) 的特征值：\\(B\\mathbf{1}=\\mathbf{1}-\\mathbf{1}=0\\)，故 0 是特征值；对与 \\(\\mathbf{1}\\) 正交的 \\(x\\)，\\(Bx=x\\)，故 1 是 \\(n-1\\) 重特征值。因此 \\(r(B)=n-1\\)，\\(f\\geq 0\\) 半正定。</p>'
    '<p>正惯性指数为 \\(n-1\\)、负惯性指数为 0，规范形为 \\(y_1^2+y_2^2+\\cdots+y_{n-1}^2\\)。</p>')

add("复习题4解答4", "solve", 4, "正交变换化标准形", 2,
    r"用正交变换 \(x=Qy\) 将二次型 \(f(x_1,x_2,x_3)=x_1^2+3x_2^2+x_3^2+2x_1x_2+2x_1x_3+2x_2x_3\) 化成标准形，并判断其正定性。",
    "标准形为 \\(y_1^2+4y_2^2\\)（特征值 \\(0,1,4\\)）；\\(f\\) 不正定（半正定）",
    '<p>矩阵 \\(A=\\begin{pmatrix}1&1&1\\\\1&3&1\\\\1&1&1\\end{pmatrix}\\)。第 1、3 行相同，故 \\(|A|=0\\)；由 \\(\\mathrm{tr}(A)=5\\)、2 阶主子式之和为 4，得特征多项式 \\(|\\lambda E-A|=\\lambda(\\lambda-1)(\\lambda-4)\\)，特征值 \\(0,1,4\\)。</p>'
    '<p>分别解 \\((A-\\lambda E)x=0\\) 得 \\(\\eta_1=(-1,1,-1)^{\\top}\\)（\\(\\lambda=1\\)），\\(\\eta_2=(-1,0,1)^{\\top}\\)（\\(\\lambda=0\\)），\\(\\eta_3=(1,2,1)^{\\top}\\)（\\(\\lambda=4\\)），三者两两正交，单位化得</p>'
    + fml(r"Q=\left(\frac{1}{\sqrt3}(-1,1,-1)^{\top},\ \frac{1}{\sqrt2}(-1,0,1)^{\top},\ \frac{1}{\sqrt6}(1,2,1)^{\top}\right)") +
    '<p>在 \\(x=Qy\\) 下 \\(f=y_1^2+4y_2^2\\)。</p>'
    '<p>因特征值含 0，\\(f\\) 不正定（为半正定二次型）。</p>')

add("复习题4解答5", "solve", 4, "求和型二次型标准形", 2,
    r"已知二次型 \(f(x_1,x_2,x_3)=\displaystyle\sum_{i=1}^{3}\sum_{j=1}^{3}ij\,x_ix_j\)。<br>① 写出 \(f(x_1,x_2,x_3)\) 对应的矩阵；<br>② 求正交变换 \(x=Qy\) 将 \(f(x_1,x_2,x_3)\) 化为标准形。",
    "矩阵 \\(\\begin{pmatrix}1&2&3\\\\2&4&6\\\\3&6&9\\end{pmatrix}\\)；标准形为 \\(14y_3^2\\)，\\(Q=\\left(\\dfrac{1}{\\sqrt5}(-2,1,0)^{\\top},\\dfrac{1}{\\sqrt{70}}(-3,-6,5)^{\\top},\\dfrac{1}{\\sqrt6}(1,2,3)^{\\top}\\right)\\)",
    '<p>① \\(f=\\sum_{i,j}(i\\cdot j)x_ix_j=\\big(x_1+2x_2+3x_3\\big)^2\\)，系数 \\(ij\\) 恰为对称矩阵 \\(A\\) 的 \\((i,j)\\) 元：</p>'
    + fml(r"A=\begin{pmatrix}1&2&3\\2&4&6\\3&6&9\end{pmatrix}=vv^{\top},\qquad v=(1,2,3)^{\top}") +
    '<p>② \\(r(A)=1\\)，\\(\\mathrm{tr}(A)=14\\)，故特征值为 \\(14,0,0\\)。属于 14 的特征向量为 \\(v=(1,2,3)^{\\top}\\)；属于 0 的特征向量满足 \\(x_1+2x_2+3x_3=0\\)，取正交规范化的一组：</p>'
    + fml(r"Q=\left(\frac{1}{\sqrt5}(-2,1,0)^{\top},\ \frac{1}{\sqrt{70}}(-3,-6,5)^{\top},\ \frac{1}{\sqrt6}(1,2,3)^{\top}\right)") +
    '<p>则在 \\(x=Qy\\) 下标准形为 \\(f=14y_3^2\\)。</p>')

with open(r"D:\Web\XD_learn\tools\batch\keben_k2.json", "w", encoding="utf-8") as fp:
    json.dump(items, fp, ensure_ascii=False, indent=1)

print("total:", len(items))
from collections import Counter
print(Counter(x["srcNo"].split("填空")[0].split("选择")[0].split("解答")[0].split("证明")[0] for x in items))
print(Counter(x["ty"] for x in items))
print(Counter(x["ch"] for x in items))
