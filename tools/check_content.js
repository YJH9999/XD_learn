// 内容文件公式校验：模拟浏览器 innerHTML 解码后提取，node tools/check_content.js
const fs = require('fs');
const katex = require('../assets/katex/katex.min.js');
const macros = { '\\R': '\\mathbb{R}', '\\E': '\\mathbb{E}', '\\bm': '\\boldsymbol' };
const decode = s => s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
let total = 0, bad = 0;
for (const f of fs.readdirSync('assets/content')) {
  const t = decode(fs.readFileSync('assets/content/' + f, 'utf8'));
  const disp = /\$\$([\s\S]*?)\$\$/g; let m;
  while ((m = disp.exec(t))) { total++;
    try { katex.renderToString(m[1], { displayMode: true, throwOnError: true, macros }); }
    catch (e) { bad++; console.log('FAIL', f, 'disp |', m[1].slice(0, 70), '|', e.message.slice(0, 90)); } }
  const inl = /\\\(([\s\S]*?)\\\)/g;
  while ((m = inl.exec(t))) { total++;
    try { katex.renderToString(m[1], { throwOnError: true, macros }); }
    catch (e) { bad++; console.log('FAIL', f, 'inl |', m[1].slice(0, 70), '|', e.message.slice(0, 90)); } }
}
console.log('content formulas', total, 'bad', bad);
