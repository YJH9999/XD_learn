// 临时校验：HTML 标签配对 + 数学模式未转义 <字母
const fs = require('fs');
var window = {}; var XDBANK_OBJ;
eval(fs.readFileSync('D:/Web/XD_learn/assets/exam/theory_bank.js','utf8'));
const B = window.XDBANK_OBJ;
eval(fs.readFileSync('D:/Web/XD_learn/assets/exam/solve_bank.js','utf8'));
const all = [...B.judge,...B.choice,...B.blank,...window.XDBANK_OBJ.solve,...window.XDBANK_OBJ.proof];
console.log('counts: judge',B.judge.length,'choice',B.choice.length,'blank',B.blank.length,'solve',window.XDBANK_OBJ.solve.length,'proof',window.XDBANK_OBJ.proof.length,'TOTAL',all.length);

const fields = all.filter(q=>!q.id||!q.ty||!q.q||!q.sol||(q.ty==='choice'&&(!q.opts||q.opts.length<2))||(q.ty==='judge'&&!q.ans)||(q.ty==='blank'&&!q.ans));
console.log('missing fields:', fields.length?fields.map(q=>q.id):'none');

const ids = all.map(q=>q.id);
const dup = ids.filter((v,i)=>ids.indexOf(v)!==i);
console.log('duplicates:', dup.length?dup:'none');

const badHtml = all.filter(q=>{
  const m=(q.sol||'').match(/<(p|div)[ >]/g)||[]; const c=(q.sol||'').match(/<\/(p|div)>/g)||[];
  return m.length!==c.length;
});
console.log('html tag mismatch:', badHtml.length?badHtml.map(q=>q.id):'none');

// 数学定界符 \(\ \) $$ $$ 内出现 <字母（innerHTML 会当标签吃掉）
function mathSpans(s){
  const out=[]; const re=/\\\((.*?)\\\)|\$\$(.*?)\$\$/g; let m;
  while((m=re.exec(s))) out.push(m[1]||m[2]);
  return out;
}
const badLt = [];
for(const q of all){
  for(const field of [q.q, q.sol, ...(q.opts||[]), q.ans||'']){
    const t = field||'';
    if(mathSpans(t).some(seg=>/<[a-zA-Z]/.test(seg))) { badLt.push(q.id); break; }
  }
}
console.log('unescaped <letter in math:', badLt.length?badLt:'none');
