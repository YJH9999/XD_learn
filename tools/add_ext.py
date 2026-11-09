# -*- coding: utf-8 -*-
"""向各小节追加「拓展 · 可能考」块 + 复习题追加「题型细节考点」块"""
import re

EXT = {}

EXT['1-1-矩阵概述'] = r'''
<details class="ext"><summary>拓展 · 可能考<span class="ext-tag">考前加分</span></summary><div class="ext-b">
  <p><strong>① \(A^{\top}A=O \Rightarrow A=O\)（实矩阵，常考小证明）</strong>：\((A^{\top}A)_{ii}\) 恰是 \(A\) 第 \(i\) 列各元素的平方和 \(\sum_k a_{ki}^2=0\)，故每列全零，\(A=O\)。注意复数域不成立（如 \(\begin{pmatrix}1&\mathrm{i}\\\mathrm{i}&-1\end{pmatrix}\)）。</p>
  <p><strong>② 对称 + 反对称分解唯一</strong>：任意方阵 \(A=\underbrace{\tfrac{A+A^{\top}}2}_{\text{对称}}+\underbrace{\tfrac{A-A^{\top}}2}_{\text{反对称}}\)。若 \(A=S+K\) 是另一种分解，则 \(S-S'=K'-K\)，左边对称、右边反对称，两边只能同时为零矩阵。</p>
  <p><strong>③ 展开陷阱</strong>：\((A+B)^2=A^2+AB+BA+B^2\)，只有 \(AB=BA\) 时才能写成 \(A^2+2AB+B^2\)；同理 \((A+B)(A-B)\ne A^2-B^2\)。</p>
</div></details>
'''

EXT['1-2-逆矩阵和行列式'] = r'''
<details class="ext"><summary>拓展 · 可能考<span class="ext-tag">考前加分</span></summary><div class="ext-b">
  <p><strong>① 幂零矩阵的可逆公式（高频小证明）</strong>：若 \(A^k=O\)，则 \((E-A)(E+A+A^2+\cdots+A^{k-1})=E-A^k=E\)，故 \(E-A\) 可逆且 \((E-A)^{-1}=E+A+\cdots+A^{k-1}\)。特别地 \(A^2=O \Rightarrow (E-A)^{-1}=E+A\)。</p>
  <p><strong>② 对合矩阵</strong>：\(A^2=E \Rightarrow A^{-1}=A\)，且 \(E-A\) 与 \(E+A\) 满足 \((E-A)(E+A)=O\)，结合零因子不等式得 \(R(E-A)+R(E+A)\le n\)。</p>
  <p><strong>③ \(\operatorname{tr}(AB)=\operatorname{tr}(BA)\) 及推论</strong>：\(\sum_i\sum_k a_{ik}b_{ki}=\sum_k\sum_i b_{ki}a_{ik}\)。推论：\(AB-BA=E\) 无解（左边迹为 \(0\)，右边迹为 \(n\)），这是判断题常客。</p>
  <p><strong>④ 数乘行列式</strong>：\(|kA|=k^n|A|\)（每行都乘 \(k\)，共提出 \(n\) 次），\(n=3\) 时 \(|2A|=8|A|\) 别算成 \(2|A|\)。</p>
</div></details>
'''

EXT['1-3-行列式的性质与应用'] = r'''
<details class="ext"><summary>拓展 · 可能考<span class="ext-tag">考前加分</span></summary><div class="ext-b">
  <p><strong>① 分块三角行列式</strong>：\(\begin{vmatrix}A&O\\C&B\end{vmatrix}=\begin{vmatrix}A&B\\O&C\end{vmatrix}=|A||C|\)，\(\begin{vmatrix}O&A\\C&B\end{vmatrix}=(-1)^{mn}|A||C|\)（\(m,n\) 为 \(A,C\) 的阶数，换位因子别丢）。</p>
  <p><strong>② 倍加不变性的证明思路</strong>：把"第 \(j\) 列加 \(k\) 倍第 \(i\) 列"按第 \(j\) 列拆成两个行列式，第二个中第 \(i,j\) 两列成比例，行列式为 \(0\)，故值不变。</p>
  <p><strong>③ 奇数阶反对称行列式必为 0</strong>：\(|A|=|A^{\top}|=|-A|=(-1)^n|A|=-|A|\)（\(n\) 奇数），得 \(|A|=0\)。判断题高频。</p>
  <p><strong>④ 范德蒙行列式</strong> \(\prod_{1\le i&lt;j\le n}(x_j-x_i)\)：归纳法——第 1 列减第 2 列、逐列减，提出公因子 \((x_1-x_2)\cdots\) 后降阶。</p>
</div></details>
'''

EXT['1-4-矩阵的初等变换'] = r'''
<details class="ext"><summary>拓展 · 可能考<span class="ext-tag">考前加分</span></summary><div class="ext-b">
  <p><strong>① 初等矩阵的逆仍为同型初等矩阵</strong>：\(E(i,j)^{-1}=E(i,j)\)（换行两遍还原）、\(E(i(c))^{-1}=E(i(1/c))\)、\(E(i,j(k))^{-1}=E(i,j(-k))\)。填空题常考 \(E(i,j(1))^{-1}=E(i,j(-1))\)。</p>
  <p><strong>② 初等矩阵的幂</strong>：\(E(i,j)^m\in\{E,E(i,j)\}\)；\(E(i,j(k))^2=E(i,j(2k))\)（连续两次把 \(j\) 行的 \(k\) 倍加到 \(i\) 行）。</p>
  <p><strong>③ "可逆 ⇔ 初等矩阵之积"的证明思路</strong>：\((A\mid E)\xrightarrow{\text{行变换}}(E\mid A^{-1})\)，行变换即左乘初等矩阵，故 \(A^{-1}=P_1\cdots P_t\)，取逆得 \(A=P_t^{-1}\cdots P_1^{-1}\)。</p>
  <p><strong>④ \(PAQ=B\Rightarrow R(A)=R(B)\)</strong>：可逆矩阵乘法不改变秩（初等变换保秩），反之秩相同只是方阵等价的充要条件（一般矩阵还需考虑形状）。</p>
</div></details>
'''

EXT['1-5-矩阵的秩和线性方程组'] = r'''
<details class="ext"><summary>拓展 · 可能考<span class="ext-tag">考前加分</span></summary><div class="ext-b">
  <p><strong>① 秩不等式全家福（证明题常考前两条）</strong>：\(R(A+B)\le R(A)+R(B)\)（\(A+B\) 的列可由 \((A,B)\) 的列线性表示）；\(AB=O\Rightarrow R(A)+R(B)\le n\)（\(B\) 的每列都是 \(Ax=0\) 的解，解空间维数 \(n-R(A)\) 装得下 \(R(B)\)）；\(R(A)+R(B)\le n+R(AB)\)（零因子不等式，用分块矩阵 \(\begin{pmatrix}A&AB\\O&B\end{pmatrix}\) 两种方式算秩）。</p>
  <p><strong>② 秩 1 矩阵分解（高次幂专用）</strong>：\(R(A)=1\iff A=\alpha\beta^{\top}\)（\(\alpha,\beta\) 非零列向量），此时 \(A^m=(\beta^{\top}\alpha)^{m-1}A=(\operatorname{tr}A)^{m-1}A\)。</p>
  <p><strong>③ 行秩 = 列秩</strong>：\(R(A^{\top})=R(A)\)，这是"按行变换算秩"与"按列取极大无关组"能混用的根本原因。</p>
</div></details>
'''

EXT['1-6-分块矩阵'] = r'''
<details class="ext"><summary>拓展 · 可能考<span class="ext-tag">考前加分</span></summary><div class="ext-b">
  <p><strong>① 分块对角阵的速算</strong>：\(\operatorname{diag}(A,B)^k=\operatorname{diag}(A^k,B^k)\)；\(|\operatorname{diag}(A,B)|=|A||B|\)；特征值 = 两块特征值的并集（由 \(\det(\operatorname{diag}(A,B)-\lambda E)=|A-\lambda E|\,|B-\lambda E|\) 直接得到），填空题秒杀用。</p>
  <p><strong>② 换位行列式的阶数符号</strong>：\(\begin{vmatrix}O&A_{m\times m}\\B_{n\times n}&O\end{vmatrix}=(-1)^{mn}|A||B|\)——把 \(B\) 从最下面挪到最上面需要 \(mn\) 次相邻行交换。</p>
  <p><strong>③ 分块乘法的兼容条件</strong>：\(A_{m\times s}B_{s\times n}\) 按列分块时 \(A(\beta_1,\dots,\beta_n)=(A\beta_1,\dots,A\beta_n)\)——"A 左乘 = 对每列分别作用"，是很多抽象证明的基本功。</p>
</div></details>
'''

EXT['1-7-矩阵应用举例'] = r'''
<details class="ext"><summary>拓展 · 可能考<span class="ext-tag">考前加分</span></summary><div class="ext-b">
  <p><strong>① 矩阵方程的通用解法链</strong>：\(AX=B\) 当 \(A\) 可逆时 \(X=A^{-1}B\)；\(A\) 不可逆（或 \(m\ne n\)）时设 \(X\) 的列 \(x_i\) 逐列解 \(Ax_i=b_i\)。抽象关系式求逆时，目标永远是<strong>凑出 \(X\) 并把系数矩阵化为 \(E\)</strong>（如 \(A^2B-A-B=E \Rightarrow (A^2-E)B=A+E\)，再检验 \(A^2-E\) 是否可逆）。</p>
  <p><strong>② 自由变量的实际含义</strong>：应用题中 \(n-R(A)\) 个自由变量对应系统的"自由度"，取不同值得到的解族在交通流/配平问题中就是可行方案族——考试只需写通解并说明参数意义。</p>
  <p><strong>③ 叠加原理</strong>：若 \(\eta\) 是 \(Ax=b\) 的解、\(\xi\) 是 \(Ax=0\) 的解，则 \(\eta+\xi\) 仍是 \(Ax=b\) 的解——"特解 + 齐次通解"结构在应用题里就是"基准方案 + 调整方案"。</p>
</div></details>
'''

EXT['2-1-向量及其线性相关性'] = r'''
<details class="ext"><summary>拓展 · 可能考<span class="ext-tag">考前加分</span></summary><div class="ext-b">
  <p><strong>① 延长向量组保持无关（常考小证明）</strong>：若 \(\alpha_1,\dots,\alpha_s\)（\(n\) 维）线性无关，各添一个分量后仍无关。证明：\(\sum c_i\beta_i=0\) 的前 \(n\) 个分量给出 \(\sum c_i\alpha_i=0\)，由原组无关得 \(c_i\) 全零。反之"截短可能变相关"。</p>
  <p><strong>② \(s&gt;n\) 必相关的证明</strong>：以 \(\alpha_i\) 为列的齐次方程组 \(Ax=0\) 有 \(n\) 个方程、\(s\) 个未知数，未知数多于方程必有无穷多解即非零解。</p>
  <p><strong>③ 速判三条</strong>：单个向量相关 ⟺ 是零向量；两个向量相关 ⟺ 对应分量成比例；含零向量的向量组必相关。</p>
</div></details>
'''

EXT['2-2-向量空间'] = r'''
<details class="ext"><summary>拓展 · 可能考<span class="ext-tag">考前加分</span></summary><div class="ext-b">
  <p><strong>① 子空间判定就两条</strong>：非空 + 对线性运算封闭（加法、数乘各一条）。验证 \(V_1+V_2\)、\(V_1\cap V_2\) 是子空间是填空/判断常客；注意 \(V_1\cup V_2\) 一般<strong>不是</strong>子空间（封闭性破坏）。</p>
  <p><strong>② 生成子空间</strong>：\(L(\alpha_1,\dots,\alpha_s)\) 的维数 = 该向量组的秩（极大无关组即它的基）。</p>
  <p><strong>③ 维数与相等</strong>：\(V_1\subseteq V_2\Rightarrow \dim V_1\le\dim V_2\)；且 \(V_1\subseteq V_2\) 与维数相等<strong>合起来</strong>才推出 \(V_1=V_2\)——单凭 \(\dim V_1=\dim V_2\) 推不出相等（\(x\) 轴与 \(y\) 轴都是 1 维）。</p>
</div></details>
'''

EXT['2-3-线性方程组解的结构'] = r'''
<details class="ext"><summary>拓展 · 可能考<span class="ext-tag">考前加分</span></summary><div class="ext-b">
  <p><strong>① 两个非齐次解之差是齐次解</strong>：\(A\eta_1=A\eta_2=b\Rightarrow A(\eta_1-\eta_2)=0\)。由此立刻得到：\(\eta_1,\eta_2\) 的线性组合 \(k_1\eta_1+k_2\eta_2\) 仍是 \(Ax=b\) 的解 \(\iff k_1+k_2=1\)（填空高频）。</p>
  <p><strong>② 解的重构技巧</strong>：已知 \(Ax=b\) 的两个解 \(\eta_1,\eta_2\) 与 \(R(A)=n-1\)，则基础解系可取 \(\eta_1-\eta_2\)，通解 \(=\eta_1+c(\eta_1-\eta_2)\)——"特解不必在题给解里挑，差向量当齐次解用"。</p>
  <p><strong>③ 公共解的三种求法</strong>已在正文；补一句记忆：两齐次方程组公共解 = 联立新方程组；一齐一非齐公共解 = 把齐次通解代入非齐次验证。</p>
</div></details>
'''

EXT['2-4-简单最小二乘问题'] = r'''
<details class="ext"><summary>拓展 · 可能考<span class="ext-tag">考前加分</span></summary><div class="ext-b">
  <p><strong>① 投影矩阵的两大性质（小证明）</strong>：\(P=A(A^{\top}A)^{-1}A^{\top}\) 满足 \(P^{\top}=P\)（\((A^{\top}A)^{-1}\) 对称）与 \(P^2=P\)（中间 \(A^{\top}A\) 约掉）。幂等对称矩阵 = 正交投影算子。</p>
  <p><strong>② 正规方程的几何语言</strong>：\(A^{\top}(b-Ax^*)=0\) 说明残差 \(b-Ax^*\) 与 \(A\) 的每一列正交，即 \(b\) 的最小二乘解 = 把 \(b\) 正交投影到列空间 \(R(A)\)。</p>
  <p><strong>③ 直线拟合的落地形式</strong>：拟合 \(y=at+b\) 时 \(A\) 的两列是 \((x_1,\dots,x_n)^{\top}\) 和 \((1,\dots,1)^{\top}\)，未知量 \(z=(a,b)^{\top}\)——数据点个数为 \(n\)，正规方程是 \(2\times2\) 的。</p>
</div></details>
'''

EXT['3-1-基变换和坐标变换'] = r'''
<details class="ext"><summary>拓展 · 可能考<span class="ext-tag">考前加分</span></summary><div class="ext-b">
  <p><strong>① 过渡矩阵必可逆</strong>：两组基等价（互相线性表示）⟹ \(C\) 可逆；反之可逆的 \(C\) 把基变成基。判断题常考。</p>
  <p><strong>② 方向别背反</strong>：\((\beta_1,\dots,\beta_n)=(\alpha_1,\dots,\alpha_n)C\)（新基 = 旧基右乘 \(C\)），坐标满足 \(x_{\alpha}=C\,x_{\beta}\)（旧坐标 = \(C\) 乘新坐标）。检验法：\(C\) 的第 \(j\) 列就是 \(\beta_j\) 在旧基下的坐标。</p>
  <p><strong>③ 求过渡矩阵的固定流程</strong>：对 \((\alpha_1,\dots,\alpha_n\mid\beta_1,\dots,\beta_n)\) 作行变换，把左块化成 \(E\)，右块即 \(A^{-1}B=C\)；最后抽一列验证 \((\alpha)c_j=\beta_j\)。</p>
</div></details>
'''

EXT['3-2-线性变换'] = r'''
<details class="ext"><summary>拓展 · 可能考<span class="ext-tag">考前加分</span></summary><div class="ext-b">
  <p><strong>① 线性变换由基像唯一决定</strong>：若两个线性变换在一组基上的像完全相同，则处处相同——因为任意向量先表示成 \(\sum c_i\alpha_i\)，两边分别作用后逐项相等。这就是"矩阵表示"合理性的来源。</p>
  <p><strong>② 秩-零化度定理</strong>：\(\dim\mathscr{A}(V)+\dim\ker\mathscr{A}=n\)，对应矩阵语言 \(R(A)+n-R(A)=n\)，与 1.5 节解空间维数定理是一回事。</p>
  <p><strong>③ 快速判定非线性变换</strong>：含常数项（如 \(\mathscr{A}x=x+1\)）、取共轭除外、非线性齐次（如平方 \(\mathscr{A}x=x^2\)）都不线性——验证时先查 \(\mathscr{A}(0)=0\) 是否成立最快。</p>
</div></details>
'''

EXT['3-3-相似矩阵'] = r'''
<details class="ext"><summary>拓展 · 可能考<span class="ext-tag">考前加分</span></summary><div class="ext-b">
  <p><strong>① \(\operatorname{tr}(C^{-1}AC)=\operatorname{tr}(A)\)（相似保迹的证明）</strong>：用 \(\operatorname{tr}(XY)=\operatorname{tr}(YX)\)，\(\operatorname{tr}(C^{-1}AC)=\operatorname{tr}(C^{-1}(AC))=\operatorname{tr}((AC)C^{-1})=\operatorname{tr}(A)\)。</p>
  <p><strong>② 特征值相同 ≠ 相似（反例必背）</strong>：\(O\) 与 \(\begin{pmatrix}0&1\\0&0\end{pmatrix}\) 特征值都是 \(0,0\)，但秩 \(0\ne1\)，不相似。判断题最爱挖这个坑。</p>
  <p><strong>③ 相似的几何本质</strong>：\(B=C^{-1}AC\) 表示同一线性变换在两组基下的矩阵——"相似 = 换个角度看同一个变换"，这也是为什么不变量（迹、行列式、秩、特征多项式）恰好都由变换本身决定。</p>
</div></details>
'''

EXT['3-4-矩阵的特征值和特征向量'] = r'''
<details class="ext"><summary>拓展 · 可能考<span class="ext-tag">考前加分</span></summary><div class="ext-b">
  <p><strong>① 特征值速查表（同一特征向量 \(\xi\)，全部直接迁移）</strong>：\(kA\to k\lambda\)，\(A^m\to\lambda^m\)，\(f(A)\to f(\lambda)\)，\(A^{-1}\to\lambda^{-1}\)（\(A\) 可逆），\(A^*\to|A|/\lambda\)，\(A^{\top}\) 与 \(A\) 特征多项式相同，\(A+kE\to\lambda+k\)。证明核心一句话：\(A\xi=\lambda\xi\) 两边作用 \(A\) 的多项式并归纳。</p>
  <p><strong>② 不同特征值的特征向量线性无关（递推证明）</strong>：设 \(\sum k_i\xi_i=0\)，两边用 \(A-\lambda_rE\) 作用，除 \(\xi_r\) 外各项系数变为 \(k_i(\lambda_i-\lambda_r)\)，由归纳假设 \(k_i(\lambda_i-\lambda_r)=0\)，又 \(\lambda_i\ne\lambda_r\)，得 \(k_i=0\)，再回代得 \(k_r=0\)。</p>
  <p><strong>③ \(|A|=0\iff 0\) 是 \(A\) 的特征值</strong>：\(f(0)=|A|\)，一行搞定，连接第 1 篇与第 3 篇的桥梁。</p>
</div></details>
'''

EXT['3-5-正交矩阵和正交变换'] = r'''
<details class="ext"><summary>拓展 · 可能考<span class="ext-tag">考前加分</span></summary><div class="ext-b">
  <p><strong>① 正交矩阵的行/列都是标准正交组</strong>：\(Q^{\top}Q=E\) 按元素读出 \((q_i,q_j)=\delta_{ij}\)——这是构造正交矩阵最直接的方法（把标准正交组按列拼起来）。</p>
  <p><strong>② \(|Q|=\pm1\)</strong>：\(|Q|^2=|Q^{\top}||Q|=|E|=1\)。注意正交矩阵的行列式可正可负（旋转 vs 反射）。</p>
  <p><strong>③ 保内积 ⟹ 保长度 ⟹ 保夹角（小证明链）</strong>：\((Q\alpha,Q\beta)=\alpha^{\top}Q^{\top}Q\beta=(\alpha,\beta)\)；取 \(\beta=\alpha\) 得 \(\|Q\alpha\|=\|\alpha\|\)；再由余弦定义得夹角不变。</p>
  <p><strong>④ 实特征值只有 \(\pm1\)</strong>：\(Q\xi=\lambda\xi\) 两边取范数 \(\|\xi\|=|\lambda|\,\|\xi\|\)，故 \(|\lambda|=1\)，实数时 \(\lambda=\pm1\)。</p>
</div></details>
'''

EXT['3-6-矩阵相似对角化的简单应用'] = r'''
<details class="ext"><summary>拓展 · 可能考<span class="ext-tag">考前加分</span></summary><div class="ext-b">
  <p><strong>① 幂等矩阵（\(A^2=A\)）速算</strong>：\(\lambda^2\xi=A^2\xi=A\xi=\lambda\xi\Rightarrow\lambda\in\{0,1\}\)，且 \(A^n=A\)（不必对角化）。判断/填空常与"幂零 \(A^2=O\Rightarrow A^n=0\)"成对出现。</p>
  <p><strong>② 递推数列 \(x_{k+1}=Ax_k\) 的对角化解法</strong>：\(x_k=A^kx_0=PA^kP^{-1}x_0\)；当所有 \(|\lambda_i|&lt;1\) 时 \(x_k\to0\)，有 \(\lambda=1\) 时趋于其特征向量方向——市场占有率稳态问题就这么解。</p>
  <p><strong>③ 用对角化算行列式</strong>：\(A\sim\Lambda \Rightarrow |A|=|\Lambda|=\prod\lambda_i\)、\(|A+kE|=\prod(\lambda_i+k)\)——比先求 \(A+kE\) 再展开快得多。</p>
</div></details>
'''

EXT['4-1-二次型及其标准形'] = r'''
<details class="ext"><summary>拓展 · 可能考<span class="ext-tag">考前加分</span></summary><div class="ext-b">
  <p><strong>① 二次型的矩阵必须对称且唯一</strong>：给出 \(x^{\top}Bx\) 要先对称化 \(A=\tfrac{B+B^{\top}}2\)；唯一性证明：若 \(x^{\top}Ax=x^{\top}A'x\) 对一切 \(x\) 成立，取 \(x=e_i\) 得对角元相同，取 \(x=e_i+e_j\) 得交叉项相同。</p>
  <p><strong>② 含交叉项 \(x_1x_2\) 的配方法</strong>：没有平方项可配时，先令 \(x_1=y_1+y_2,\ x_2=y_1-y_2\)（可逆线性变换），凑出 \(y_1^2-y_2^2\) 再继续。</p>
  <p><strong>③ 合同的三条性质</strong>：反身、对称、传递；可逆线性变换保持秩与正负惯性指数——这就是"规范形唯一"的全部依据。</p>
</div></details>
'''

EXT['4-2-正定二次型'] = r'''
<details class="ext"><summary>拓展 · 可能考<span class="ext-tag">考前加分</span></summary><div class="ext-b">
  <p><strong>① 正定 ⟹ 主对角元全正（小证明）</strong>：取 \(x=e_i\)，\(a_{ii}=e_i^{\top}Ae_i&gt;0\)。注意只是必要条件：对角元全正不能反推正定（如 \(\begin{pmatrix}1&10\\10&1\end{pmatrix}\) 不正定）。</p>
  <p><strong>② \(A^{\top}A\) 半正定，列满秩时正定</strong>：\(x^{\top}A^{\top}Ax=\|Ax\|^2\ge0\)；\(A\) 列满秩时 \(Ax\ne0\)（\(x\ne0\)），故严格大于零。这是构造半正定/正定矩阵的标准手法。</p>
  <p><strong>③ 正定矩阵的家族保持</strong>：\(A\) 正定 ⟹ \(A^{-1}\)（特征值 \(1/\lambda&gt;0\)）、\(A^*\)（\(|A|/\lambda&gt;0\)）、\(A^m\)（\(\lambda^m&gt;0\)）都正定；但 \(A+B\) 正定需要 \(A,B\) 各自正定（半正定 + 正定也行），半正定 + 半正定不一定正定。</p>
</div></details>
'''

EXT['4-3-二次型的简单应用'] = r'''
<details class="ext"><summary>拓展 · 可能考<span class="ext-tag">考前加分</span></summary><div class="ext-b">
  <p><strong>① 曲面类型速查</strong>：标准形 \(\lambda_1z_1^2+\lambda_2z_2^2+\lambda_3z_3^2=1\)——三正 = 椭球面；两正一负 = 单叶双曲面；一正两负 = 双叶双曲面；有零系数且异号 = 锥面。由惯性指数直接读图，选填题高频。</p>
  <p><strong>② 平面二次曲线的判别式</strong>：\(f(x,y)=ax^2+2bxy+cy^2\)，\(ac-b^2&gt;0\) 为椭圆型、\(=0\) 抛物型、\(&lt;0\) 双曲型（正是 \(A\) 的 2 阶主子式）。</p>
  <p><strong>③ 极值的 Hesse 判据</strong>：驻点处 Hesse 矩阵正定 ⟹ 极小值点，负定 ⟹ 极大值点，不定 ⟹ 鞍点——多元微积分与二次型的接口，考研也常考。</p>
</div></details>
'''

KP = {}
KP['复习题-1'] = r'''<details class="ext"><summary>题型细节考点清单 · 第 1 篇<span class="ext-tag">对照题库</span></summary><div class="ext-b">
  <ul>
  <li><strong>判断题常挖坑</strong>：\(AB=O\) 推不出 \(A=O\) 或 \(B=O\)（零因子）；\(A^2=A\) 推不出 \(A=E\)；初等矩阵经"列变换"意义不同；\(|A|=0\iff\) 列向量组相关。</li>
  <li><strong>选择题高频</strong>：行列式倍加/数乘性质（\(|2A^{\top}|=2^n|A|\)）；可逆充要条件循环链（\(|A|\ne0\)、\(R(A)=n\)、\(Ax=0\) 仅零解、行列向量组无关）；伴随矩阵公式三件套。</li>
  <li><strong>填空高频</strong>：\(|A^*|=|A|^{n-1}\)；初等矩阵幂 \(E(i,j(k))^2=E(i,j(2k))\)；\((A^*)^*=|A|^{n-2}A\)。</li>
  <li><strong>计算大题</strong>：含参方程组全分类讨论（唯一/无穷/无解）；矩阵方程 \(AX=B\)（可逆化或逐列解）；爪形/三对角行列式；\((A\mid E)\) 行变换求逆并验算 \(AA^{-1}=E\)。</li>
  <li><strong>证明大题</strong>：幂零矩阵秩的上下界（凑和/凑积）；\(A^2=O\Rightarrow(E-A)^{-1}=E+A\)；\(R(A^*)\) 三段取值。</li>
  </ul>
</div></details>'''

KP['复习题-2'] = r'''<details class="ext"><summary>题型细节考点清单 · 第 2 篇<span class="ext-tag">对照题库</span></summary><div class="ext-b">
  <ul>
  <li><strong>判断题常挖坑</strong>：\(s&gt;n\) 必相关但 \(s\le n\) 不一定无关；部分相关 ⟹ 整体相关、整体无关 ⟹ 部分无关（逆否同真）；零向量入组必相关。</li>
  <li><strong>选择题高频</strong>：解的结构（非齐次解之差是齐次解；\(k_1\eta_1+k_2\eta_2\) 为解 ⟺ \(k_1+k_2=1\)）；基础解系含 \(n-R(A)\) 个向量且不唯一。</li>
  <li><strong>填空高频</strong>：通解 = 特解 + 齐次通解；由两个特解重构通解（差向量进基础解系）。</li>
  <li><strong>计算大题</strong>：极大无关组（只行变换、最简形拐点列 + 读表示系数）；含参线性表示三分类；由解反求方程组（构造正交补行向量）；最小二乘拟合直线（正规方程 \(2\times2\)）。</li>
  <li><strong>证明大题</strong>：正交组线性无关（内积组合）；基础解系维数定理 \(n-R(A)\)；两个基础解系等价（都线性无关且维数相同即等价）。</li>
  </ul>
</div></details>'''

KP['复习题-3'] = r'''<details class="ext"><summary>题型细节考点清单 · 第 3 篇<span class="ext-tag">对照题库</span></summary><div class="ext-b">
  <ul>
  <li><strong>判断题常挖坑</strong>：相似有传递性；特征值相同 ≠ 相似（秩反例 \(O\) vs \(\begin{pmatrix}0&1\\0&0\end{pmatrix}\)）；正交矩阵行列式 \(\pm1\)；实对称矩阵必可（正交）对角化。</li>
  <li><strong>选择题高频</strong>：可对角化判定（互异 ⟹ 可；重根看 \(R(A-\lambda E)\)）；\(A^*\) 的特征值 \(|A|/\lambda\)；\(f(A)\) 的特征值 \(f(\lambda)\)。</li>
  <li><strong>填空高频</strong>：秩 1 矩阵幂 \(A^m=(\operatorname{tr}A)^{m-1}A\)；\(|f(A)|=\prod f(\lambda_i)\)；正交变换保长度 \(\|Qx\|=\|x\|\)。</li>
  <li><strong>计算大题</strong>：过渡矩阵 \((A\mid B)\) 行变换 + 坐标换算；相似传递求 \(A^n\)；对角化（含零特征值）；求特征值特征向量完整流程。</li>
  <li><strong>证明大题</strong>：Householder 矩阵构造（\(H=E-2uu^{\top}\) 正交对称且 \(Hu\) 为反射）；实对称不同特征值特征向量正交；幂等矩阵特征值只有 0/1；相似的传递性。</li>
  </ul>
</div></details>'''

KP['复习题-4'] = r'''<details class="ext"><summary>题型细节考点清单 · 第 4 篇<span class="ext-tag">对照题库</span></summary><div class="ext-b">
  <ul>
  <li><strong>判断题常挖坑</strong>：对角元全正 / \(|A|&gt;0\) / 迹为正都只是必要条件；\(A\) 正定 ⟹ \(A^{-1}\) 正定，但 \(A\) 半正定时 \(A^{-1}\) 未必存在；\(x^{\top}Ax&gt;0\) 要求对<strong>一切</strong> \(x\ne0\) 成立。</li>
  <li><strong>选择题高频</strong>：正定判定四件套（特征值全正 / 顺序主子式全正 / 正惯性指数 = n / \(A=CC^{\top}\)）；正交变换化标准形的系数即特征值。</li>
  <li><strong>填空高频</strong>：正定性定参数（顺序主子式不等式组联立）；合同不变量（正负惯性指数）。</li>
  <li><strong>计算大题</strong>：正交变换化标准形全流程（特征值 → 重根施密特正交化 → 单位化拼 \(Q\) → 写标准形）；配方法化标准形（可逆变换、验证合同）。</li>
  <li><strong>证明大题</strong>：正定的保持（\(A^{-1},A^*,A^m\) 用特征值迁移）；正定 ⟹ 主对角元全正（取 \(e_i\)）；\(A^{\top}A\) 半正定、列满秩时正定。</li>
  </ul>
</div></details>'''

import os
base = 'assets/content'
n_ok = 0
for name, block in EXT.items():
    p = os.path.join(base, name + '.html')
    t = open(p, encoding='utf-8').read()
    if 'class="ext"' in t:
        print('skip (已存在)', name); continue
    open(p, 'a', encoding='utf-8').write('\n' + block.strip() + '\n')
    n_ok += 1
for name, block in KP.items():
    p = os.path.join(base, name + '.html')
    t = open(p, encoding='utf-8').read()
    if '题型细节考点清单' in t:
        print('skip (已存在)', name); continue
    open(p, 'a', encoding='utf-8').write('\n' + block + '\n')
    n_ok += 1
print('appended:', n_ok)
