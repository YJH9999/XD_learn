/* 可疑字符全量扫描：题库 + 复习数据 + 内容页
   检查：控制符、DEL、孤立代理对、U+FFFD 替换符、零宽字符、HTML 实体合法性 */
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname, '..');

let issues = 0;
function scan(name, s){
  if (typeof s !== 'string') return;
  const found = [];
  for (let i = 0; i < s.length; i++){
    const c = s.codePointAt(i);
    if (c < 0x20 && c !== 9 && c !== 10 && c !== 13)
      found.push('ctrl U+' + c.toString(16).toUpperCase().padStart(4,'0') + ' @' + i);
    if (c >= 0xD800 && c <= 0xDBFF){
      const n = s.codePointAt(i+1);
      if (!(n >= 0xDC00 && n <= 0xDFFF))
        found.push('孤立高代理 U+' + c.toString(16).toUpperCase() + ' @' + i);
    } else if (c >= 0xDC00 && c <= 0xDFFF){
      const p = s.codePointAt(i-1);
      if (!(p >= 0xD800 && p <= 0xDBFF))
        found.push('孤立低代理 U+' + c.toString(16).toUpperCase() + ' @' + i);
    }
    if (c === 0xFFFD) found.push('替换符 U+FFFD @' + i);
    if ((c >= 0x200B && c <= 0x200D) || c === 0xFEFF || c === 0x2060)
      found.push('零宽字符 U+' + c.toString(16).toUpperCase() + ' @' + i);
    if (c === 0x7F) found.push('DEL @' + i);
  }
  // 非法 HTML 实体（& 开头但不是已知实体且无分号结尾的模式太多，只查常见坏实体）
  const badEnt = s.match(/&(?!(?:amp|lt|gt|quot|apos|nbsp|#\d+|#x[0-9a-fA-F]+);)[a-zA-Z]{2,8};/g);
  if (badEnt) found.push('可疑实体 ' + badEnt.slice(0,3).join(' '));
  if (found.length){
    issues++;
    console.log('✗', name, '→', found.slice(0,6).join(' | '), found.length > 6 ? `...共${found.length}` : '');
  }
}

/* 1) 题库 */
const window_ = {};
global.window = window_;
eval(fs.readFileSync(path.join(ROOT, 'assets/exam/theory_bank.js'), 'utf8'));
eval(fs.readFileSync(path.join(ROOT, 'assets/exam/solve_bank.js'), 'utf8'));
const B = window_.XDBANK_OBJ;
let nQ = 0;
for (const ty of Object.keys(B)) for (const q of B[ty]){
  nQ++;
  scan(`${q.id}(${ty}).q`,   q.q);
  scan(`${q.id}(${ty}).sol`, q.sol);
  if (typeof q.ans === 'string') scan(`${q.id}.ans`, q.ans);
  if (Array.isArray(q.opts)) q.opts.forEach((o,i)=>scan(`${q.id}.opt${i}`, o));
  scan(`${q.id}.kp`, q.kp);
  scan(`${q.id}.src`, q.src);
}

/* 2) 复习数据 */
const rvSrc = fs.readFileSync(path.join(ROOT, 'assets/exam/review_data.js'), 'utf8');
const w2 = {};
global.window = w2;
eval(rvSrc);
const RV = w2.XD_REVIEW || [];
let nP = 0;
for (const ch of RV) for (const p of (ch.points||[])){
  nP++;
  scan(`复习[${ch.ch}] ${p.t}`.slice(0, 30), p.t);
  scan(`复习[${ch.ch}] ${p.t}`.slice(0, 30) + '.d', p.d);
}

/* 3) 内容页 */
const cdir = path.join(ROOT, 'assets/content');
let nC = 0;
for (const f of fs.readdirSync(cdir).sort()){
  if (!f.endsWith('.html')) continue;
  nC++;
  scan('内容 ' + f, fs.readFileSync(path.join(cdir, f), 'utf8'));
}

console.log(`\n=== 扫描完成：题库 ${nQ} 题 · 复习 ${nP} 个考点 · 内容页 ${nC} 个`);
console.log(issues === 0 ? '✅ 未发现任何可疑字符（控制符/替换符/零宽/孤立代理/坏实体均为 0）'
  : `⚠️ 共 ${issues} 个条目存在问题，见上`);
