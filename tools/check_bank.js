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
  const disp = /\$\$([\s\S]*?)\$\$/g;
  const spans = []; let m;
  while ((m = disp.exec(t))) { spans.push([m[1], true]); }
  // 行分隔符 \\ 只存在于 $$..$$ 内；剔除行间块后再扫行内公式，
  // 避免 "行分隔符 \\ + 内积括号 (" 被误判为行内定界符 \(（p35 误报根源）
  const rest = t.replace(/\$\$[\s\S]*?\$\$/g, '');
  const inl = /\\\(([\s\S]*?)\\\)/g;
  while ((m = inl.exec(rest))) { spans.push([m[1], false]); }
  for (const [seg, isDisp] of spans) { total++;
    try { katex.renderToString(seg, { displayMode: isDisp, throwOnError: true, macros }); }
    catch (e) { bad++; console.log('FAIL', id, label, isDisp ? 'disp' : 'inl', '|', seg.slice(0, 70), '|', e.message.slice(0, 90)); } }
}
for (const ty of Object.keys(B)) for (const q of B[ty]) {
  check(q.q || '', 'q', q.id);
  check(q.sol || '', 'sol', q.id);
  if (q.opts) q.opts.forEach((o, i) => check(o, 'opt' + i, q.id));
  if (typeof q.ans === 'string' && q.ans.startsWith('\\')) check(q.ans, 'ans', q.id);
}
console.log('bank formulas', total, 'bad', bad);
