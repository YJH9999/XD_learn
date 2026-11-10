/* ============================================================
   XD_learn 备考中心 · 组卷模拟
   题型: judge 判断(2′) choice 选择(4′) blank 填空(4′)
         solve 计算(12′) proof 证明(6′)
   组卷: 题型数量 stepper（默认值=江南大学期末卷结构）
         + 章节筛选 + 来源筛选；随机抽题、乱序
   客观题自动判分；计算/证明题不设空——查看参考答案后自评
   ============================================================ */
(function(){
'use strict';

const TY = {
  judge:{name:'判断题', score:2,客观:true},
  choice:{name:'选择题', score:4,客观:true},
  blank:{name:'填空题', score:4,客观:true},
  solve:{name:'计算题', score:12,客观:false},
  proof:{name:'证明题', score:6,客观:false}
};
const PRESETS = {
  std:  {judge:10, choice:0, blank:5, solve:4, proof:2},
  choice:{judge:0, choice:5, blank:5, solve:4, proof:2},
  calc: {judge:0, choice:0, blank:0, solve:8, proof:2},
  mini: {judge:5, choice:0, blank:3, solve:2, proof:1}
};

/* ---------- 题库合并 ---------- */
const BANK = {};
for (const ty of Object.keys(TY)) BANK[ty] = (window.XDBANK_OBJ && window.XDBANK_OBJ[ty]) || [];
const BANK_COUNT = Object.values(BANK).reduce((s,a)=>s+a.length,0);

/* ---------- 状态 ---------- */
const $ = s => document.querySelector(s);
const $$ = s => Array.from(document.querySelectorAll(s));
const LS = {
  get(k,d){ try{ return JSON.parse(localStorage.getItem('xd_'+k)) ?? d; }catch(e){ return d; } },
  set(k,v){ localStorage.setItem('xd_'+k, JSON.stringify(v)); }
};
let paper = [];        // 当前试卷
let idx = 0;           // 当前题号
let answers = {};      // {id:{ans, ok, self}}
let wrongBook = LS.get('wrong', []);   // [题对象快照]
let filterCh = '', filterSrc = '';
let counts = {...PRESETS.std};

/* ---------- 视图切换（支持 #review / #quiz 直达） ---------- */
function showView(name){
  $$('.tabs .tab').forEach(x=>x.classList.toggle('on', x.dataset.view===name));
  $$('.view').forEach(v=>v.classList.toggle('on', v.id==='view-'+name));
}
$$('.tabs .tab').forEach(b=>b.onclick=()=>{
  showView(b.dataset.view);
  history.replaceState(null,'','#'+b.dataset.view);
});
(function(){
  const h=(location.hash||'').replace('#','');
  if(h==='quiz'||h==='review') showView(h);
})();

/* ---------- 主题 ---------- */
function setTheme(dark){
  document.body.classList.toggle('dark', dark);
  LS.set('dark', dark);
}
$('#m-light').onclick = ()=>setTheme(false);
$('#m-dark').onclick  = ()=>setTheme(true);
if (LS.get('dark', matchMedia('(prefers-color-scheme:dark)').matches)) setTheme(true);

/* ---------- 公式渲染 ---------- */
function renderMath(el){
  if (window.renderMathInElement) renderMathInElement(el, {
    delimiters:[
      {left:'$$', right:'$$', display:true},
      {left:'\\(', right:'\\)', display:false}
    ],
    throwOnError:false
  });
}

/* ---------- 考点速览 ---------- */
(function renderReview(){
  const data = window.XD_REVIEW || [];
  const host = $('#review-list');
  if (!data.length){ host.innerHTML = '<div class="panel">复习数据未加载</div>'; return; }
  host.innerHTML = data.map(ch=>`
    <div class="panel rv-ch">
      <h2>${ch.ch}</h2>
      ${ch.points.map(p=>`
        <details class="rv-card"><summary>${p.t}</summary>
          <div class="rv-b">${p.d}</div></details>`).join('')}
    </div>`).join('');
  renderMath(host);
})();

/* ---------- 组卷面板 ---------- */
function availCount(ty){
  return BANK[ty].filter(q=>
    (!filterCh || q.ch==+filterCh) &&
    (!filterSrc || (q.src||'').includes(filterSrc))
  ).length;
}
function refreshSetup(){
  $$('#type-row .type-cell').forEach(cell=>{
    const ty = cell.dataset.ty;
    cell.querySelector('.stepper b').textContent = counts[ty];
    const n = availCount(ty);
    const warn = counts[ty] > n;
    cell.classList.toggle('lack', warn);
    const av = cell.querySelector('.t-avail');
    if (av) av.textContent = n;
    cell.title = warn ? `题库中该范围内仅 ${n} 题，组卷时将按实际数量抽取` : `可用 ${n} 题`;
  });
  let total = 0;
  for (const ty of Object.keys(counts)) total += counts[ty]*TY[ty].score;
  const nQ = Object.values(counts).reduce((a,b)=>a+b,0);
  $('#paper-total').textContent = `本次组卷：${nQ} 题 · 共 ${total} 分`;
}
$$('#type-row .stepper button').forEach(b=>b.onclick=()=>{
  const cell = b.closest('.type-cell');
  const ty = cell.dataset.ty;
  counts[ty] = Math.max(0, Math.min(20, counts[ty] + +b.dataset.d));
  refreshSetup();
});
$$('#ch-row .chip').forEach(b=>b.onclick=()=>{
  $$('#ch-row .chip').forEach(x=>x.classList.remove('on'));
  b.classList.add('on'); filterCh = b.dataset.ch; refreshSetup();
});
$$('#src-row .chip').forEach(b=>b.onclick=()=>{
  $$('#src-row .chip').forEach(x=>x.classList.remove('on'));
  b.classList.add('on'); filterSrc = b.dataset.src; refreshSetup();
});
$$('.preset-row .chip').forEach(b=>b.onclick=()=>{
  counts = {...PRESETS[b.dataset.preset]};
  refreshSetup();
});
refreshSetup();

/* ---------- 抽题组卷 ---------- */
function shuffle(a){ for(let i=a.length-1;i>0;i--){ const j=Math.random()*(i+1)|0; [a[i],a[j]]=[a[j],a[i]]; } return a; }
function draw(ty, n){
  const pool = shuffle(BANK[ty].filter(q=>
    (!filterCh || q.ch==+filterCh) &&
    (!filterSrc || (q.src||'').includes(filterSrc))
  ).map(q=>q));
  return pool.slice(0, n);
}
function buildPaper(){
  paper = [];
  // 按试卷顺序：判断/选择 → 填空 → 计算 → 证明
  for (const ty of ['judge','choice','blank','solve','proof']){
    if (counts[ty]>0) paper.push(...draw(ty, counts[ty]));
  }
  answers = {}; idx = 0;
}

/* ---------- 作答视图（整卷展示） ---------- */
function showRun(){
  $('#quiz-setup').hidden = true;
  $('#quiz-result').hidden = true;
  $('#quiz-run').hidden = false;
  renderAll();
}
function norm(s){
  return (s||'').replace(/\s|\\,|\\;|\\quad|\\qquad/g,'')
    .replace(/\\\\/g,'\\').toLowerCase();
}
function qBody(q, i){
  let body = `<div class="res-h"><b>${i+1}</b> <span class="tychip t-${q.ty}">${TY[q.ty].name}</span>
    <span class="src">${q.src} · ${q.kp} · ${TY[q.ty].score}分</span>
    <span class="v" id="mark-${q.id}"></span></div>
    <div class="q-stem">${q.q}</div>`;
  if (q.ty==='judge'){
    body += `<div class="ans-row">
      <button class="ans-btn" data-v="√">√ 正确</button>
      <button class="ans-btn" data-v="×">× 错误</button></div>`;
  } else if (q.ty==='choice'){
    body += `<div class="ans-row col">` + q.opts.map((o,i)=>
      `<button class="ans-btn" data-v="${i}"><b>${'ABCD'[i]}</b> ${o}</button>`).join('') + `</div>`;
  } else if (q.ty==='blank'){
    body += `<div class="ans-row"><input class="blank-in" id="blank-in-${q.id}" placeholder="输入答案（式子可用 LaTeX，如 \\frac12）" autocomplete="off">
      <button class="btn small" id="blank-ok-${q.id}">提交</button></div>`;
  } else {
    body += `<div class="self-note">写出完整过程后，对照参考答案自评。</div>
      <div class="btnrow"><button class="btn small" id="btn-show-sol-${q.id}">查看参考答案</button></div>
      <div id="sol-wrap-${q.id}" hidden><div class="sol-box">${q.sol}</div>
        <div class="ans-row"><button class="ans-btn self" data-v="ok" data-q="${q.id}">自评：已掌握</button>
        <button class="ans-btn self bad" data-v="no" data-q="${q.id}">自评：还需巩固</button></div></div>`;
  }
  return body;
}
function renderAll(){
  const total = paper.reduce((s,q)=>s+TY[q.ty].score,0);
  $('#run-type').textContent = `模拟试卷 · 共 ${paper.length} 题 · ${total} 分`;
  $('#bar-fill').style.width = '0%';
  const host = $('#q-list');
  host.innerHTML = paper.map((q,i)=>
    `<div class="panel q-item" id="qi-${q.id}">${qBody(q,i)}</div>`).join('');
  renderMath(host);
  paper.forEach(q=>{
    const panel = $('#qi-'+q.id);
    if (q.ty==='judge' || q.ty==='choice'){
      panel.querySelectorAll('.ans-btn').forEach(b=>b.onclick=()=>{
        if (answers[q.id]) return;                       // 已作答锁定
        panel.querySelectorAll('.ans-btn').forEach(x=>x.classList.add('done'));
        b.classList.add('picked');
        gradeObjective(q, b.dataset.v);
        const ok = answers[q.id].ok;
        const right = q.ty==='judge' ? q.ans : 'ABCD'[q.ans];
        $('#mark-'+q.id).innerHTML = ok
          ? '<span class="v right">✓ 得分</span>'
          : `<span class="v wrong">✗ 参考 ${right}</span>`;
        renderMath($('#mark-'+q.id));
        updateProgress();
      });
    } else if (q.ty==='blank'){
      const input = $('#blank-in-'+q.id), okBtn = $('#blank-ok-'+q.id);
      const submit = ()=>{
        const v = input.value.trim();
        if (!v || answers[q.id]) return;
        gradeObjective(q, v);
        const ok = answers[q.id].ok;
        input.classList.add(ok?'right':'wrong');
        input.disabled = true; okBtn.disabled = true;
        okBtn.textContent = ok ? '✓ 正确' : '✗ 参考：' + q.ans;
        renderMath(okBtn);
        $('#mark-'+q.id).innerHTML = ok
          ? '<span class="v right">✓ 得分</span>' : '<span class="v wrong">✗ 不得分</span>';
        updateProgress();
      };
      okBtn.onclick = submit;
      input.addEventListener('keydown', e=>{ if(e.key==='Enter') submit(); });
    } else {
      $('#btn-show-sol-'+q.id).onclick = ()=>{
        $('#sol-wrap-'+q.id).hidden = false;
        $('#btn-show-sol-'+q.id).disabled = true;
        renderMath($('#sol-wrap-'+q.id));
      };
    }
  });
  host.querySelectorAll('.ans-btn.self').forEach(b=>b.onclick=()=>{
    const qid = b.dataset.q;
    if (answers[qid]) return;
    const q = paper.find(x=>x.id===qid);
    answers[qid] = {self:b.dataset.v};
    recordWrongIfNeeded(q, b.dataset.v==='no');
    b.parentElement.querySelectorAll('.ans-btn').forEach(x=>x.classList.add('done'));
    b.classList.add('picked');
    $('#mark-'+qid).innerHTML = b.dataset.v==='ok'
      ? '<span class="v right">自评掌握</span>' : '<span class="v warn">自评待巩固</span>';
    updateProgress();
  });
  updateProgress();
}
function answeredCount(){
  return paper.filter(q=>{
    const a = answers[q.id];
    return a && (a.ok!==undefined || a.self);
  }).length;
}
function updateProgress(){
  const n = answeredCount();
  $('#bar-fill').style.width = (n/Math.max(1,paper.length)*100)+'%';
  $('#run-progress').textContent = `已作答 ${n} / ${paper.length}`;
}
function gradeObjective(q, v){
  let ok = false;
  if (q.ty==='judge') ok = v===q.ans;
  else if (q.ty==='choice') ok = +v===q.ans;
  else if (q.ty==='blank') ok = norm(v)===norm(q.ans);
  answers[q.id] = {ans:v, ok};
  recordWrongIfNeeded(q, !ok);
}
function recordWrongIfNeeded(q, bad){
  if (!bad) return;
  if (!wrongBook.find(w=>w.id===q.id)){
    wrongBook.push({id:q.id, ty:q.ty, ch:q.ch, kp:q.kp, src:q.src, q:q.q, opts:q.opts, ans:q.ans, sol:q.sol});
    LS.set('wrong', wrongBook);
    renderWrong();
  }
}

/* ---------- 成绩页 ---------- */
function finish(){
  $('#quiz-run').hidden = true;
  $('#quiz-result').hidden = false;
  $('#bar-fill').style.width = '100%';

  let objScore=0, objMax=0, objRight=0, objN=0, selfOk=0, selfNo=0;
  paper.forEach(q=>{
    const a = answers[q.id];
    if (TY[q.ty].客观){
      objN++; objMax += TY[q.ty].score;
      if (a && a.ok){ objScore += TY[q.ty].score; objRight++; }
    } else {
      if (a && a.self==='ok') selfOk++; else selfNo++;
    }
  });
  const selfScore = selfOk * TY.proof.score; // 自评按 6 分估算（保守）
  const est = objScore + selfScore;
  $('#score-line').textContent =
    `客观题 ${objScore} / ${objMax} 分${selfOk+selfNo? ` · 自评已掌握 ${selfOk}/${selfOk+selfNo}`:''}`;
  $('#score-sub').textContent =
    `预估总得分约 ${est} 分（主观题按自评每题 ${TY.proof.score} 分估算，仅供自查）`;

  const list = $('#result-list');
  list.innerHTML = paper.map((q,i)=>{
    const a = answers[q.id] || {};
    let verdict, detail;
    if (TY[q.ty].客观){
      verdict = a.ok ? '<span class="v right">✓ 得分</span>' : '<span class="v wrong">✗ 不得分</span>';
      const yours = q.ty==='judge' ? (a.ans||'未答') : q.ty==='choice' ? ('ABCD'[a.ans]||'未答') : (a.ans||'未答');
      const right = q.ty==='judge' ? q.ans : q.ty==='choice' ? 'ABCD'[q.ans] : q.ans;
      detail = `<p class="cmp">你的答案：<b>${yours}</b>${a.ok?'':'　参考答案：<b>'+right+'</b>'}</p>`;
    } else {
      verdict = a.self==='ok' ? '<span class="v right">自评掌握</span>' : '<span class="v warn">自评待巩固</span>';
      detail = `<div class="sol-box">${q.sol}</div>`;
    }
    return `<div class="panel res-item">
      <div class="res-h"><b>${i+1}</b> <span class="tychip t-${q.ty}">${TY[q.ty].name}</span>
        <span class="src">${q.src} · ${q.kp} · ${TY[q.ty].score}分</span> ${verdict}</div>
      <div class="res-q">${q.q}</div>
      ${detail}
    </div>`;
  }).join('');
  renderMath(list);
}

/* ---------- 错题本 ---------- */
function renderWrong(){
  $('#wrong-count').textContent = wrongBook.length ? `${wrongBook.length} 题` : '';
  const host = $('#wrong-list');
  host.innerHTML = wrongBook.length ? wrongBook.map(w=>`
    <details class="rv-card"><summary>${TY[w.ty].name} · ${w.kp} · ${w.src}</summary>
      <div class="rv-b"><div>${w.q}</div>
        ${w.opts?`<p>选项：${w.opts.join('　')}</p>`:''}
        ${w.ans?`<p class="cmp">参考答案：<b>${w.ans}</b></p>`:''}
        ${w.sol?`<div class="sol-box">${w.sol}</div>`:''}</div>
    </details>`).join('') : '<p class="muted">暂无错题——组卷开刷吧！</p>';
  renderMath(host);
}
renderWrong();
$('#btn-practice-wrong').onclick = ()=>{
  if (!wrongBook.length) return;
  paper = shuffle(wrongBook.slice());
  answers = {}; idx = 0;
  showRun();
};
$('#btn-clear-wrong').onclick = ()=>{
  if (!wrongBook.length) return;
  if (confirm('确定清空错题本？')){ wrongBook = []; LS.set('wrong', []); renderWrong(); }
};

/* ---------- 导航 ---------- */
$('#btn-start').onclick = ()=>{
  if (Object.values(counts).reduce((a,b)=>a+b,0)===0) return alert('请先设置至少 1 道题');
  buildPaper();
  if (!paper.length) return alert('该筛选范围下没有可用题目，放宽章节或来源试试');
  showRun();
};
$('#btn-submit').onclick = ()=>{
  const n = answeredCount();
  if (n < paper.length && !confirm(`还有 ${paper.length-n} 题未作答，确定交卷？未答题按不得分计。`)) return;
  finish();
};
$('#btn-quit').onclick = ()=>{
  if (confirm('放弃本次组卷？已作答内容不会保存。')){
    $('#quiz-run').hidden = true; $('#quiz-setup').hidden = false;
  }
};
$('#btn-again').onclick = ()=>{ $('#quiz-result').hidden = true; $('#quiz-setup').hidden = false; };
$('#btn-home').onclick = ()=>{ $('#quiz-result').hidden = true; $('#quiz-setup').hidden = false; };

/* ---------- 导出 PDF（浏览器打印 → 另存为 PDF） ---------- */
function buildPrintSheet(withSol){
  const total = paper.reduce((s,q)=>s+TY[q.ty].score,0);
  const d = new Date();
  const dateStr = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
  let h = `<div class="ps-head"><h1>《线性代数》模拟试卷</h1>
    <p class="ps-sub">${dateStr} 组卷 · 共 ${paper.length} 题 · 满分 ${total} 分</p>
    <p class="ps-rule">姓名＿＿＿＿＿＿　学号＿＿＿＿＿＿　得分＿＿＿＿＿＿</p></div>`;
  paper.forEach((q,i)=>{
    h += `<div class="ps-q"><p class="ps-no"><b>${i+1}.</b>［${TY[q.ty].name} · ${TY[q.ty].score}分］</p>
      <div class="ps-stem">${q.q}</div>`;
    if (q.ty==='judge'){
      h += `<p class="ps-bracket">（　　　　　）</p>`;
    } else if (q.ty==='choice' && q.opts){
      h += `<div class="ps-opts">${q.opts.map((o,j)=>`<p><b>${'ABCD'[j]}．</b>${o}</p>`).join('')}</div>`;
    } else if (q.ty==='solve'){
      h += `<div class="ps-space" style="min-height:215px"></div>`;
    } else if (q.ty==='proof'){
      h += `<div class="ps-space" style="min-height:150px"></div>`;
    }
    h += `</div>`;
  });
  if (withSol){
    h += `<h2 class="ps-sol-head">参考答案与解析</h2>`;
    paper.forEach((q,i)=>{
      let ans = '';
      if (q.ty==='judge') ans = q.ans;
      else if (q.ty==='choice') ans = 'ABCD'[q.ans];
      else if (q.ty==='blank') ans = String(q.ans||'');
      h += `<div class="ps-q"><p class="ps-no"><b>${i+1}.</b>［${TY[q.ty].name} · ${TY[q.ty].score}分］${ans?`　答案：<b>${ans}</b>`:''}</p>
        <div class="ps-stem">${q.q}</div>
        ${q.sol?`<div class="sol-box">${q.sol}</div>`:''}</div>`;
    });
  }
  $('#print-sheet').innerHTML = h;
  renderMath($('#print-wrap'));
}
$('#btn-export').onclick = ()=>{
  buildPrintSheet(false);
  setTimeout(()=>window.print(), 400);
};
$('#btn-export-sol').onclick = ()=>{
  buildPrintSheet(true);
  setTimeout(()=>window.print(), 400);
};

/* ---------- 题库统计 ---------- */
const statHost = $('#bank-stats');
if (statHost) statHost.innerHTML =
  `全题库 ${BANK_COUNT} 题：` +
  Object.keys(TY).map(ty=>`${TY[ty].name} ${BANK[ty].length}`).join(' · ');

})();
