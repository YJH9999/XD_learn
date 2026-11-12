/* XD 分章题型统计（读 window.XDBANK_OBJ） */
'use strict';
const fs = require('fs');
global.window = {};
eval(fs.readFileSync('assets/exam/theory_bank.js', 'utf8'));
eval(fs.readFileSync('assets/exam/solve_bank.js', 'utf8'));
const O = global.window.XDBANK_OBJ || {};
const all = [...(O.judge || []), ...(O.choice || []), ...(O.blank || []), ...(O.solve || []), ...(O.proof || [])];
const c = {};
for (const q of all) {
  const k = q.ch + '|' + q.ty;
  c[k] = (c[k] || 0) + 1;
}
const chs = [...new Set(all.map(q => q.ch))].sort((a, b) => a - b);
for (const ch of chs) {
  const row = {};
  for (const t of ['judge', 'choice', 'blank', 'solve', 'proof']) row[t] = c[ch + '|' + t] || 0;
  const ok = row.judge >= 30 && row.choice >= 60 && row.blank >= 60 && row.proof >= 20;
  console.log('ch' + ch, JSON.stringify(row), ok ? 'OK' : '*** 缺口 ***');
}
console.log('total', all.length);
