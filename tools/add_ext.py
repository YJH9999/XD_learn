# -*- coding: utf-8 -*-
"""向各章节追加第二块「拓展 · 常用技巧」（与已有的「拓展 · 可能考」互补，不重复）。
幂等：文件里已含「拓展 · 常用技巧」则跳过。
技巧取材：毛纲源《线性代数解题方法技巧归纳》、同济《线性代数》、
陈建龙《线性代数》、李尚志《线性代数》、Lay/Leon/Poole 教材常用套路。"""
import os

EXT = {}

EXT['1-1-矩阵概述'] = r'''
<details class="ext"><summary>拓展 · 常用技巧<span class="ext-tag">技巧归纳</span></summary><div class="ext-b">
  <p><strong>① 可交换的两类矩阵</strong>：对角阵与对角阵相乘可交换；数量矩阵 \(kE\) 与任意同阶方阵可交换。\(AB=BA\) 一般不成立——判断题里"由 \(AB=BA\) 推出…"是高频考法。</p>
  <p><strong>② 幂等与对合的特征值速记</strong>：\(A^2=A\)（幂等）的特征值只能是 \(1/0\)；\(A^2=E\)（对合）的特征值只能是 \(\pm1\)。幂零 \(A^k=O\) 的特征值全为 \(0\)。</p>
  <p><strong>③ 乘法可行性口诀</strong>：\(A_{m\times s}B_{s\times n}\) 才能乘，结果 \(m\times n\)（"中间相等取两头"）；\(AB\) 有意义不代表 \(BA\) 有意义。</p>
  <p><strong>④ 转置运算律</strong>：\((AB)^{\top}=B^{\top}A^{\top}\)、\((A+B)^{\top}=A^{\top}+B^{\top}\)、\((kA)^{\top}=kA^{\top}\)——"顺序翻转"是转置证明题的第一步。</p>
</div></details>
'''

EXT['1-2-逆矩阵和行列式'] = r'''
<details class="ext"><summary>拓展 · 常用技巧<span class="ext-tag">技巧归纳</span></summary><div class="ext-b">
  <p><strong>① 二阶伴随速写</strong>：\(A=\begin{pmatrix}a&b\\c&d\end{pmatrix}\Rightarrow A^{*}=\begin{pmatrix}d&-b\\-c&a\end{pmatrix}\)（主对角互换、副对角变号）——二阶题不用按定义算。</p>
  <p><strong>② 伴随家族公式</strong>：\((A^{*})^{*}=|A|^{n-2}A\)（\(n\ge2\)）；\(A^{*}\) 可逆时 \((A^{*})^{-1}=\dfrac{A}{|A|}\)；\((A^{*})^{\top}=(A^{\top})^{*}\)；\((A^{*})^{-1}=(A^{-1})^{*}\)。</p>
  <p><strong>③ 逆的混合运算</strong>：\(A,B,A+B\) 都可逆时 \((A^{-1}+B^{-1})^{-1}=A(A+B)^{-1}B\)，右乘展开即验证。</p>
  <p><strong>④ \(|A+B|\) 没有公式</strong>：\(|A+B|\ne|A|+|B|\)；想拆分必须只拆一行（列）且其余行原样不动——行列式性质题的标准陷阱。</p>
</div></details>
'''

EXT['1-3-行列式的性质与应用'] = r'''
<details class="ext"><summary>拓展 · 常用技巧<span class="ext-tag">技巧归纳</span></summary><div class="ext-b">
  <p><strong>① 加边法（升阶法）</strong>：行和相等、爪形行列式，加一行 \((1,1,\dots,1)\) 与一列 \((1,0,\dots,0)^{\top}\)，行列式值不变但结构可消——毛纲源《技巧归纳》的经典起手式。</p>
  <p><strong>② 逐行相减</strong>：相邻两行 \(r_i-r_{i-1}\) 制造零与公因子，常把 \(n\) 阶行列式化成三对角或范德蒙型再递推。</p>
  <p><strong>③ 行和相等固定起手</strong>：每行元素之和相等时，把各列都加到第一列提出公因子，再用第一行的倍数消其余行。</p>
  <p><strong>④ 拆分原则</strong>：一次只拆一行（列），其余行不动；适合含 \(x\) 行列式的分段讨论，拆完逐段求根。</p>
</div></details>
'''

EXT['1-4-矩阵的初等变换'] = r'''
<details class="ext"><summary>拓展 · 常用技巧<span class="ext-tag">技巧归纳</span></summary><div class="ext-b">
  <p><strong>① 左行右列法则</strong>：\(PA\) = 对 \(A\) 作 \(P\) 对应的<b>行</b>变换；\(AP\) = 对 \(A\) 作 \(P\) 对应的<b>列</b>变换。解方程组与求逆只允许行变换。</p>
  <p><strong>② 解矩阵方程的方向选择</strong>：\(AX=B\) 且 \(A\) 可逆 → \((A\mid B)\xrightarrow{\text{行}}(E\mid X)\)；\(XA=B\) → 转置成 \(A^{\top}X^{\top}=B^{\top}\) 或用列变换。</p>
  <p><strong>③ 初等变换保相关性</strong>：初等列变换不改变列向量组的线性相关性（只换坐标），所以"列拼—行变换—读极大无关组"用的必须是行变换。</p>
  <p><strong>④ 倍加阵的幂</strong>：\(E(i,j(k))^m=E(i,j(mk))\)（倍数累加）；换行阵偶次幂 = \(E\)。求 \(P^{2022}AP\) 先辨认 \(P\) 属于哪一类。</p>
</div></details>
'''

EXT['1-5-矩阵的秩和线性方程组'] = r'''
<details class="ext"><summary>拓展 · 常用技巧<span class="ext-tag">技巧归纳</span></summary><div class="ext-b">
  <p><strong>① Sylvester 不等式</strong>：\(R(AB)\ge R(A)+R(B)-n\)（\(n\) 为 \(A\) 的列数）；与 \(AB=O\Rightarrow R(A)+R(B)\le n\) 互为上下界，证明题打包出现。</p>
  <p><strong>② 实矩阵关键等式</strong>：\(R(A^{\top}A)=R(A)\)，由此 \(A^{\top}Ax=A^{\top}b\) 恒有解（最小二乘的存在性）。</p>
  <p><strong>③ 行最简形直接读解</strong>：自由未知量个数 \(=n-R(A)\)，主元未知量按行最简形抄成表达式即可，不必回代。</p>
  <p><strong>④ 等价标准形是底牌</strong>：\(R(A)=r\iff\) 存在可逆 \(P,Q\) 使 \(PAQ=\begin{pmatrix}E_r&O\\O&O\end{pmatrix}\)——所有抽象秩证明的最后一张牌。</p>
</div></details>
'''

EXT['1-6-分块矩阵'] = r'''
<details class="ext"><summary>拓展 · 常用技巧<span class="ext-tag">技巧归纳</span></summary><div class="ext-b">
  <p><strong>① 三角分块求逆</strong>：\(\begin{pmatrix}A&O\\C&B\end{pmatrix}^{-1}=\begin{pmatrix}A^{-1}&O\\-B^{-1}CA^{-1}&B^{-1}\end{pmatrix}\)——"主对角取逆，副对角添负号再左乘邻居的逆"。</p>
  <p><strong>② 副对角型互换取逆</strong>：\(\begin{pmatrix}O&A\\B&O\end{pmatrix}^{-1}=\begin{pmatrix}O&B^{-1}\\A^{-1}&O\end{pmatrix}\)。</p>
  <p><strong>③ 分块初等变换</strong>：\(\begin{pmatrix}P&O\\O&E\end{pmatrix}M\) 只对 \(M\) 的上块作行变换——分块消元的本质，"左乘 = 行变换"的块版本。</p>
  <p><strong>④ 分块伴随</strong>：\(\mathrm{diag}(A,B)^{*}=\mathrm{diag}(B^{*},A^{*})\)（注意两块<b>换位</b>，由 \(A^{*}A=|A|E\) 验证），填空易错点。</p>
</div></details>
'''

EXT['1-7-矩阵应用举例'] = r'''
<details class="ext"><summary>拓展 · 常用技巧<span class="ext-tag">技巧归纳</span></summary><div class="ext-b">
  <p><strong>① 建模三板斧</strong>：交通流—每个节点"流入 = 流出"列方程；混合浓度—总量守恒；投入产出—\(x=Cx+d\)。</p>
  <p><strong>② 编码与解码</strong>：可逆矩阵 \(A\) 编码 \(C=AM\)、解码 \(M=A^{-1}C\)——可逆性的直接应用，注意分块后逐列处理。</p>
  <p><strong>③ 克拉默还是消元</strong>：未知量少且系数行列式好算用克拉默；规模大或含参讨论一律高斯消元。</p>
  <p><strong>④ 应用题验算习惯</strong>：解出后回代原方程，尤其含参题要检查分母非零、参数取值是否漏分类。</p>
</div></details>
'''

EXT['2-1-向量及其线性相关性'] = r'''
<details class="ext"><summary>拓展 · 常用技巧<span class="ext-tag">技巧归纳</span></summary><div class="ext-b">
  <p><strong>① 添向量判秩</strong>：\(R(\alpha_1,\dots,\alpha_s,\beta)=s\iff\beta\) 可由组内线性表示；\(=s+1\iff\) 不能表示（此时原组无关且加入 \(\beta\) 仍无关）。</p>
  <p><strong>② 等价的秩判据</strong>：向量组 I 与 II 等价 \(\iff R(\mathrm{I})=R(\mathrm{II})=R(\mathrm{I},\mathrm{II})\)；等价必同秩，同秩不一定等价（\(x\) 轴与 \(y\) 轴）。</p>
  <p><strong>③ 反证法模板</strong>：假设相关 → 某向量 = 其余向量的线性组合 → 代入题目条件导出矛盾——抽象无关证明题九成走这条路。</p>
  <p><strong>④ 整组相关 ⟺ 极大无关组不满员</strong>：\(s\) 个向量相关 ⟺ 其极大无关组含向量数 \(&lt;s\) ⟺ \(R&lt;s\)。</p>
</div></details>
'''

EXT['2-2-向量空间'] = r'''
<details class="ext"><summary>拓展 · 常用技巧<span class="ext-tag">技巧归纳</span></summary><div class="ext-b">
  <p><strong>① 施密特正交化公式</strong>：\(\beta_k=\alpha_k-\sum_{i&lt;k}\dfrac{(\alpha_k,\beta_i)}{(\beta_i,\beta_i)}\beta_i\)，先正交再逐个单位化。</p>
  <p><strong>② 标准正交基的标志</strong>：列向量组构成标准正交基 \(\iff Q^{\top}Q=E\iff Q\) 是正交矩阵。</p>
  <p><strong>③ 解空间就是齐次解集</strong>：\(Ax=0\) 的解集是 \(n-R(A)\) 维子空间，基础解系就是它的一组基；非齐次解集不含零向量、不是子空间。</p>
  <p><strong>④ 过渡矩阵与正交性</strong>：两组基都标准正交时，过渡矩阵必为正交矩阵（\(C^{-1}=C^{\top}\)），求逆零成本。</p>
</div></details>
'''

EXT['2-3-线性方程组解的结构'] = r'''
<details class="ext"><summary>拓展 · 常用技巧<span class="ext-tag">技巧归纳</span></summary><div class="ext-b">
  <p><strong>① 由解反求方程组</strong>：把 \(s\) 个无关解的分量逐行写成"系数关系"，取其正交补向量拼成 \(A\) 的行，行数 \(\ge n-R\)，再用行变换化简验证。</p>
  <p><strong>② 同解判定</strong>：\(Ax=0\) 与 \(Bx=0\) 同解 \(\iff R(A)=R(B)=R(A;B)\)（行向量组等价）；同解则 \(A^{\top}A\) 与 \(B^{\top}B\) 相关结论一并迁移。</p>
  <p><strong>③ 解的存在性几何版</strong>：\(Ax=b\) 有解 \(\iff b\in R(A)\)（列空间）；残差 \(b-Ax\) 垂直于列空间时解即最小二乘解。</p>
  <p><strong>④ 通解写完必验算</strong>：特解代回 + 基础解系逐个代回 \(Ax=0\)，含参题还要核对各情形的维数是否连续变化。</p>
</div></details>
'''

EXT['2-4-简单最小二乘问题'] = r'''
<details class="ext"><summary>拓展 · 常用技巧<span class="ext-tag">技巧归纳</span></summary><div class="ext-b">
  <p><strong>① 存在性与唯一性</strong>：正规方程 \(A^{\top}Ax=A^{\top}b\) 恒有解；解唯一 \(\iff R(A)=\) 列数（\(A\) 列无关）。</p>
  <p><strong>② \(A^{\top}A\) 可逆判据</strong>：\(A\) 列无关 \(\iff A^{\top}A\) 可逆（实矩阵 \(R(A^{\top}A)=R(A)\)），此时唯一解 \(x=(A^{\top}A)^{-1}A^{\top}b\)。</p>
  <p><strong>③ 多解时的通解</strong>：\(A\) 列相关时最小二乘解不唯一，通解 = 任一特解 + \(\ker A\)；数据拟合题选范数最小的一个。</p>
  <p><strong>④ 三点共线的行列式判据</strong>：平面上三点 \((x_i,y_i)\) 共线 \(\iff\begin{vmatrix}1&x_1&y_1\\1&x_2&y_2\\1&x_3&y_3\end{vmatrix}=0\)——"拟合直线是否存在"的快速判断。</p>
</div></details>
'''

EXT['3-1-基变换和坐标变换'] = r'''
<details class="ext"><summary>拓展 · 常用技巧<span class="ext-tag">技巧归纳</span></summary><div class="ext-b">
  <p><strong>① 标准正交基间过渡矩阵 = 转置</strong>：两组基都标准正交时 \(C^{-1}=C^{\top}\)，先验证正交再"求逆免算"。</p>
  <p><strong>② 抽查验证</strong>：任取一列检查 \(\beta_j=\sum_i c_{ij}\alpha_i\)，过渡矩阵题九成错误能靠这一步抓住。</p>
  <p><strong>③ 坐标唯一性</strong>：同一组基下坐标唯一；不同基下坐标不同，但由可逆矩阵唯一联系。</p>
  <p><strong>④ 几何视角</strong>：正交过渡矩阵对应坐标系旋转（\(|C|=1\)）或旋转 + 反射（\(|C|=-1\)），向量本身不变、只是坐标换了说法。</p>
</div></details>
'''

EXT['3-2-线性变换'] = r'''
<details class="ext"><summary>拓展 · 常用技巧<span class="ext-tag">技巧归纳</span></summary><div class="ext-b">
  <p><strong>① 表示矩阵按列放</strong>：\(\mathscr{A}\) 在基 \(\varepsilon_i\) 下的矩阵，是把 \(\mathscr{A}\varepsilon_j\) 的坐标写成第 \(j\) 列——"像的坐标写列"，不要按行放。</p>
  <p><strong>② 复合顺序别反</strong>：\((\mathscr{A}\mathscr{B})(x)=\mathscr{A}(\mathscr{B}x)\) 对应矩阵 \(AB\)，先作用的写在右边。</p>
  <p><strong>③ 可逆的三等价</strong>：线性变换可逆 ⟺ 表示矩阵可逆 ⟺ 核只有零向量 ⟺ 把基映成基。</p>
  <p><strong>④ 不变子空间</strong>：若 \(W\) 对 \(\mathscr{A}\) 封闭，则取 \(W\) 的基拼进大基后表示矩阵呈块三角——这是分块对角化的来源。</p>
</div></details>
'''

EXT['3-3-相似矩阵'] = r'''
<details class="ext"><summary>拓展 · 常用技巧<span class="ext-tag">技巧归纳</span></summary><div class="ext-b">
  <p><strong>① 相似必要条件清单</strong>：迹、行列式、秩、特征多项式、各特征值全部相同。任何一条不满足即"不相似"（一票否决）；全满足也不保证相似。</p>
  <p><strong>② 判相似实操顺序</strong>：先比迹与行列式 → 再逐特征值比几何重数 → 最后找可逆 \(P\) 或公共对角化对象。</p>
  <p><strong>③ 相似的传染性</strong>：\(A\sim B\Rightarrow A^{k}\sim B^{k},\ A^{\top}\sim B^{\top},\ A^{-1}\sim B^{-1}\)（可逆时）、\(f(A)\sim f(B)\)、\(A+kE\sim B+kE\)。</p>
  <p><strong>④ 相似 / 等价 / 合同辨析</strong>：等价 = 同秩（\(PAQ\)，\(P,Q\) 各自可逆）；相似 = 同变换（\(P^{-1}AP\)）；合同 = 同惯性（\(C^{\top}AC\)，\(C\) 可逆）。正交相似三者兼顾。</p>
</div></details>
'''

EXT['3-4-矩阵的特征值和特征向量'] = r'''
<details class="ext"><summary>拓展 · 常用技巧<span class="ext-tag">技巧归纳</span></summary><div class="ext-b">
  <p><strong>① 速算三件套</strong>：各行元素之和为 \(s\) ⟹ \(s\) 是特征值；\(\operatorname{tr}A=\sum\lambda_i\)；\(|A|=\prod\lambda_i\)。已知 \(n-1\) 个特征值与 \(|A|\)，最后一个 = \(|A|/\prod\)。</p>
  <p><strong>② 特征多项式系数公式</strong>：\(f(\lambda)=\lambda^n-\operatorname{tr}(A)\lambda^{n-1}+\cdots+(-1)^n|A|\)——由迹与行列式直接写特征多项式。</p>
  <p><strong>③ 几何重数 ≤ 代数重数</strong>：\((\lambda E-A)x=0\) 解空间维数 ≤ 重数，相等才可对角化；单特征值必有一个无关特征向量。</p>
  <p><strong>④ 特征向量方向不变</strong>：\(A\xi=\lambda\xi\) ⟹ \(A^{k}\xi=\lambda^{k}\xi\)、\(f(A)\xi=f(\lambda)\xi\)——抽象题里"同一个 \(\xi\) 用到底"。</p>
</div></details>
'''

EXT['3-5-正交矩阵和正交变换'] = r'''
<details class="ext"><summary>拓展 · 常用技巧<span class="ext-tag">技巧归纳</span></summary><div class="ext-b">
  <p><strong>① 施密特流程固定</strong>：先正交化（逐个减投影）再单位化，顺序不能反；同一特征值的多个向量也要互相正交化。</p>
  <p><strong>② 构造正交矩阵收尾</strong>：把 \(n\) 个正交单位向量按列排成 \(Q\)，自动满足 \(Q^{\top}Q=E\)——正交对角化题的最后一步。</p>
  <p><strong>③ 求逆 = 转置</strong>：\(Q^{-1}=Q^{\top}\)；\(|Q|=\pm1\)，\(-1\) 对应含反射。</p>
  <p><strong>④ 反射矩阵（Householder）</strong>：\(H=E-2uu^{\top}\)（\(\|u\|=1\)）正交、对称、\(Hu\) 是关于与 \(u\) 垂直的超平面的反射——构造正交阵的万能公式。</p>
</div></details>
'''

EXT['3-6-矩阵相似对角化的简单应用'] = r'''
<details class="ext"><summary>拓展 · 常用技巧<span class="ext-tag">技巧归纳</span></summary><div class="ext-b">
  <p><strong>① 求 \(A^{k}\) 流程</strong>：先证可对角化 → 求 \(P,\Lambda\) → \(A^{k}=P\Lambda^{k}P^{-1}\)；对角阵的幂逐元素取幂，最后乘回 \(P\)，别忘了 \(P^{-1}\)。</p>
  <p><strong>② 斐波那契建模</strong>：\(\binom{F_{k+1}}{F_k}=\begin{pmatrix}1&1\\1&0\end{pmatrix}\binom{F_k}{F_{k-1}}\)，通项 = 特征值 \(\\dfrac{1\pm\sqrt5}{2}\) 的组合。</p>
  <p><strong>③ 马尔可夫稳态</strong>：列和为 \(1\) 的转移矩阵有特征值 \(1\)，长期状态 = \(\lambda=1\) 的单位特征向量——人口迁移、市场份额应用题。</p>
  <p><strong>④ \(0\) 特征值与可逆性</strong>：\(A\) 可逆 ⟺ 无 \(0\) 特征值；\(A\) 不可逆时 \(Ax=0\) 的非零解就是 \(0\) 的特征向量，常用来反求参数。</p>
</div></details>
'''

EXT['4-1-二次型及其标准形'] = r'''
<details class="ext"><summary>拓展 · 常用技巧<span class="ext-tag">技巧归纳</span></summary><div class="ext-b">
  <p><strong>① 配方法完整步骤</strong>：有平方项就把该变量的所有项配成完全平方后换元；无平方项先作 \(x_i=y_i+y_j,\ x_j=y_i-y_j\) 造平方项；最后写出可逆变换 \(x=Cy\) 并验证 \(C^{\top}AC\)。</p>
  <p><strong>② 正交变换法五步</strong>：写 \(A\) → 求特征值 → 求特征向量 → 同特征值向量施密特正交化后全体单位化 → 按列排 \(Q\)，标准形系数 = 特征值顺序。</p>
  <p><strong>③ 标准形不唯一、规范形唯一</strong>：可逆变换可改变标准形系数，但 \(p,q\) 不动（惯性定理）。</p>
  <p><strong>④ 惯性指数的可靠来源</strong>：\(p\) = 正特征值个数（正交变换后数正号），或由各阶顺序主子式符号与 \(|A|\) 符号联合判定——别试图用迹单独猜 \(p\)。</p>
</div></details>
'''

EXT['4-2-正定二次型'] = r'''
<details class="ext"><summary>拓展 · 常用技巧<span class="ext-tag">技巧归纳</span></summary><div class="ext-b">
  <p><strong>① 正定充要条件全家桶</strong>（任一即可）：顺序主子式全正；特征值全正；正惯性指数 \(=n\)；与 \(E\) 合同；存在可逆 \(C\) 使 \(A=C^{\top}C\)。</p>
  <p><strong>② 顺序主子式必须左上角逐阶</strong>：\(\Delta_1,\Delta_2,\dots,\Delta_n\) 依次取左上角 \(k\) 阶子式——位置取错是计算题最常见失误。</p>
  <p><strong>③ 含参正定套路</strong>：联立 \(\Delta_1&gt;0,\Delta_2&gt;0,\Delta_3&gt;0\) 解公共区间，千万别只验 \(|A|&gt;0\)。</p>
  <p><strong>④ 必要条件当快筛</strong>：正定 ⟹ \(a_{ii}&gt;0\)、\(\operatorname{tr}A&gt;0\)、\(|A|&gt;0\)；对角元有非正的直接判"不正定"，省一轮完整计算。</p>
</div></details>
'''

EXT['4-3-二次型的简单应用'] = r'''
<details class="ext"><summary>拓展 · 常用技巧<span class="ext-tag">技巧归纳</span></summary><div class="ext-b">
  <p><strong>① 单位球上的最值</strong>：\(f(x)=x^{\top}Ax\) 在 \(\|x\|=1\) 上的最大 / 最小值 = 最大 / 最小特征值，取到点是对应单位特征向量（瑞利商极值）。</p>
  <p><strong>② 主轴定理一句话</strong>：实二次型总能经正交变换（旋转）化成纯平方和——交叉项消失，主轴方向 = 特征向量方向。</p>
  <p><strong>③ 等值面形状</strong>：\(f(x)=c\) 的等值面由 \(p,q\) 决定：全正为椭球面，异号为双曲面——正定性在图形上就是"等值面是否闭合"。</p>
  <p><strong>④ 拉格朗日乘数接口</strong>：约束 \(\|x\|^2=1\) 下求 \(f\) 极值，乘子恰好是 \(A\) 的特征值——多元微积分与二次型的同源问题。</p>
</div></details>
'''

base = r'D:\Web\XD_learn\assets\content'
ok, skip = 0, []
for name, block in EXT.items():
    p = os.path.join(base, name + '.html')
    if not os.path.exists(p):
        skip.append(name + ' 缺文件'); continue
    t = open(p, encoding='utf-8').read()
    if '拓展 · 常用技巧' in t:
        skip.append(name + ' 已有'); continue
    if not t.endswith('\n'):
        t += '\n'
    open(p, 'a', encoding='utf-8', newline='\n').write(block.strip() + '\n')
    ok += 1
print('appended:', ok, '· skipped:', skip if skip else 'none')
