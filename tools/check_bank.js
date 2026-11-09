// 临时校验脚本：node tools/check_bank.js
global.window = global;
require('../assets/exam/theory_bank.js');
require('../assets/exam/solve_bank.js');
const katex = require('../assets/katex/katex.min.js');
const macros = { '\\R': '\\mathbb{R}', '\\E': '\\mathbb{E}', '\\bm': '\\boldsymbol' };
let total = 0, bad = 0;
const B = window.XDBANK_OBJ;
// 浏览器等价：innerHTML 会先解码 HTML 实体，再由 KaTeX 处理文本
const decode = s => s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
function check(raw, label, id) {
  const t = decode(raw);
  const disp = /\$\$([\s\S]*?)\$\$/g; let m;
  while ((m = disp.exec(t))) { total++;
    try { katex.renderToString(m[1], { displayMode: true, throwOnError: true, macros }); }
    catch (e) { bad++; console.log('FAIL', id, label, 'disp |', m[1].slice(0, 70), '|', e.message.slice(0, 90)); } }
  const inl = /\\\(([\s\S]*?)\\\)/g;
  while ((m = inl.exec(t))) { total++;
    try { katex.renderToString(m[1], { throwOnError: true, macros }); }
    catch (e) { bad++; console.log('FAIL', id, label, 'inl |', m[1].slice(0, 70), '|', e.message.slice(0, 90)); } }
}
for (const ty of Object.keys(B)) for (const q of B[ty]) {
  check(q.q || '', 'q', q.id);
  check(q.sol || '', 'sol', q.id);
  if (q.opts) q.opts.forEach((o, i) => check(o, 'opt' + i, q.id));
  if (typeof q.ans === 'string' && q.ans.startsWith('\\')) check(q.ans, 'ans', q.id);
}
console.log('bank formulas', total, 'bad', bad);
