# -*- coding: utf-8 -*-
# 线性代数学习指导 第五章(方阵的特征值与特征向量) p112-p119 转录
import json, io

SRC = "学习指导"

def e(srcNo, ty, ch, kp, diff, score, q, ans, sol, opts=None):
    d = {"src": SRC, "srcNo": srcNo, "ty": ty, "ch": ch, "kp": kp,
         "diff": diff, "score": score, "q": q}
    if opts is not None:
        d["opts"] = opts
    d["ans"] = ans
    d["sol"] = sol
    return d

items = []

# ---------------- 例21 ----------------
items.append(e("例21", "solve", 3, "特征值与矩阵幂", 3, 8,
r"某地区每年有比例为 \(p\) 的农村居民移居城镇，有比例为 \(q\) 的城镇居民移居农村。假设该地区总人口数不变，且上述人口迁移的规律不变。记 \(n\) 年后农村人口和城镇人口占总人口的比例依次为 \(x_n\) 和 \(y_n\)（\(x_n+y_n=1\)）。<br>(1) 求关系式 \(\begin{pmatrix}x_{n+1}\\y_{n+1}\end{pmatrix}=A\begin{pmatrix}x_n\\y_n\end{pmatrix}\) 中的矩阵 \(A\)；<br>(2) 设目前农村人口和城镇人口相等，即 \(\begin{pmatrix}x_0\\y_0\end{pmatrix}=\begin{pmatrix}0.5\\0.5\end{pmatrix}\)，求 \(\begin{pmatrix}x_n\\y_n\end{pmatrix}\)。",
r"\(A=\begin{pmatrix}1-p&q\\p&1-q\end{pmatrix}\)；\(\begin{pmatrix}x_n\\y_n\end{pmatrix}=\dfrac{1}{2(p+q)}\begin{pmatrix}2q+(p-q)(1-p-q)^n\\2p+(q-p)(1-p-q)^n\end{pmatrix}\)。",
r"<p>(1) 由题意知 \(x_{n+1}=(1-p)x_n+qy_n\)，\(y_{n+1}=px_n+(1-q)y_n\)，故 \(A=\begin{pmatrix}1-p&q\\p&1-q\end{pmatrix}\)。</p><p>(2) 由 (1) 知 \(\begin{pmatrix}x_n\\y_n\end{pmatrix}=A^n\begin{pmatrix}x_0\\y_0\end{pmatrix}\)。先求 \(A^n\)：\(A\) 的特征值为 \(\lambda_1=1\)，\(\lambda_2=1-p-q\)，对应的特征向量分别为 \(\xi_1=(q,p)^{\top}\)，\(\xi_2=(-1,1)^{\top}\)。令 \(P=(\xi_1,\xi_2)\)，则 \(P\) 可逆，且 \(P^{-1}AP=\operatorname{diag}(1,1-p-q)\)，于是</p><div class=\"fml\">$$A^n=P\operatorname{diag}(1,(1-p-q)^n)P^{-1}=\frac{1}{p+q}\begin{pmatrix}q+p(1-p-q)^n&q-q(1-p-q)^n\\p-p(1-p-q)^n&p+q(1-p-q)^n\end{pmatrix}.$$</div><p>代入 \(x_0=y_0=0.5\) 得</p><div class=\"fml\">$$\begin{pmatrix}x_n\\y_n\end{pmatrix}=A^n\begin{pmatrix}0.5\\0.5\end{pmatrix}=\frac{1}{2(p+q)}\begin{pmatrix}2q+(p-q)(1-p-q)^n\\2p+(q-p)(1-p-q)^n\end{pmatrix}.$$</div><p>方法点评：这是特征值对角化应用于离散递推模型的典型问题，关键是将递推关系写成矩阵形式，再通过相似对角化计算 \(A^n\)。</p>"))

# ---------------- 例22 ----------------
items.append(e("例22", "proof", 3, "特征向量与数量矩阵", 3, 8,
r"若任一 \(n\) 维非零列向量都是 \(n\) 阶矩阵 \(A\) 的特征向量，证明：\(A\) 是数量矩阵。",
r"\(A\) 是数量矩阵（即 \(A=\lambda E\)）。",
r"<p>设单位向量 \(\varepsilon_1,\varepsilon_2,\dots,\varepsilon_n\) 分别为对应于 \(A\) 的特征值 \(\lambda_1,\lambda_2,\dots,\lambda_n\) 的特征向量，即 \(A\varepsilon_i=\lambda_i\varepsilon_i\)。则</p><div class=\"fml\">$$A(\varepsilon_1,\varepsilon_2,\dots,\varepsilon_n)=(A\varepsilon_1,A\varepsilon_2,\dots,A\varepsilon_n)=(\lambda_1\varepsilon_1,\lambda_2\varepsilon_2,\dots,\lambda_n\varepsilon_n)=(\varepsilon_1,\varepsilon_2,\dots,\varepsilon_n)\operatorname{diag}(\lambda_1,\lambda_2,\dots,\lambda_n).$$</div><p>由于 \((\varepsilon_1,\varepsilon_2,\dots,\varepsilon_n)=E\)，故 \(A=\operatorname{diag}(\lambda_1,\lambda_2,\dots,\lambda_n)\)。</p><p>再设向量 \(p=(1,1,\dots,1)^{\top}\) 是矩阵 \(A\) 对应于特征值 \(\lambda\) 的特征向量，则 \(Ap=\lambda p\)，而 \(Ap=(\lambda_1,\lambda_2,\dots,\lambda_n)^{\top}=\lambda(1,1,\dots,1)^{\top}\)，故 \(\lambda_1=\lambda_2=\dots=\lambda_n=\lambda\)。所以 \(A=\begin{pmatrix}\lambda&&\\&\ddots&\\&&\lambda\end{pmatrix}\) 是数量矩阵。证毕。</p><p>方法点评：本题的关键是先用标准基向量把 \(A\) 化为对角阵，再用全 1 向量迫使对角元全部相等。</p>"))

# ---------------- 同步练习 1 单选题 ----------------
items.append(e("同步练习1(1)", "choice", 3, "特征值满足矩阵方程", 1, 8,
r"设 \(A\) 为 \(n\) 阶矩阵，且 \(A^2=A\)，则（　）",
3,
r"<p>设 \(Ax=\lambda x\)（\(x\neq0\)），则 \(A^2x=\lambda^2x\)。由 \(A^2=A\) 得 \(\lambda^2x=\lambda x\)，故 \(\lambda^2=\lambda\)，特征值只能是 0 或 1。（\(A=O\) 或 \(A=E\) 不必然成立，\(|A|=1\) 也不必然成立。）故选 D。</p>",
["\\(A\\) \\(|A|=1\\)", "\\(B\\) \\(A=O\\) 或 \\(A=E\\)", "\\(C\\) \\(A\\) 的特征值可能是 0 或 1", "\\(D\\) \\(A\\) 的特征值只能是 0 或 1"]))

items.append(e("同步练习1(2)", "choice", 3, "相似矩阵的性质", 2, 8,
r"设 \(A,B\) 为 \(n\) 阶矩阵，且 \(A\) 与 \(B\) 相似，则（　）",
2,
r"<p>\(A\sim B\) 即存在可逆 \(P\) 使 \(P^{-1}AP=B\)，两边取行列式得 \(|A|=|B|\)；相似矩阵显然等价，故 C 正确。相似矩阵不一定有相同的特征向量，也不一定都能相似于对角阵，更不一定存在正交相似变换矩阵，A、B、D 均不正确。故选 C。</p>",
["\\(A\\) \\(A\\) 与 \\(B\\) 有相同的特征向量", "\\(B\\) \\(A\\) 与 \\(B\\) 相似于同一个对角矩阵", "\\(C\\) \\(A\\) 与 \\(B\\) 等价且 \\(|A|=|B|\\)", "\\(D\\) 存在正交矩阵 \\(M\\)，使得 \\(M^{\\top}AM=B\\)"]))

items.append(e("同步练习1(3)", "choice", 3, "可对角化的条件", 1, 8,
r"若 \(n\) 阶方阵 \(A\) 与某个对角矩阵相似，则（　）",
3,
r"<p>\(A\) 相似于对角阵的充要条件是 \(A\) 有 \(n\) 个线性无关的特征向量，故 D 正确。此时 \(A\) 未必满秩（0 可以是特征值），特征值未必互异，\(A\) 也未必是对称矩阵，A、B、C 均不成立。故选 D。</p>",
["\\(A\\) \\(R(A)=n\\)", "\\(B\\) \\(A\\) 有 \\(n\\) 个不同的特征值", "\\(C\\) \\(A\\) 一定是对称矩阵", "\\(D\\) \\(A\\) 有 \\(n\\) 个线性无关的特征向量"]))

items.append(e("同步练习1(4)", "choice", 3, "伴随矩阵的特征值", 2, 8,
r"若 3 阶矩阵 \(A\) 的特征值为 \(-1,1,2\)，则矩阵 \(A^{*}+2E\) 的特征值为（　）",
2,
r"<p>\(|A|=(-1)\times1\times2=-2\)。当 \(A\) 可逆时 \(A^{*}=|A|A^{-1}\)，故 \(A^{*}\) 的特征值为 \(|A|/\lambda_i\)，即 \(2,-2,-1\)。从而 \(A^{*}+2E\) 的特征值为 \(4,0,1\)。故选 C。</p>",
["\\(A\\) \\(2,3,5\\)", "\\(B\\) \\(-2,0,1\\)", "\\(C\\) \\(4,0,1\\)", "\\(D\\) \\(-1,1,2\\)"]))

items.append(e("同步练习1(5)", "choice", 3, "特征向量求参数", 2, 8,
r"已知 \(\alpha=(1,-2,3)^{\top}\) 是矩阵 \(A=\begin{pmatrix}3&2&-1\\a&-2&2\\3&b&-1\end{pmatrix}\) 的特征向量，则（　）",
0,
r"<p>设 \(A\alpha=\lambda\alpha\)，计算 \(A\alpha=(3-4-3,\ a+4+6,\ 3-2b-3)^{\top}=(-4,\ a+10,\ -2b)^{\top}\)。由第一个分量得 \(\lambda=-4\)；由第二个分量 \(a+10=(-4)\times(-2)=8\) 得 \(a=-2\)；由第三个分量 \(-2b=(-4)\times3=-12\) 得 \(b=6\)。故选 A。</p>",
["\\(A\\) \\(a=-2,\\ b=6\\)", "\\(B\\) \\(a=2,\\ b=-6\\)", "\\(C\\) \\(a=2,\\ b=6\\)", "\\(D\\) \\(a=-2,\\ b=-6\\)"]))

items.append(e("同步练习1(6)", "choice", 3, "相似对角化判定", 2, 8,
r"下列矩阵不能相似对角化的是（　）",
3,
r"<p>(A) 为实对称矩阵，必可相似对角化。(B) 上三角矩阵，特征值 \(1,3,-1\) 互不相同，必可对角化。(C) 各行成比例，\(R(A)=1\)，特征值为 \(4,0,0\)；属于二重特征值 0 的线性无关特征向量有 \(3-1=2\) 个，等于其代数重数，可对角化。(D) 上三角阵，特征值 \(1,1,-1\)；对二重特征值 1，\(R(B-E)=2\)，线性无关特征向量只有 \(3-2=1\) 个，少于代数重数 2，故不能相似对角化。故选 D。</p>",
["\\(A\\) \\(\\begin{pmatrix}1&0&-1\\\\0&2&3\\\\-1&3&5\\end{pmatrix}\\)", "\\(B\\) \\(\\begin{pmatrix}1&0&0\\\\2&3&0\\\\-1&5&-1\\end{pmatrix}\\)", "\\(C\\) \\(\\begin{pmatrix}1&0&-1\\\\2&0&-2\\\\-3&0&3\\end{pmatrix}\\)", "\\(D\\) \\(\\begin{pmatrix}1&2&3\\\\0&1&3\\\\0&0&-1\\end{pmatrix}\\)"]))

items.append(e("同步练习1(7)", "choice", 3, "实对称阵特征向量", 2, 8,
r"设 \(A\) 是 \(n\) 阶实对称矩阵，\(P\) 是 \(n\) 阶可逆矩阵。已知 \(n\) 维向量 \(\alpha\) 是 \(A\) 属于特征值 \(\lambda\) 的特征向量，则 \((P^{-1}AP)^{\top}\) 属于特征值 \(\lambda\) 的特征向量是（　）",
1,
r"<p>由 \(A\) 实对称知 \(A^{\top}=A\)，故 \((P^{-1}AP)^{\top}=P^{\top}A^{\top}(P^{-1})^{\top}=P^{\top}A(P^{-1})^{\top}\)。记 \(B=(P^{-1}AP)^{\top}\)，则 \(B(P^{\top}\alpha)=P^{\top}A(P^{-1})^{\top}P^{\top}\alpha=P^{\top}A\alpha=\lambda(P^{\top}\alpha)\)，且 \(P^{\top}\alpha\neq0\)，故 \(P^{\top}\alpha\) 是 \(B\) 属于 \(\lambda\) 的特征向量。故选 B。</p>",
["\\(A\\) \\(P^{-1}\\alpha\\)", "\\(B\\) \\(P^{\\top}\\alpha\\)", "\\(C\\) \\(P\\alpha\\)", "\\(D\\) \\((P^{-1})^{\\top}\\alpha\\)"]))

items.append(e("同步练习1(8)", "choice", 3, "特征向量的传递性", 2, 8,
r"设 \(A\) 是 \(n\) 阶矩阵，则下列命题正确的是（　）",
3,
r"<p>若 \(\alpha\) 是 \(A^{-1}\) 的特征向量，即 \(A^{-1}\alpha=\lambda\alpha\)（\(\lambda\neq0\)），两边左乘 \(A\) 得 \(\alpha=\lambda A\alpha\)，即 \(A\alpha=\frac{1}{\lambda}\alpha\)，故 \(\alpha\) 也是 \(A\) 的特征向量，D 正确。\(A^{\top}\)、\(A^{*}\)、\(A^2\) 的特征向量一般不是 \(A\) 的特征向量。故选 D。</p>",
["\\(A\\) 若 \\(\\alpha\\) 是 \\(A^{\\top}\\) 的特征向量，则 \\(\\alpha\\) 是 \\(A\\) 的特征向量", "\\(B\\) 若 \\(\\alpha\\) 是 \\(A^{*}\\) 的特征向量，则 \\(\\alpha\\) 是 \\(A\\) 的特征向量", "\\(C\\) 若 \\(\\alpha\\) 是 \\(A^2\\) 的特征向量，则 \\(\\alpha\\) 是 \\(A\\) 的特征向量", "\\(D\\) 若 \\(\\alpha\\) 是 \\(A^{-1}\\) 的特征向量，则 \\(\\alpha\\) 是 \\(A\\) 的特征向量"]))

items.append(e("同步练习1(9)", "choice", 3, "相似矩阵的性质", 2, 8,
r"设 \(A,B\) 为 \(n\) 阶矩阵，且 \(A\) 与 \(B\) 相似，则（　）",
3,
r"<p>设 \(B=P^{-1}AP\)，则对任意常数 \(t\)：\(tE-B=tE-P^{-1}AP=P^{-1}(tE-A)P\)，故 \(tE-A\) 与 \(tE-B\) 相似，D 正确。\(A\) 与 \(B\) 是不同矩阵，\(\lambda E-A=\lambda E-B\) 一般不成立；相似矩阵的特征向量一般不同；相似矩阵未必都能对角化。故选 D。</p>",
["\\(A\\) \\(\\lambda E-A=\\lambda E-B\\)", "\\(B\\) \\(A\\) 与 \\(B\\) 有相同的特征值和特征向量", "\\(C\\) \\(A\\) 与 \\(B\\) 都相似于一个对角矩阵", "\\(D\\) 对任意常数 \\(t\\)，\\(tE-A\\) 与 \\(tE-B\\) 相似"]))

items.append(e("同步练习1(10)", "choice", 3, "特征向量线性无关", 2, 8,
r"设 \(\lambda_1,\lambda_2\) 是矩阵 \(A\) 的两个不同的特征值，对应的特征向量分别为 \(\alpha_1,\alpha_2\)，则 \(\alpha_1\)，\(A(\alpha_1+\alpha_2)\) 线性无关的充分必要条件是（　）",
1,
r"<p>设 \(k_1\alpha_1+k_2A(\alpha_1+\alpha_2)=0\)，即 \(k_1\alpha_1+k_2(\lambda_1\alpha_1+\lambda_2\alpha_2)=(k_1+k_2\lambda_1)\alpha_1+k_2\lambda_2\alpha_2=0\)。由 \(\alpha_1,\alpha_2\) 线性无关（不同特征值的特征向量必线性无关）得 \(k_1+k_2\lambda_1=0\) 且 \(k_2\lambda_2=0\)。该向量组线性无关的充要条件是上式只有零解：当 \(\lambda_2\neq0\) 时必有 \(k_2=0\)，进而 \(k_1=0\)；当 \(\lambda_2=0\) 时 \(k_2\) 可任取，有非零解。故充要条件为 \(\lambda_2\neq0\)。故选 B。</p>",
["\\(A\\) \\(\\lambda_1\\neq0\\)", "\\(B\\) \\(\\lambda_2\\neq0\\)", "\\(C\\) \\(\\lambda_1=0\\)", "\\(D\\) \\(\\lambda_2=0\\)"]))

items.append(e("同步练习1(11)", "choice", 3, "特征值与可逆性", 1, 8,
r"设 3 阶矩阵 \(A\) 有特征值 \(1,-1,2\)，则下列矩阵为可逆矩阵的是（　）",
3,
r"<p>\(tE-A\) 可逆 \(\iff\) \(t\) 不是 \(A\) 的特征值。特征值为 \(1,-1,2\)，故 \(E-A\)、\(E+A\)、\(2E-A\) 都以 \(A\) 的特征值为自己的特征值，均含有特征值 0，不可逆；而 \(2E+A\) 的特征值为 \(3,1,4\)，全不为零，故可逆。故选 D。</p>",
["\\(A\\) \\(E-A\\)", "\\(B\\) \\(E+A\\)", "\\(C\\) \\(2E-A\\)", "\\(D\\) \\(2E+A\\)"]))

# ---------------- 同步练习 2 填空题 ----------------
items.append(e("同步练习2(1)", "blank", 3, "矩阵多项式特征值", 1, 8,
r"设 \(n\) 阶矩阵有一个特征值 \(\lambda=2\)，则 \(2A^2-2A+5E\) 必有特征值 \(\underline{\hspace{2em}}\)。",
r"\(9\)。",
r"<p>设 \(Ax=2x\)，则 \(2A^2-2A+5E\) 的特征值为 \(f(2)=2\times2^2-2\times2+5=8-4+5=9\)。</p>"))

items.append(e("同步练习2(2)", "blank", 3, "相似对角化条件", 2, 8,
r"设 \(\begin{pmatrix}\lambda_0&a\\0&\lambda_0\end{pmatrix}\) 相似于对角阵，则 \(a=\underline{\hspace{2em}}\)。",
r"\(0\)。",
r"<p>该矩阵的特征值为二重根 \(\lambda_0\)。它相似于对角阵要求属于 \(\lambda_0\) 有两个线性无关的特征向量，即 \(R(\lambda_0E-A)=R\begin{pmatrix}0&-a\\0&0\end{pmatrix}=0\)，故 \(a=0\)。</p>"))

items.append(e("同步练习2(3)", "blank", 3, "特征值与行列式", 2, 8,
r"已知矩阵 \(A=\begin{pmatrix}a&1&b\\2&3&4\\-1&1&-1\end{pmatrix}\) 的特征值之和为 3，特征值之积为 \(-24\)，则 \(b=\underline{\hspace{2em}}\)。",
r"\(-3\)（此时 \(a=1\)）。",
r"<p>特征值之和等于迹：\(a+3+(-1)=3\)，得 \(a=1\)。特征值之积等于行列式：\(|A|=-24\)。计算 \(|A|=a(3\times(-1)-4\times1)-1\cdot(2\times(-1)-4\times(-1))+b(2\times1-3\times(-1))=-7a-2+5b\)，代入 \(a=1\) 得 \(-7-2+5b=-24\)，故 \(b=-3\)。</p>"))

items.append(e("同步练习2(4)", "blank", 3, "相似变换矩阵", 2, 8,
r"设 \(A\) 为 3 阶矩阵，\(P\) 为 3 阶可逆矩阵，且 \(P^{-1}AP=\begin{pmatrix}1&0&0\\0&1&0\\0&0&2\end{pmatrix}\)。若 \(P=(\alpha_1,\alpha_2,\alpha_3)\)，\(Q=(\alpha_1+\alpha_2,\alpha_2,\alpha_3)\)，则 \(Q^{-1}AQ=\underline{\hspace{4em}}\)。",
r"\(\begin{pmatrix}1&0&0\\0&1&0\\0&0&2\end{pmatrix}\)。",
r"<p>由 \(P^{-1}AP=\operatorname{diag}(1,1,2)\) 知 \(A\alpha_1=\alpha_1\)，\(A\alpha_2=\alpha_2\)，\(A\alpha_3=2\alpha_3\)。记 \(Q=(\alpha_1+\alpha_2,\alpha_2,\alpha_3)\)，则 \(AQ=(A\alpha_1+A\alpha_2,\ A\alpha_2,\ A\alpha_3)=(\alpha_1+\alpha_2,\ \alpha_2,\ 2\alpha_3)=Q\operatorname{diag}(1,1,2)\)。由 \(Q\) 可逆得 \(Q^{-1}AQ=\operatorname{diag}(1,1,2)\)。</p>"))

items.append(e("同步练习2(5)", "blank", 3, "特征值与可逆性", 2, 8,
r"设 \(A\) 为 3 阶矩阵，\(E+A\)，\(3E+A\)，\(2E+A\) 均不可逆，则 \(|A|=\underline{\hspace{2em}}\)。",
r"\(-6\)。",
r"<p>\(E+A\)、\(3E+A\)、\(2E+A\) 均不可逆，等价于 \(-1,-3,-2\) 都是 \(A\) 的特征值。3 阶矩阵的全部特征值即 \(-1,-3,-2\)，故 \(|A|=(-1)\times(-3)\times(-2)=-6\)。</p>"))

items.append(e("同步练习2(6)", "blank", 3, "伴随矩阵特征值", 2, 8,
r"设方阵 \(A\) 的特征值为 2，且 \(|A|=4\)，则 \(\left(\frac{1}{4}A\right)^{-1}-\frac{1}{2}A^{*}\) 有一个特征值为 \(\underline{\hspace{2em}}\)。",
r"\(1\)。",
r"<p>设 \(Ax=2x\)。\(A\) 可逆，\(\left(\frac14A\right)^{-1}=4A^{-1}\) 的特征值为 \(4/2=2\)；\(A^{*}=|A|A^{-1}\) 的特征值为 \(|A|/\lambda=4/2=2\)，故 \(\frac12A^{*}\) 的特征值为 1。所求矩阵的特征值为 \(2-1=1\)。</p>"))

items.append(e("同步练习2(7)", "blank", 3, "相似矩阵的秩", 2, 8,
r"设矩阵 \(A=\begin{pmatrix}0&0&1\\0&1&0\\1&0&0\end{pmatrix}\)，已知矩阵 \(B\) 相似于 \(A\)，\(E\) 为 3 阶单位阵，则 \(R(B-E)=\underline{\hspace{2em}}\)。",
r"\(1\)。",
r"<p>\(B\sim A\)，故 \(B-E\sim A-E\)，从而 \(R(B-E)=R(A-E)\)。\(A-E=\begin{pmatrix}-1&0&1\\0&0&0\\1&0&-1\end{pmatrix}\)，第一行与第三行互为相反数，秩为 1，故 \(R(B-E)=1\)。</p>"))

items.append(e("同步练习2(8)", "blank", 3, "相似矩阵迹与行列式", 2, 8,
r"设矩阵 \(A=\begin{pmatrix}1&-2&0\\-2&x&-2\\0&-2&3\end{pmatrix}\) 与 \(B=\begin{pmatrix}-1&0&0\\0&2&0\\0&0&y\end{pmatrix}\) 相似，则 \(x=\underline{\hspace{2em}}\)，\(y=\underline{\hspace{2em}}\)。",
r"\(x=2,\ y=5\)。",
r"<p>相似矩阵有相同的迹与行列式。由迹：\(1+x+3=(-1)+2+y\)，得 \(y=x+3\)。由行列式：按第一行展开 \(|A|=1\times(3x-4)-(-2)\times(-6-0)+0=3x-16\)，而 \(|B|=-1\times2\times y=-2y=-2x-6\)。由 \(3x-16=-2x-6\) 得 \(x=2\)，从而 \(y=5\)。</p>"))

# ---------------- 同步练习 3-23 ----------------
items.append(e("同步练习3", "solve", 3, "正交矩阵的构造", 2, 8,
r"设 \(A=\begin{pmatrix}0&1&0\\a&0&c\\b&0&\frac12\end{pmatrix}\)，取一组 \(a,b,c\) 使得 \(A\) 为正交矩阵。",
r"可取 \(a=\frac12,\ b=-\frac{\sqrt3}{2},\ c=\frac{\sqrt3}{2}\)（答案不唯一）。",
r"<p>由 \(A\) 正交即 \(A^{\top}A=E\)，即 \(A\) 的列向量组为标准正交组。三个列向量为 \((0,a,b)^{\top}\)、\((1,0,0)^{\top}\)、\((0,c,\frac12)^{\top}\)，于是得方程组 \(\begin{cases}a^2+b^2=1,\\ ac+\frac12b=0,\\ c^2+\frac14=1.\end{cases}\)</p><p>由 \(c^2=\frac34\) 取 \(c=\frac{\sqrt3}{2}\)；由 \(ac=-\frac b2\) 取 \(a=\frac12\) 得 \(b=-\sqrt3 a=-\frac{\sqrt3}{2}\)。验证：\(a^2+b^2=\frac14+\frac34=1\)，\(ac+\frac12b=\frac{\sqrt3}{4}-\frac{\sqrt3}{4}=0\)，成立。故可取 \(a=\frac12,\ b=-\frac{\sqrt3}{2},\ c=\frac{\sqrt3}{2}\)。</p>"))

items.append(e("同步练习4", "solve", 3, "特征向量求参数", 1, 8,
r"已知 \(\alpha=(1,1,1)^{\top}\) 是 \(A=\begin{pmatrix}a&1&1\\2&0&1\\-1&2&2\end{pmatrix}\) 属于特征值 \(\lambda\) 的特征向量，求 \(a,\lambda\)。",
r"\(\lambda=3,\ a=1\)。",
r"<p>由题意知 \(A\alpha=\lambda\alpha\)，即 \(\begin{pmatrix}a&1&1\\2&0&1\\-1&2&2\end{pmatrix}\begin{pmatrix}1\\1\\1\end{pmatrix}=\begin{pmatrix}a+2\\3\\3\end{pmatrix}=\lambda\begin{pmatrix}1\\1\\1\end{pmatrix}\)。比较第二、三个分量得 \(\lambda=3\)；再比较第一个分量得 \(a+2=3\)，即 \(a=1\)。故 \(\lambda=3,\ a=1\)。</p>"))

items.append(e("同步练习5", "solve", 3, "可对角化求参数", 2, 8,
r"设矩阵 \(A=\begin{pmatrix}0&0&1\\x&1&y\\1&0&0\end{pmatrix}\) 有三个线性无关的特征向量，求 \(x\) 与 \(y\) 应满足的条件。",
r"\(x+y=0\)。",
r"<p>由 \(A\) 的特征方程 \(|A-\lambda E|=\begin{vmatrix}-\lambda&0&1\\x&1-\lambda&y\\1&0&-\lambda\end{vmatrix}=(1-\lambda)(\lambda^2-1)=-(\lambda-1)^2(\lambda+1)=0\)，得 \(A\) 的全部特征值 \(\lambda_1=\lambda_2=1\)，\(\lambda_3=-1\)。有三个线性无关的特征向量要求二重特征值 1 恰有两个线性无关的特征向量，即 \(R(A-E)=1\)。由题设推知 \(R(A-E)=1\)，而 \(A-E=\begin{pmatrix}-1&0&1\\x&0&y\\1&0&-1\end{pmatrix}\)，其秩为 1 要求其任意二阶子式为零，特别地 \(\begin{vmatrix}-1&1\\x&y\end{vmatrix}=0\)，即 \(x+y=0\) 为所求的关系式。</p>"))

items.append(e("同步练习6", "solve", 3, "相似矩阵特征向量", 1, 8,
r"设方阵 \(A\) 与 \(B\) 相似（相似变换矩阵为 \(P\)），且 \(\xi\) 为 \(A\) 的特征值 \(\lambda_0\) 对应的特征向量，求矩阵 \(B\) 对应于特征值 \(\lambda_0\) 的一个特征向量。",
r"\(P^{-1}\xi\)。",
r"<p>由 \(A\sim B\) 设 \(P^{-1}AP=B\)，且 \(A\xi=\lambda_0\xi\)。由 \(A=PBP^{-1}\) 得 \(A\xi=PBP^{-1}\xi\)，两边左乘 \(P^{-1}\)：\(P^{-1}A\xi=BP^{-1}\xi\)，即 \(B(P^{-1}\xi)=\lambda_0(P^{-1}\xi)\)。由于 \(\xi\neq0\) 且 \(P\) 可逆，\(P^{-1}\xi\neq0\)，故 \(P^{-1}\xi\) 是 \(B\) 对应于 \(\lambda_0\) 的特征向量。注意 \(P^{-1}\xi\) 一般不等于 \(\xi\)，这说明相似矩阵有相同的特征值，但不一定有相同的特征向量。</p>"))

items.append(e("同步练习7", "proof", 3, "特征向量线性无关", 2, 8,
r"设 \(\lambda_1,\lambda_2\) 为 \(n\) 阶方阵 \(A\) 的两个不同特征值，\(x_1,x_2\) 分别为对应于 \(\lambda_1,\lambda_2\) 的特征向量，试证 \(x_1+x_2\) 不是 \(A\) 的特征向量。",
r"用反证法证明 \(x_1+x_2\) 不是 \(A\) 的特征向量。",
r"<p>反证法。倘若 \(x_1+x_2\) 是 \(A\) 的某个特征值 \(\lambda_0\) 对应的特征向量，则 \(A(x_1+x_2)=\lambda_0(x_1+x_2)\)。而 \(A(x_1+x_2)=Ax_1+Ax_2=\lambda_1x_1+\lambda_2x_2\)，故 \((\lambda_1-\lambda_0)x_1+(\lambda_2-\lambda_0)x_2=0\)。由于 \(\lambda_1\neq\lambda_2\)，属于不同特征值的特征向量 \(x_1,x_2\) 线性无关，于是 \(\lambda_1-\lambda_0=0\) 且 \(\lambda_2-\lambda_0=0\)，得 \(\lambda_1=\lambda_2\)，与 \(\lambda_1\neq\lambda_2\) 矛盾。故 \(x_1+x_2\) 不是 \(A\) 的特征向量，命题得证。</p>"))

items.append(e("同步练习8", "proof", 3, "伴随矩阵的正交性", 2, 8,
r"设 \(A\) 为正交矩阵，证明：\(A\) 的伴随矩阵 \(A^{*}\) 也是正交矩阵。",
r"由 \((A^{*})^{\top}A^{*}=E\) 证得。",
r"<p>因 \(A\) 为正交矩阵，有 \(A^{\top}A=AA^{\top}=E\)，故 \(A\) 可逆且 \(|A|^2=|A^{\top}A|=1\)，即 \(|A|=\pm1\neq0\)。由 \(A^{*}=|A|A^{-1}\) 得 \((A^{*})^{\top}A^{*}=(|A|A^{-1})^{\top}(|A|A^{-1})=|A|^2(A^{-1})^{\top}A^{-1}=|A|^2(A^{\top})^{-1}A^{-1}=|A|^2(AA^{\top})^{-1}=|A|^2E=E\)。故 \(A^{*}\) 也是正交矩阵，证毕。</p>"))

items.append(e("同步练习9", "solve", 3, "伴随矩阵迹与特征值", 2, 8,
r"设 3 阶方阵 \(A=(a_{ij})\) 可逆，已知 \(A^{-1}\) 的特征值为 \(1,\frac12,\frac13\)，试求 \(A\) 的伴随矩阵 \(A^{*}\) 的主对角线元素之和 \(A_{11}+A_{22}+A_{33}\)。",
r"\(11\)。",
r"<p>\(A^{-1}\) 的特征值为 \(1,\frac12,\frac13\)，故 \(A\) 的特征值为 \(1,2,3\)，从而 \(|A|=1\times2\times3=6\)。当 \(A\) 可逆时 \(A^{*}=|A|A^{-1}\)，故 \(A^{*}\) 的特征值为 \(|A|/\lambda\)，即 \(6,3,2\)。矩阵的迹等于其特征值之和，故 \(A_{11}+A_{22}+A_{33}=\operatorname{tr}(A^{*})=6+3+2=11\)。</p>"))

items.append(e("同步练习10", "proof", 3, "行和与特征值", 2, 8,
r"设 \(n\) 阶方阵 \(A=(a_{ij})\) 可逆，且 \(A\) 的每行元素之和都等于常数 \(a\)，试证：\(a\) 是 \(A\) 的一个特征值且 \(a\neq0\)，并说明 \(A\) 的伴随矩阵 \(A^{*}\) 的每行元素之和都等于什么。",
r"\(a\) 是 \(A\) 的特征值且 \(a\neq0\)；\(A^{*}\) 的每行元素之和都等于 \(\frac{|A|}{a}\)。",
r"<p>由每行元素之和为 \(a\) 得 \(A(1,1,\dots,1)^{\top}=a(1,1,\dots,1)^{\top}\)，由特征值定义知 \(a\) 是 \(A\) 的一个特征值，\(\xi=(1,1,\dots,1)^{\top}\) 为对应的特征向量。若 \(a=0\)，则 0 是 \(A\) 的特征值，\(|A|=0\)，与 \(A\) 可逆矛盾，故 \(a\neq0\)。进而 \(|A|/a\) 是 \(A^{*}=|A|A^{-1}\) 的特征值，且对应特征向量仍为 \(\xi\)，即 \(A^{*}\xi=\frac{|A|}{a}\xi\)。写成分量形式即 \(\left(\sum_{j=1}^n A_{1j},\ \sum_{j=1}^n A_{2j},\ \dots,\ \sum_{j=1}^n A_{nj}\right)^{\top}=\frac{|A|}{a}(1,1,\dots,1)^{\top}\)，故 \(A^{*}\) 的每行元素之和都等于 \(\frac{|A|}{a}\)，证毕。</p>"))

items.append(e("同步练习11", "solve", 3, "实对称矩阵求 A", 3, 8,
r"设 3 阶实对称矩阵 \(A\) 的特征值为 \(1,2,-1\)，且 \(\alpha_1=(1,1,1)^{\top}\)，\(\alpha_2=(1,0,-1)^{\top}\) 分别为对应于特征值 \(1,2\) 的特征向量，试求矩阵 \(A\)。",
r"\(A=\begin{pmatrix}\frac76&\frac23&-\frac56\\\frac23&-\frac13&\frac23\\-\frac56&\frac23&\frac76\end{pmatrix}\)。",
r"<p>设对应于特征值 \(-1\) 的特征向量为 \(\alpha_3=(x_1,x_2,x_3)^{\top}\)。由实对称矩阵不同特征值对应的特征向量正交，得 \(\alpha_1^{\top}\alpha_3=0\)，\(\alpha_2^{\top}\alpha_3=0\)，即方程组 \(\begin{cases}x_1+x_2+x_3=0,\\ x_1-x_3=0.\end{cases}\) 解得其基础解系为 \(\alpha_3=(1,-2,1)^{\top}\)。</p><p>令 \(P=(\alpha_1,\alpha_2,\alpha_3)=\begin{pmatrix}1&1&1\\1&0&-2\\1&-1&1\end{pmatrix}\)，则 \(P^{-1}AP=\operatorname{diag}(1,2,-1)\)，故 \(A=P\operatorname{diag}(1,2,-1)P^{-1}\)，即 \(A=\sum_i\lambda_i\frac{\alpha_i\alpha_i^{\top}}{\alpha_i^{\top}\alpha_i}=\frac13\alpha_1\alpha_1^{\top}+\alpha_2\alpha_2^{\top}-\frac16\alpha_3\alpha_3^{\top}\)，计算得</p><div class=\"fml\">$$A=\begin{pmatrix}\frac76&\frac23&-\frac56\\\frac23&-\frac13&\frac23\\-\frac56&\frac23&\frac76\end{pmatrix}.$$</div><p>可验证 \(A\alpha_1=\alpha_1\)，\(A\alpha_2=2\alpha_2\)，且 \(A\) 为实对称矩阵，结果正确。</p>"))

items.append(e("同步练习12", "solve", 3, "伴随特征值反求参数", 3, 8,
r"设矩阵 \(A=\begin{pmatrix}a&-1&c\\5&b&3\\1-c&0&-a\end{pmatrix}\)，\(|A|=-1\)，又 \(A^{*}\) 有一个特征值 \(\lambda_0\)，对应的一个特征向量为 \(\alpha=(-1,-1,1)^{\top}\)，求参数 \(a,b,c\) 和 \(\lambda_0\) 的值。",
r"\(a=2,\ b=-3,\ c=2,\ \lambda_0=1\)。",
r"<p>由 \(A^{*}\alpha=\lambda_0\alpha\)，两边左乘 \(A\) 并利用 \(AA^{*}=|A|E=-E\)，得 \(-\alpha=\lambda_0 A\alpha\)，即 \(A\alpha=-\frac{1}{\lambda_0}\alpha\)，故 \(\alpha\) 也是 \(A\) 的特征向量。设 \(A\alpha=\mu\alpha\)，计算 \(A\alpha=(1-a+c,\ -2-b,\ c-1-a)^{\top}\)。由第 1、3 分量相等：\(1-a+c=-(c-1-a)\)，化简得 \(c=a\)；于是 \(\mu=c-1-a=-1\)，从而 \(\lambda_0=-1/\mu=1\)；由第 2 分量 \(-2-b=-\mu=1\) 得 \(b=-3\)。最后由 \(|A|=-1\)：当 \(c=a\) 时直接展开得 \(|A|=-ab-2a-3=-1\)，即 \(a(b+2)=-2\)，代入 \(b=-3\) 得 \(a=2\)，故 \(c=2\)。综上 \(a=2,\ b=-3,\ c=2,\ \lambda_0=1\)。</p>"))

items.append(e("同步练习13", "solve", 3, "幂零矩阵特征值", 2, 8,
r"设 \(\alpha=(a_1,a_2,\dots,a_n)^{\top}\)，\(\beta=(b_1,b_2,\dots,b_n)^{\top}\) 均为非零向量，且 \(\alpha^{\top}\beta=0\)。设 \(A=\alpha\beta^{\top}\)，求：(1) \(A^2\)；(2) 矩阵 \(A\) 的特征值和特征向量。",
r"\(A^2=O\)；\(A\) 的特征值全为 0，特征向量为满足 \(\beta^{\top}x=0\) 的全部非零向量。",
r"<p>(1) \(A^2=(\alpha\beta^{\top})(\alpha\beta^{\top})=\alpha(\beta^{\top}\alpha)\beta^{\top}\)。由 \(\alpha^{\top}\beta=0\) 知 \(\beta^{\top}\alpha=0\)，故 \(A^2=O\)。</p><p>(2) 因 \(\alpha,\beta\) 均非零，\(R(A)=R(\alpha\beta^{\top})=1\)，故 \(A\) 有 \(n-1\) 个特征值为 0，最后一个特征值为迹：\(\operatorname{tr}(A)=\beta^{\top}\alpha=0\)，即 \(A\) 的特征值全为 0。属于 0 的特征向量即 \(Ax=0\) 的非零解：由 \(\alpha\neq0\) 知 \(Ax=\alpha(\beta^{\top}x)=0\iff\beta^{\top}x=0\)，故 \(A\) 的特征向量为齐次方程组 \(b_1x_1+b_2x_2+\dots+b_nx_n=0\) 的全部非零解，其基础解系含 \(n-1\) 个向量。</p>"))

items.append(e("同步练习14", "solve", 3, "相似对角化构造 B", 3, 8,
r"已知 3 阶矩阵 \(A\) 与 3 维向量 \(x\)，向量 \(x,Ax,A^2x\) 线性无关，且满足 \(A^3x=3Ax-2A^2x\)。(1) 记 \(P=(x,Ax,A^2x)\)，求矩阵 \(B\)，使得 \(A=PBP^{-1}\)；(2) 求 \(|A+E|\) 的值。",
r"\(B=\begin{pmatrix}0&0&0\\1&0&-2\\0&1&3\end{pmatrix}\)；\(|A+E|=6\)。",
r"<p>(1) \(AP=(Ax,\ A^2x,\ A^3x)\)。将 \(Ax,A^2x,A^3x\) 用 \(P\) 的列 \(x,Ax,A^2x\) 表示：\(Ax=0\cdot x+1\cdot Ax+0\cdot A^2x\)，\(A^2x=0\cdot x+0\cdot Ax+1\cdot A^2x\)，\(A^3x=3Ax-2A^2x=0\cdot x+3\cdot Ax-2\cdot A^2x\)，故</p><div class=\"fml\">$$AP=P\begin{pmatrix}0&0&0\\1&0&-2\\0&1&3\end{pmatrix},\qquad B=\begin{pmatrix}0&0&0\\1&0&-2\\0&1&3\end{pmatrix}.$$</div><p>(2) 由 \(A=PBP^{-1}\) 知 \(A\sim B\)，故 \(A+E\sim B+E\)，从而 \(|A+E|=|B+E|=\begin{vmatrix}1&0&0\\1&1&-2\\0&1&4\end{vmatrix}=1\times(1\times4-(-2)\times1)=6\)。</p>"))

items.append(e("同步练习15", "solve", 3, "对角化判定与求解", 2, 8,
r"判别下列矩阵能否对角化，并在可以对角化时，求可逆矩阵 \(P\) 使得 \(P^{-1}AP=\Lambda\) 为对角阵。<br>(1) \(A=\begin{pmatrix}1&2&-3\\-1&4&-3\\1&-2&5\end{pmatrix}\)；　(2) \(B=\begin{pmatrix}1&1&0\\0&2&1\\0&0&1\end{pmatrix}\)。",
r"(1) 能，\(P=\begin{pmatrix}2&-3&-1\\1&0&-1\\0&1&1\end{pmatrix}\)，\(P^{-1}AP=\operatorname{diag}(2,2,6)\)；(2) 不能。",
r"<p>(1) \(|A-\lambda E|=-(\lambda-2)^2(\lambda-6)\)，特征值 \(\lambda_{1,2}=2\)，\(\lambda_3=6\)。对二重特征值 2，\(A-2E=\begin{pmatrix}-1&2&-3\\-1&2&-3\\1&-2&3\end{pmatrix}\)，\(R(A-2E)=1\)，属于 2 的线性无关特征向量有 \(3-1=2\) 个，等于代数重数，故 \(A\) 可对角化。解得属于 2 的特征向量 \(\xi_1=(2,1,0)^{\top}\)，\(\xi_2=(-3,0,1)^{\top}\)；属于 6 的特征向量 \(\xi_3=(-1,-1,1)^{\top}\)。取 \(P=(\xi_1,\xi_2,\xi_3)\)，则 \(P^{-1}AP=\operatorname{diag}(2,2,6)\)。</p><p>(2) \(B\) 为上三角阵，特征值 \(1,1,2\)。对二重特征值 1，\(B-E=\begin{pmatrix}0&1&0\\0&1&1\\0&0&0\end{pmatrix}\)，\(R(B-E)=2\)，属于 1 的线性无关特征向量只有 \(3-2=1\) 个，少于代数重数 2，故 \(B\) 不能相似对角化。</p>"))

items.append(e("同步练习16", "solve", 3, "正交相似对角化", 2, 8,
r"试求正交矩阵 \(Q\) 及对角阵 \(\Lambda\)，使 \(Q^{-1}AQ=\Lambda\)，其中 \(\Lambda\) 为对角阵。<br>(1) \(A=\begin{pmatrix}0&-1&1\\-1&0&1\\1&1&0\end{pmatrix}\)；　(2) \(A=\begin{pmatrix}1&-2&-4\\-2&4&-2\\-4&-2&1\end{pmatrix}\)。",
r"(1) \(Q=\begin{pmatrix}-\frac1{\sqrt2}&\frac1{\sqrt6}&\frac1{\sqrt5}\\\frac1{\sqrt2}&\frac1{\sqrt6}&\frac2{\sqrt5}\\0&\frac2{\sqrt6}&0\end{pmatrix}\)，\(\Lambda=\operatorname{diag}(1,1,-2)\)；(2) \(Q=\begin{pmatrix}\frac1{\sqrt5}&\frac4{3\sqrt5}&\frac1{\sqrt2}\\-\frac2{\sqrt5}&\frac2{3\sqrt5}&0\\0&-\frac5{3\sqrt5}&-\frac1{\sqrt2}\end{pmatrix}\)，\(\Lambda=\operatorname{diag}(5,5,-4)\)。",
r"<p>(1) \(|A-\lambda E|=-(\lambda-1)^2(\lambda+2)\)，特征值 \(\lambda_{1,2}=1\)，\(\lambda_3=-2\)。属于 1 的线性无关特征向量为 \(\xi_1=(-1,1,0)^{\top}\)，\(\xi_2=(1,0,1)^{\top}\)，二者不正交，Schmidt 正交化并单位化得 \(\eta_1=\frac1{\sqrt2}(-1,1,0)^{\top}\)，\(\eta_2=\frac1{\sqrt6}(1,1,2)^{\top}\)；属于 \(-2\) 的特征向量 \(\xi_3=(1,2,0)^{\top}\)，单位化 \(\eta_3=\frac1{\sqrt5}(1,2,0)^{\top}\)。于是</p><div class=\"fml\">$$Q=(\eta_1,\eta_2,\eta_3)=\begin{pmatrix}-\frac1{\sqrt2}&\frac1{\sqrt6}&\frac1{\sqrt5}\\\frac1{\sqrt2}&\frac1{\sqrt6}&\frac2{\sqrt5}\\0&\frac2{\sqrt6}&0\end{pmatrix},\qquad \Lambda=\operatorname{diag}(1,1,-2).$$</div><p>(2) \(|A-\lambda E|=-(\lambda-5)^2(\lambda+4)\)，特征值 \(\lambda_{1,2}=5\)，\(\lambda_3=-4\)。属于 5 的特征向量 \(\xi_1=(1,-2,0)^{\top}\)，\(\xi_2=(1,0,-1)^{\top}\)，正交化：\(\eta_1=\frac1{\sqrt5}(1,-2,0)^{\top}\)，\(\eta_2=\frac1{3\sqrt5}(4,2,-5)^{\top}\)；属于 \(-4\) 的特征向量 \(\xi_3=(1,0,-1)^{\top}\)，单位化 \(\eta_3=\frac1{\sqrt2}(1,0,-1)^{\top}\)。于是</p><div class=\"fml\">$$Q=\begin{pmatrix}\frac1{\sqrt5}&\frac4{3\sqrt5}&\frac1{\sqrt2}\\-\frac2{\sqrt5}&\frac2{3\sqrt5}&0\\0&-\frac5{3\sqrt5}&-\frac1{\sqrt2}\end{pmatrix},\qquad \Lambda=\operatorname{diag}(5,5,-4).$$</div><p>方法点评：实对称矩阵必可用正交阵对角化；重特征值的特征向量须先 Schmidt 正交化再单位化。</p>"))

items.append(e("同步练习17", "solve", 3, "特殊矩阵的特征值", 2, 8,
r"已知 \(A=\begin{pmatrix}n&1&\cdots&1\\1&n&\cdots&1\\\vdots&\vdots&&\vdots\\1&1&\cdots&n\end{pmatrix}\) 是 \(n\) 阶矩阵，求 \(A\) 的特征值，并求可逆矩阵 \(P\)，使得 \(P^{-1}AP=\Lambda\) 为对角阵。",
r"特征值为 \(2n-1\)（1 重）与 \(n-1\)（\(n-1\) 重）；\(P=(\xi_1,\xi_2,\dots,\xi_n)\)，\(\xi_1=(1,\dots,1)^{\top}\)，\(\xi_i=(1,0,\dots,0,-1,\dots,0)^{\top}\)（第 \(i\) 个分量为 \(-1\)）。",
r"<p>设 \(J\) 为全 1 矩阵，则 \(A=(n-1)E+J\)。\(R(J)=1\)，\(J\) 的特征值为 \(n\)（对应特征向量 \(\xi_1=(1,1,\dots,1)^{\top}\)）与 \(0\)（\(n-1\) 重）。故 \(A\) 的特征值为 \(\lambda_1=(n-1)+n=2n-1\)（对应特征向量仍为 \(\xi_1\)）与 \(\lambda_2=\dots=\lambda_n=(n-1)+0=n-1\)（对应特征向量为与 \(\xi_1\) 正交的非零向量）。取</p><div class=\"fml\">$$\xi_2=(1,-1,0,\dots,0)^{\top},\ \xi_3=(1,0,-1,\dots,0)^{\top},\ \dots,\ \xi_n=(1,0,\dots,0,-1)^{\top},$$</div><p>它们线性无关且都是属于 \(n-1\) 的特征向量。令 \(P=(\xi_1,\xi_2,\dots,\xi_n)\)，则 \(P\) 可逆，且 \(P^{-1}AP=\operatorname{diag}(2n-1,n-1,\dots,n-1)\)。</p>"))

items.append(e("同步练习18", "solve", 3, "秩一矩阵相似对角化", 2, 8,
r"设 \(\alpha=(1,1,1)^{\top}\)，\(\beta=(1,0,k)^{\top}\)，若 \(\alpha\beta^{\top}\) 相似于 \(\begin{pmatrix}3&0&0\\0&0&0\\0&0&0\end{pmatrix}\)，求 \(k\) 的值。",
r"\(k=2\)。",
r"<p>\(\alpha\beta^{\top}=\begin{pmatrix}1&0&k\\1&0&k\\1&0&k\end{pmatrix}\)，\(R(\alpha\beta^{\top})=1\)，故其特征值为迹 \(\operatorname{tr}(\alpha\beta^{\top})=1+0+k=1+k\) 与 \(0,0\)。相似矩阵有相同的特征值，故 \(1+k=3\)，即 \(k=2\)。</p>"))

items.append(e("同步练习19", "solve", 3, "正交阵与代数余子式", 3, 8,
r"设 3 阶方阵 \(A=(a_{ij})\) 是正交矩阵，且 \(a_{ij}=A_{ij}\)（其中 \(A_{ij}\) 是 \(a_{ij}\) 的代数余子式），且 \(a_{33}=-1\)，求 \(Ax=(0,0,1)^{\top}\) 的解。",
r"\(x=(0,0,-1)^{\top}\)。",
r"<p>由 \(a_{ij}=A_{ij}\) 知 \(A^{\top}=A^{*}\)。由 \(A\) 正交得 \(E=AA^{\top}=AA^{*}=|A|E\)，故 \(|A|=1\)。由 \(A^{\top}A=E\) 知 \(A\) 的行向量组为单位向量组：第三行 \((a_{31},a_{32},a_{33})\) 满足 \(a_{31}^2+a_{32}^2+1=1\)，故 \(a_{31}=a_{32}=0\)；同理列向量为单位向量，第三列 \((a_{13},a_{23},a_{33})^{\top}\) 满足 \(a_{13}=a_{23}=0\)。于是 \(A=\begin{pmatrix}a_{11}&a_{12}&0\\a_{21}&a_{22}&0\\0&0&-1\end{pmatrix}\)。由 \(A\) 可逆，\(x=A^{-1}(0,0,1)^{\top}=A^{\top}(0,0,1)^{\top}\)（正交阵的逆即转置），而 \(A^{\top}(0,0,1)^{\top}\) 是 \(A^{\top}\) 的第三列，即 \(A\) 的第三行，故 \(x=(0,0,-1)^{\top}\)。</p>"))

items.append(e("同步练习20", "solve", 3, "幂等矩阵行列式", 2, 8,
r"设 \(A\) 为 \(n\) 阶实对称矩阵，且满足 \(A^2=A\)，\(R(A)=r\)（\(0&lt;r&lt;n\)），求 \(\left|E+A+A^2+\dots+A^{2006}\right|\)。",
r"\(2007^r\)。",
r"<p>设 \(Ax=\lambda x\)（\(x\neq0\)），由 \(A^2=A\) 得 \(\lambda^2=\lambda\)，故 \(A\) 的特征值只能是 0 或 1。\(A\) 为实对称矩阵必可对角化，且 \(R(A)=r\) 说明特征值 1 恰有 \(r\) 个（线性无关特征向量恰 \(r\) 个），0 有 \(n-r\) 个。对 \(f(A)=E+A+A^2+\dots+A^{2006}\)：特征值 1 对应 \(1+\underbrace{1+\dots+1}_{2006}=2007\)；特征值 0 对应 \(1+0+\dots+0=1\)。故 \(f(A)\) 的特征值为 2007（\(r\) 个）与 1（\(n-r\) 个），行列式等于特征值之积：\(\left|E+A+\dots+A^{2006}\right|=2007^r\)。</p>"))

items.append(e("同步练习21", "solve", 3, "抽象矩阵特征值", 3, 8,
r"已知 \(A\) 是 3 阶矩阵，\(\alpha_1,\alpha_2,\alpha_3\) 是线性无关的 3 维列向量，满足 \(A\alpha_1=-\alpha_1-3\alpha_2-3\alpha_3\)，\(A\alpha_2=4\alpha_1+4\alpha_2+\alpha_3\)，\(A\alpha_3=-2\alpha_1+3\alpha_3\)。(1) 求矩阵 \(A\) 的特征值；(2) 求矩阵 \(A\) 的特征向量；(3) 求矩阵 \(A^{*}-6E\) 的秩。",
r"(1) 特征值为 \(1,2,3\)；(2) 特征向量为 \(\alpha_1+\alpha_2+\alpha_3\)，\(2\alpha_1+3\alpha_2+3\alpha_3\)，\(\alpha_1+3\alpha_2+4\alpha_3\)；(3) \(R(A^{*}-6E)=2\)。",
r"<p>(1) 由题设 \(A(\alpha_1,\alpha_2,\alpha_3)=(\alpha_1,\alpha_2,\alpha_3)B\)，其中 \(B=\begin{pmatrix}-1&4&-2\\-3&4&0\\-3&1&3\end{pmatrix}\)。记 \(P=(\alpha_1,\alpha_2,\alpha_3)\)，则 \(P\) 可逆且 \(P^{-1}AP=B\)，故 \(A\sim B\)。计算 \(|B-\lambda E|=-(\lambda-1)(\lambda-2)(\lambda-3)\)，故 \(A\) 的特征值为 \(1,2,3\)。</p><p>(2) 分别解 \((B-E)y=0\)、\((B-2E)y=0\)、\((B-3E)y=0\)，得基础解系 \(y_1=(1,1,1)^{\top}\)，\(y_2=(2,3,3)^{\top}\)，\(y_3=(1,3,4)^{\top}\)。由 \(P^{-1}AP=B\) 知 \(A\) 的属于 \(\lambda_i\) 的特征向量为 \(Py_i\)，故 \(A\) 的特征向量为：属于 1 的 \(k(\alpha_1+\alpha_2+\alpha_3)\)，属于 2 的 \(k(2\alpha_1+3\alpha_2+3\alpha_3)\)，属于 3 的 \(k(\alpha_1+3\alpha_2+4\alpha_3)\)（\(k\neq0\)）。</p><p>(3) \(|A|=|B|=1\times2\times3=6\)，故 \(A^{*}=|A|A^{-1}\) 的特征值为 \(6,3,2\)，从而 \(A^{*}-6E\) 的特征值为 \(0,-3,-4\)。其行列式 \(=0\times(-3)\times(-4)=0\)，故 \(A^{*}-6E\) 不可逆；而它恰有一个特征值为 0，其余 \(-3,-4\) 非零，相似于 \(\operatorname{diag}(0,-3,-4)\)，故 \(R(A^{*}-6E)=2\)。</p>"))

items.append(e("同步练习22", "proof", 3, "相似矩阵的证明", 2, 8,
r"证明：\(n\) 阶矩阵 \(\begin{pmatrix}1&1&\cdots&1\\1&1&\cdots&1\\\vdots&\vdots&&\vdots\\1&1&\cdots&1\end{pmatrix}\) 与 \(\begin{pmatrix}0&0&\cdots&1\\0&0&\cdots&2\\\vdots&\vdots&&\vdots\\0&0&\cdots&n\end{pmatrix}\) 相似。",
r"两者都相似于 \(\operatorname{diag}(n,0,\dots,0)\)，故彼此相似。",
r"<p>记 \(J\) 为全 1 矩阵，\(M\) 为第二个矩阵（仅第 \(n\) 列为 \((1,2,\dots,n)^{\top}\)，其余元素全为 0）。\(J\) 的特征值为 \(n\)（1 重，对应特征向量 \((1,\dots,1)^{\top}\)）与 \(0\)（\(n-1\) 重），且 \(R(J)=1\)，故属于 0 的线性无关特征向量有 \(n-1\) 个，\(J\) 可对角化，\(J\sim\operatorname{diag}(n,0,\dots,0)\)。\(M\) 为上三角矩阵，特征值为 \(0,\dots,0,n\)（对角元中仅第 \(n\) 个为 \(n\)）；\(R(M)=1\)（仅第 \(n\) 列非零），故属于 0 的线性无关特征向量有 \(n-1\) 个，\(M\) 也可对角化，\(M\sim\operatorname{diag}(n,0,\dots,0)\)。由相似关系的对称性与传递性，\(J\sim M\)，命题得证。</p>"))

items.append(e("同步练习23", "solve", 3, "实对称正交对角化", 2, 8,
r"设 3 阶实对称矩阵 \(A\) 的各行元素之和均为 3，向量 \(\alpha_1=(-1,2,-1)^{\top}\)，\(\alpha_2=(0,-1,1)^{\top}\) 是线性方程组 \(Ax=0\) 的两个解。(1) 求 \(A\) 的特征值与特征向量；(2) 求正交矩阵 \(Q\) 和对角阵 \(\Lambda\)，使得 \(Q^{-1}AQ=\Lambda\)。",
r"(1) 特征值 \(3,0,0\)；属于 3 的特征向量为 \(k(1,1,1)^{\top}\)，属于 0 的特征向量为 \(k_1\alpha_1+k_2\alpha_2\)（不全为零）；(2) \(Q=\begin{pmatrix}-\frac1{\sqrt6}&-\frac1{\sqrt2}&\frac1{\sqrt3}\\\frac2{\sqrt6}&0&\frac1{\sqrt3}\\-\frac1{\sqrt6}&\frac1{\sqrt2}&\frac1{\sqrt3}\end{pmatrix}\)，\(\Lambda=\operatorname{diag}(0,0,3)\)。",
r"<p>(1) 各行元素之和均为 3，即 \(A(1,1,1)^{\top}=3(1,1,1)^{\top}\)，故 \(\lambda_1=3\) 是 \(A\) 的特征值，对应特征向量为 \((1,1,1)^{\top}\)。又 \(A\alpha_1=0\)，\(A\alpha_2=0\)，且 \(\alpha_1,\alpha_2\) 线性无关，故 0 是 \(A\) 的（至少二重的）特征值。3 阶实对称矩阵恰有 3 个线性无关的特征向量，故 \(A\) 的特征值为 \(\lambda_1=3\)，\(\lambda_2=\lambda_3=0\)；属于 3 的特征向量为 \(k(1,1,1)^{\top}\)（\(k\neq0\)），属于 0 的特征向量为 \(k_1(-1,2,-1)^{\top}+k_2(0,-1,1)^{\top}\)（\(k_1,k_2\) 不全为零）。</p><p>(2) 将属于 0 的两个特征向量 Schmidt 正交化：\(\beta_1=\alpha_1=(-1,2,-1)^{\top}\)；\(\beta_2=\alpha_2-\frac{\alpha_2^{\top}\beta_1}{\beta_1^{\top}\beta_1}\beta_1=(0,-1,1)^{\top}+\frac12(-1,2,-1)^{\top}=\left(-\frac12,0,\frac12\right)^{\top}\)，取 \(\beta_2=(-1,0,1)^{\top}\)。与 \((1,1,1)^{\top}\) 相互正交（实对称阵不同特征值的特征向量必正交）。单位化得 \(\eta_1=\frac1{\sqrt6}(-1,2,-1)^{\top}\)，\(\eta_2=\frac1{\sqrt2}(-1,0,1)^{\top}\)，\(\eta_3=\frac1{\sqrt3}(1,1,1)^{\top}\)。于是</p><div class=\"fml\">$$Q=(\eta_1,\eta_2,\eta_3)=\begin{pmatrix}-\frac1{\sqrt6}&-\frac1{\sqrt2}&\frac1{\sqrt3}\\\frac2{\sqrt6}&0&\frac1{\sqrt3}\\-\frac1{\sqrt6}&\frac1{\sqrt2}&\frac1{\sqrt3}\end{pmatrix},\qquad \Lambda=\operatorname{diag}(0,0,3),$$</div><p>满足 \(Q^{-1}AQ=\Lambda\)。</p>"))

with io.open(r"D:\Web\XD_learn\tools\batch\guide_g7b.json", "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=1)
print("total:", len(items))
from collections import Counter
print(Counter(x["ty"] for x in items))
