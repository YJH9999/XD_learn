// 把现有题库 JS 导出为 JSON，供 merge_bank.py 使用
const fs = require('fs');
var window = {};
eval(fs.readFileSync('D:/Web/XD_learn/assets/exam/theory_bank.js', 'utf8'));
eval(fs.readFileSync('D:/Web/XD_learn/assets/exam/solve_bank.js', 'utf8'));
fs.writeFileSync('D:/Web/XD_learn/tools/bank_current.json',
  JSON.stringify(window.XDBANK_OBJ, null, 1), 'utf8');
console.log('dumped:',
  ['judge','choice','blank','solve','proof'].map(t=>t+':'+window.XDBANK_OBJ[t].length).join(' '));
