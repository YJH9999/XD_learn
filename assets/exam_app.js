/* ============================================================
   XD_learn 备考中心 · 组卷模拟
   题型: judge 判断  choice 选择  blank 填空  solve 计算  proof 证明
   组卷: 题型数量 stepper + 章节 / 来源筛选 + 题库自选题
        分值: 题型分值、逐题分值、目标总分 都可改
   作答: 先选答案不判分，可反复修改；点「交卷」后统一判分并出详解
   错题: 待巩固 / 已攻克 两个分区；可随机抽错题或全量重做
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
  std:   {judge:10, choice:0, blank:5, solve:4, proof:2},
  choice:{judge:0, choice:5, blank:5, solve:4, proof:2},
  calc:  {judge:0, choice:0, blank:0, solve:8, proof:2},
  mini:  {judge:5, choice:0, blank:3, solve:2, proof:1}
};
const ORDER = ['judge','choice','blank','solve','proof'];

/* ---------- 题库合并 ---------- */
const BANK = {};
for (const ty of Object.keys(TY)) BANK[ty] = (window.XDBANK_OBJ && window.XDBANK_OBJ[ty]) || [];
const BANK_COUNT = Object.values(BANK).reduce((s,a)=>s+a.length,0);
const BYID = {};
Object.keys(TY).forEach(ty=>BANK[ty].forEach(q=>{ BYID[q.id] = Object.assign({ty}, q); }));

/* ---------- 状态 ---------- */
const $ = s => document.querySelector(s);
const $$ = s => Array.from(document.querySelectorAll(s));
const LS = {
  get(k,d){ try{ return JSON.parse(localStorage.getItem('xd_'+k)) ?? d; }catch(e){ return d; } },
  set(k,v){ localStorage.setItem('xd_'+k, JSON.stringify(v)); }
};
let paper = [];        // 当前试卷（题目副本，带 pts）
let answers = {};      // {id:{ans, self}}  —— 交卷前不判分
let graded = null;     // 交卷后的判分结果
let wrongBook = LS.get('wrong', []);
wrongBook.forEach(w=>{ if (!w.status) w.status = 'open'; });   // 兼容旧数据
let filterChs = [];    // 多选章节；空数组 = 全部章节
let filterSrc = '';
let counts = {...PRESETS.std};
let pts = {};          // 题型分值（可编辑）
ORDER.forEach(ty=>{ pts[ty] = TY[ty].score; });
let targetTotal = 100;
let curRec = null;
let picks = [];        // 题库自选的题目 id

/* ---------- 视图切换 ---------- */
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
  if(h==='quiz'||h==='bank') showView(h);
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
  const go = ()=>{
    if (!window.renderMathInElement) return;
    renderMathInElement(el, {
      delimiters:[
        {left:'$$', right:'$$', display:true},
        {left:'\\[', right:'\\]', display:true},
        {left:'\\(', right:'\\)', display:false}
      ],
      throwOnError:false,
      strict:false,
      macros:{"\\bm":"\\boldsymbol","\\R":"\\mathbb{R}","\\E":"\\mathbb{E}",
              "\\arccot":"\\operatorname{arccot}","\\arcsec":"\\operatorname{arcsec}","\\arccsc":"\\operatorname{arccsc}","\\cdotp":"\\cdot"}
    });
  };
  if (window.renderMathInElement) go();
  else if (document.readyState === 'loading')
    document.addEventListener('DOMContentLoaded', go, {once:true});
  else
    window.addEventListener('load', go, {once:true});
}
function fmtAns(a){
  const s = String(a==null?'':a);
  if (!s) return '';
  if (s.includes('\\(') || s.includes('$$') || s.includes('\\[') || !/\\[a-zA-Z]+/.test(s)) return s;
  return '\\(' + s + '\\)';
}

/* ---------- 分值 ---------- */
function availCount(ty){
  return BANK[ty].filter(q=>
    (!filterChs.length || filterChs.indexOf(q.ch)>=0) &&
    (!filterSrc || (q.src||'').includes(filterSrc))
  ).length;
}
function setupTotal(){
  let t = 0;
  for (const ty of ORDER) t += counts[ty] * pts[ty];
  return Math.round(t*10)/10;
}
function paperTotal(){
  return Math.round(paper.reduce((s,q)=>s+ptsOf(q),0)*10)/10;
}
function ptsOf(q){ return q && q.pts!=null ? +q.pts : (pts[q.ty] || 0); }

/* ---------- 组卷面板 ---------- */
function refreshSetup(){
  $$('#type-row .type-cell').forEach(cell=>{
    const ty = cell.dataset.ty;
    cell.querySelector('.stepper b').textContent = counts[ty];
    const inp = cell.querySelector('.pts-in');
    if (inp && document.activeElement!==inp) inp.value = pts[ty];
    const n = availCount(ty);
    const warn = counts[ty] > n;
    cell.classList.toggle('lack', warn);
    const av = cell.querySelector('.t-avail');
    if (av) av.textContent = n;
    const sub = cell.querySelector('.t-sum');
    if (sub) sub.textContent = counts[ty] ? `共 ${Math.round(counts[ty]*pts[ty]*10)/10} 分` : '未选';
    cell.title = warn ? `题库中该范围内仅 ${n} 题，组卷时将按实际数量抽取` : `可用 ${n} 题`;
  });
  const nQ = Object.values(counts).reduce((a,b)=>a+b,0);
  const t = setupTotal();
  const tip = $('#paper-total');
  if (tip) tip.innerHTML = `本次组卷：<b>${nQ}</b> 题 · 共 <b>${t}</b> 分`
    + (Math.abs(t-targetTotal)>0.01 ? `<span class="tt-diff">（目标 ${targetTotal} 分）</span>` : '');
  const tt = $('#total-target');
  if (tt && document.activeElement!==tt) tt.value = targetTotal;
}
$$('#type-row .stepper button').forEach(b=>b.onclick=()=>{
  const cell = b.closest('.type-cell');
  const ty = cell.dataset.ty;
  counts[ty] = Math.max(0, Math.min(30, counts[ty] + +b.dataset.d));
  refreshSetup();
});
$$('#type-row .pts-in').forEach(inp=>{
  inp.addEventListener('change', ()=>{
    const ty = inp.dataset.ty;
    const v = Math.max(0, Math.round((+inp.value||0)*10)/10);
    pts[ty] = v; inp.value = v; refreshSetup();
  });
});
(function(){
  const tt = $('#total-target'), btn = $('#btn-scale');
  if (tt) tt.addEventListener('change', ()=>{
    targetTotal = Math.max(1, Math.round((+tt.value||0)*10)/10);
    tt.value = targetTotal; refreshSetup();
  });
  if (btn) btn.onclick = ()=>scaleToTarget();
})();
/* 按目标总分折算各题型每题分值（题量不变） */
function scaleToTarget(){
  const nQ = ORDER.reduce((s,ty)=>s+counts[ty],0);
  if (!nQ) return alert('请先设置题量');
  const base = setupTotal();
  if (!base) return;
  const k = targetTotal / base;
  let acc = 0;
  const last = ORDER.slice().reverse().find(ty=>counts[ty]>0);
  ORDER.forEach(ty=>{
    if (!counts[ty]) return;
    if (ty===last){
      const rest = targetTotal - acc;
      pts[ty] = Math.max(0.5, Math.round(rest/counts[ty]*10)/10);
    }else{
      const v = Math.max(0.5, Math.round(pts[ty]*k*10)/10);
      pts[ty] = v; acc += v*counts[ty];
    }
  });
  refreshSetup();
}
$$('#ch-row .chip').forEach(b=>b.onclick=()=>{
  const v = b.dataset.ch;
  if (!v){
    filterChs = [];
  }else{
    const n = +v, i = filterChs.indexOf(n);
    if (i>=0) filterChs.splice(i,1); else filterChs.push(n);
  }
  syncChChips(); refreshSetup();
});
function syncChChips(){
  $$('#ch-row .chip').forEach(x=>{
    const v = x.dataset.ch;
    x.classList.toggle('on', v ? filterChs.indexOf(+v)>=0 : !filterChs.length);
  });
}
$$('#src-row .chip').forEach(b=>b.onclick=()=>{
  $$('#src-row .chip').forEach(x=>x.classList.remove('on'));
  b.classList.add('on'); filterSrc = b.dataset.src; refreshSetup();
});
$$('.preset-row .chip').forEach(b=>b.onclick=()=>{
  counts = {...PRESETS[b.dataset.preset]};
  $$('.preset-row .chip').forEach(x=>x.classList.toggle('on', x===b));
  refreshSetup();
});
refreshSetup();

/* ---------- 抽题组卷 ---------- */
function shuffle(a){ for(let i=a.length-1;i>0;i--){ const j=Math.random()*(i+1)|0; [a[i],a[j]]=[a[j],a[i]]; } return a; }
function draw(ty, n){
  const pool = shuffle(BANK[ty].filter(q=>
    (!filterChs.length || filterChs.indexOf(q.ch)>=0) &&
    (!filterSrc || (q.src||'').includes(filterSrc))
  ).map(q=>q));
  return pool.slice(0, n);
}
/* picked 为空 = 按题量随机抽；否则用自选题目 */
function buildPaper(picked){
  paper = []; answers = {}; graded = null;
  if (picked && picked.length){
    const sel = picked.map(q=>Object.assign({}, q, {pts: q.pts!=null ? q.pts : (pts[q.ty]||0)}));
    sel.sort((a,b)=>ORDER.indexOf(a.ty)-ORDER.indexOf(b.ty));
    paper = sel;
  }else{
    for (const ty of ORDER){
      if (counts[ty]>0) paper.push(...draw(ty, counts[ty]).map(q=>Object.assign({}, q, {pts: pts[ty]})));
    }
  }
  startRecord();
}

/* ---------- 试卷记录（kb-paper.js） ---------- */
function startRecord(){
  if (!window.KBPaper) return;
  const d = new Date();
  curRec = {
    id: KBPaper.uid(), ts: Date.now(),
    title: `${d.getMonth()+1}月${d.getDate()}日 ${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')} 组卷`,
    n: paper.length, total: paperTotal(),
    qs: paper.map(q=>q.id),
    pts: {}, ans: {}, done: false, score: null, secs: 0,
    src: filterSrc || '', chs: filterChs.slice()
  };
  paper.forEach(q=>{ curRec.pts[q.id] = ptsOf(q); });
  KBPaper.put(curRec);
  renderHistory();
}
function syncRecord(){
  if (!curRec || !window.KBPaper) return;
  const a = {};
  paper.forEach(q=>{ if (answers[q.id]) a[q.id] = answers[q.id]; });
  curRec.ans = a;
  curRec.total = paperTotal();
  curRec.pts = {};
  paper.forEach(q=>{ curRec.pts[q.id] = ptsOf(q); });
  if (!curRec.done) curRec.secs = Math.round((Date.now()-curRec.ts)/1000);
  KBPaper.put(curRec);
}
function renderHistory(){
  const host = $('#history-list');
  if (!host) return;
  if (!window.KBPaper){ host.innerHTML = '<p class="muted">试卷记录模块未加载</p>'; return; }
  const n = KBPaper.list().length;
  const cnt = $('#hist-count');
  if (cnt) cnt.textContent = n ? `${n} 份` : '';
  KBPaper.render(host, { onOpen: openRecord, attOpts: rec=>({ estSec: estFromRec(rec) }) });
}
function estFromRec(rec){
  if (rec && rec.estSec) return rec.estSec;
  let s = 0;
  ((rec && rec.qs) || []).forEach(id=>{ const q = BYID[id]; if (q) s += (EXAM_MIN[q.ty] || 2); });
  return Math.round(Math.min(s, 150) * 60);
}
function openRecord(rec, act){
  const qs = (rec.qs||[]).map(id=>BYID[id]).filter(Boolean);
  if (!qs.length) return alert('题库里已找不到这份卷子的题目了（题库可能更新过）');
  const cp = qs.map(q=>{
    const o = Object.assign({}, q);
    o.pts = (rec.pts && rec.pts[q.id]!=null) ? rec.pts[q.id] : (pts[q.ty]||0);
    return o;
  });
  if (act==='redo'){
    paper = shuffle(cp.slice());
    answers = {}; graded = null;
    startRecord();
    showRun();
    return;
  }
  paper = cp;
  answers = {};
  Object.keys(rec.ans||{}).forEach(k=>{ answers[k] = rec.ans[k]; });
  curRec = rec;
  if (rec.done){
    graded = computeResult();
    showResult(true);
  }else{
    graded = null;
    showRun();
  }
}

/* ---------- 作答视图 ---------- */
function showRun(){
  $('#quiz-setup').hidden = true;
  $('#quiz-result').hidden = true;
  $('#quiz-run').hidden = false;
  renderAll();
  window.scrollTo(0,0);
}

const EXAM_MIN = {judge:1.2, choice:1.8, blank:2.5, solve:10, proof:12};
function estSeconds(){
  let s = 0;
  paper.forEach(q=>{ s += (EXAM_MIN[q.ty] || 2); });
  return Math.round(Math.min(s, 150) * 60);
}
/* ---------- 打印：等 KaTeX 字体真正加载完再弹打印对话框 ---------- */
const KATEX_FONTS = ['KaTeX_Main','KaTeX_Math','KaTeX_AMS','KaTeX_Caligraphic','KaTeX_Fraktur',
  'KaTeX_SansSerif','KaTeX_Script','KaTeX_Size1','KaTeX_Size2','KaTeX_Size3','KaTeX_Size4','KaTeX_Typewriter'];
function printAfterFonts(){
  const wrap = document.getElementById('print-wrap');
  if (wrap) wrap.classList.add('ps-prep');
  const jobs = [];
  if (document.fonts && document.fonts.load && document.fonts.ready) {
    KATEX_FONTS.forEach(f=>{ try{ jobs.push(document.fonts.load('16px "'+f+'"').catch(()=>{})); }catch(e){} });
    jobs.push(document.fonts.ready);
  }
  const done = ()=>{ if (wrap) wrap.classList.remove('ps-prep'); try{ window.print(); }catch(e){} };
  Promise.all(jobs).then(()=>new Promise(r=>setTimeout(r,150))).then(done).catch(done);
  if (wrap) setTimeout(()=>wrap.classList.remove('ps-prep'), 30000);
  window.addEventListener('afterprint', function once(){ wrap && wrap.classList.remove('ps-prep'); window.removeEventListener('afterprint', once); });
}
function printBlank(){ buildPrintSheet('blank'); printAfterFonts(); }
function printAns(){ buildPrintSheet('sol'); printAfterFonts(); }
function askMode(){
  if (!window.KBPaper){ showRun(); return; }
  KBPaper.chooseMode({
    rec: curRec,
    estSec: estSeconds(),
    n: paper.length,
    total: paperTotal(),
    printBlank, printAns,
    onOnline: showRun,
    onOffline: ()=>{ $('#quiz-setup').hidden = false; renderHistory(); },
    onCancel: ()=>{ $('#quiz-setup').hidden = false; renderHistory(); }
  });
}
function norm(s){
  return (s||'').replace(/\s|\\,|\\;|\\quad|\\qquad/g,'')
    .replace(/\\\\/g,'\\').toLowerCase();
}
function isRight(q, v){
  if (v===null || v===undefined) return false;
  if (q.ty==='judge') return String(v).replace('√','✓')===String(q.ans).replace('√','✓');
  if (q.ty==='choice') return +v===+q.ans;
  return norm(v)===norm(q.ans);
}

/* ---------- 题目卡片（作答态，不判分） ---------- */
function qBody(q, i){
  let body = `<div class="res-h"><b>${i+1}</b> <span class="tychip t-${q.ty}">${TY[q.ty].name}</span>
    <span class="src">${q.src||''} · ${q.kp||''}</span>
    <span class="ptsbox">分值 <input class="ptq" type="number" min="0" step="0.5" value="${ptsOf(q)}" data-q="${q.id}"> 分</span>
    </div>
    <div class="q-stem">${q.q}</div>`;
  if (q.ty==='judge'){
    body += `<div class="ans-row">
      <button class="ans-btn" type="button" data-v="✓">✓ 正确</button>
      <button class="ans-btn" type="button" data-v="×">× 错误</button></div>`;
  } else if (q.ty==='choice'){
    body += `<div class="ans-row col">` + q.opts.map((o,j)=>
      `<button class="ans-btn" type="button" data-v="${j}"><b>${'ABCD'[j]}</b> ${fmtAns(o)}</button>`).join('') + `</div>`;
  } else if (q.ty==='blank'){
    body += `<div class="ans-row"><input class="blank-in" id="blank-in-${q.id}" placeholder="填写答案（式子可用 LaTeX，如 \\frac12）" autocomplete="off"></div>`;
  } else {
    body += `<div class="self-note">在纸上写出完整过程，交卷后对照参考答案自评。</div>
      <textarea class="subj-in" id="subj-${q.id}" rows="3" placeholder="可在这里记下关键步骤（选填，交卷后一起看详解）"></textarea>`;
  }
  return body;
}
/* 已作答题目在重绘后的还原（不显示对错） */
function applyAnswered(q, panel){
  const a = answers[q.id];
  if (!a) return;
  if (q.ty==='judge' || q.ty==='choice'){
    panel.querySelectorAll('.ans-btn').forEach(x=>{
      if (String(x.dataset.v)===String(a.ans)) x.classList.add('picked');
    });
  } else if (q.ty==='blank'){
    const input = $('#blank-in-'+q.id);
    if (input) input.value = a.ans==null?'':a.ans;
  } else {
    const ta = $('#subj-'+q.id);
    if (ta) ta.value = a.ans||'';
  }
}

function renderAll(){
  $('#run-type').textContent = `模拟试卷 · 共 ${paper.length} 题 · ${paperTotal()} 分`;
  $('#bar-fill').style.width = '0%';
  const tip = $('#run-tip');
  if (tip) tip.textContent = '作答过程中只记录选择、不判对错，随时可以改；点「交卷判分」后统一出分数、正确答案与详解。';
  const host = $('#q-list');
  host.innerHTML = paper.map((q,i)=>
    `<div class="panel q-item" id="qi-${q.id}">${qBody(q,i)}</div>`).join('');
  renderMath(host);
  paper.forEach(q=>{
    const panel = $('#qi-'+q.id);
    if (!panel) return;
    const ptIn = panel.querySelector('.ptq');
    if (ptIn) ptIn.onchange = ()=>{
      const v = Math.max(0, Math.round((+ptIn.value||0)*10)/10);
      q.pts = v; ptIn.value = v;
      $('#run-type').textContent = `模拟试卷 · 共 ${paper.length} 题 · ${paperTotal()} 分`;
      syncRecord();
    };
    if (q.ty==='judge' || q.ty==='choice'){
      panel.querySelectorAll('.ans-btn').forEach(b=>{
        b.onclick = ()=>{
          if (graded) return;
          panel.querySelectorAll('.ans-btn').forEach(x=>x.classList.remove('picked'));
          b.classList.add('picked');
          answers[q.id] = {ans: b.dataset.v};
          updateProgress(); syncRecord();
        };
      });
    } else if (q.ty==='blank'){
      const input = $('#blank-in-'+q.id);
      if (input) input.addEventListener('input', ()=>{
        const v = input.value.trim();
        if (v) answers[q.id] = {ans:v}; else delete answers[q.id];
        updateProgress(); queueSync();
      });
    } else {
      const ta = $('#subj-'+q.id);
      if (ta) ta.addEventListener('input', ()=>{
        const v = ta.value.trim();
        if (v) answers[q.id] = {ans:v}; else delete answers[q.id];
        updateProgress(); queueSync();
      });
    }
    applyAnswered(q, panel);
  });
  updateProgress();
}
let _syncT = null;
function queueSync(){ clearTimeout(_syncT); _syncT = setTimeout(syncRecord, 500); }

function answeredCount(){
  return paper.filter(q=>{
    const a = answers[q.id];
    return a && a.ans!==undefined && a.ans!==null && String(a.ans).trim()!=='';
  }).length;
}
function updateProgress(){
  const n = answeredCount();
  $('#bar-fill').style.width = (n/Math.max(1,paper.length)*100)+'%';
  $('#run-progress').textContent = `已作答 ${n} / ${paper.length}`;
}

/* ---------- 判分（交卷时一次算完） ---------- */
function computeResult(){
  const byId = {};
  let total=0, objScore=0, objTotal=0, objRight=0, objN=0, selfScore=0, selfOk=0, selfN=0;
  paper.forEach(q=>{
    const P = ptsOf(q);
    total += P;
    const a = answers[q.id];
    if (TY[q.ty].客观){
      objN++; objTotal += P;
      const ok = !!(a && isRight(q, a.ans));
      if (ok){ objScore += P; objRight++; }
      byId[q.id] = {ok, ans: a?a.ans:null, pts:P};
    }else{
      selfN++;
      const self = a && a.self;
      if (self==='ok'){ selfOk++; selfScore += P; }
      byId[q.id] = {ok: self==='ok', ans: a?a.ans:null, self: self||null, pts:P};
    }
  });
  const score = Math.round((objScore+selfScore)*10)/10;
  return {
    byId, total: Math.round(total*10)/10,
    objScore: Math.round(objScore*10)/10, objTotal: Math.round(objTotal*10)/10,
    objRight, objN, selfScore: Math.round(selfScore*10)/10, selfOk, selfN,
    score, pct: total ? Math.round(score/total*100) : 0
  };
}

/* ---------- 成绩页 ---------- */
function showResult(replay){
  $('#quiz-run').hidden = true;
  $('#quiz-setup').hidden = true;
  $('#quiz-result').hidden = false;
  $('#bar-fill').style.width = '100%';
  const g = graded || computeResult();
  const grade = g.pct>=90?'优秀':g.pct>=75?'良好':g.pct>=60?'及格':'需加强';
  $('#score-line').innerHTML = `${g.score}<span class="score-den"> / ${g.total}</span> <em class="score-grade">${grade}</em>`;
  const parts = [`客观题 ${g.objScore} / ${g.objTotal} 分（答对 ${g.objRight}/${g.objN}）`];
  if (g.selfN) parts.push(`主观题自评 ${g.selfScore} / ${g.total - g.objTotal} 分（掌握 ${g.selfOk}/${g.selfN}）`);
  parts.push(replay?'历史卷面':'本次用时 ' + fmtSecs(curRec && curRec.secs));
  const nWrong = paper.filter(q=>{ const r=g.byId[q.id]; return r && !r.ok && (r.ans!=null || r.self==='no'); }).length;
  if (nWrong) parts.push(`本次错 ${nWrong} 题已收入错题本`);
  $('#score-sub').textContent = parts.join(' · ');

  const list = $('#result-list');
  list.innerHTML = paper.map((q,i)=>resItem(q, i, g.byId[q.id])).join('');
  renderMath(list);
  bindResultActions();
}
function fmtSecs(s){
  s = Math.round(s||0);
  if (s<60) return s+' 秒';
  return Math.floor(s/60)+' 分 '+(s%60)+' 秒';
}
function resItem(q, i, r){
  const P = r ? r.pts : ptsOf(q);
  const got = r && r.ok ? P : 0;
  const verdict = r && r.ok
    ? `<span class="v right">✓ 得 ${got} / ${P} 分</span>`
    : `<span class="v wrong">✗ 得 0 / ${P} 分</span>`;
  let ansHtml = '';
  if (q.ty==='choice'){
    ansHtml = `<div class="ans-row col res-opts">` + q.opts.map((o,j)=>{
      const cls = ['ans-btn'];
      if (j===+q.ans) cls.push('rightopt');
      else if (r && !r.ok && j===+r.ans) cls.push('wrongpick');
      return `<div class="${cls.join(' ')}"><b>${'ABCD'[j]}</b> ${fmtAns(o)}</div>`;
    }).join('') + `</div>
    <p class="cmp">你的答案：<b class="${r&&r.ok?'ok':'no'}">${r&&r.ans!=null?'ABCD'[r.ans]:'未作答'}</b>　正确答案：<b class="ok">${'ABCD'[q.ans]}</b></p>`;
  } else if (q.ty==='judge'){
    ansHtml = `<p class="cmp">你的答案：<b class="${r&&r.ok?'ok':'no'}">${r&&r.ans!=null?r.ans:'未作答'}</b>　正确答案：<b class="ok">${q.ans}</b></p>`;
  } else if (q.ty==='blank'){
    ansHtml = `<p class="cmp">你的答案：<b class="${r&&r.ok?'ok':'no'}">${fmtAns(r&&r.ans!=null?r.ans:'未作答')}</b>　参考答案：<b class="ok">${fmtAns(q.ans)}</b></p>`;
  } else {
    ansHtml = (r && r.ans) ? `<p class="cmp">你的要点：<b>${r.ans}</b></p>` : '';
    ansHtml += `<div class="self-row">对照答案自评：
      <button class="ans-btn self" type="button" data-self="ok" data-q="${q.id}">已掌握</button>
      <button class="ans-btn self bad" type="button" data-self="no" data-q="${q.id}">还需巩固</button></div>`;
  }
  return `<div class="panel res-item ${r&&r.ok?'ok':'bad'}">
    <div class="res-h"><b>${i+1}</b> <span class="tychip t-${q.ty}">${TY[q.ty].name}</span>
      <span class="src">${q.src||''} · ${q.kp||''} · ${P} 分</span> ${verdict}</div>
    <div class="res-q">${q.q}</div>
    ${ansHtml}
    ${q.sol?`<div class="sol-box"><b class="sol-t">解析</b>${q.sol}</div>`:''}
  </div>`;
}
function bindResultActions(){
  const rb = $('#btn-redo-wrong');
  if (rb) rb.onclick = ()=>{
    const ids = paper.filter(q=>{ const r=(graded||computeResult()).byId[q.id]; return r && !r.ok; })
      .map(q=>q.id);
    if (!ids.length) return alert('本次没有错题');
    paper = shuffle(ids.map(id=>{
      const q = BYID[id] || paper.find(x=>x.id===id);
      const o = Object.assign({}, q);
      o.pts = pts[q.ty] || 5;
      return o;
    }));
    answers = {}; graded = null;
    startRecord(); showRun();
  };
  $$('#result-list .ans-btn.self').forEach(b=>{
    b.onclick = ()=>{
      const qid = b.dataset.q;
      const q = paper.find(x=>x.id===qid);
      if (!q) return;
      answers[qid] = Object.assign({}, answers[qid], {self:b.dataset.self});
      graded = computeResult();
      if (b.dataset.self==='ok'){ markFixed(q); } else { upsertWrong(q, 'open'); }
      if (window.KBStats) KBStats.answer(b.dataset.self==='ok');
      renderWrong();
      showResult(true);
      syncRecord();
    };
  });
}

/* ---------- 错题本 ---------- */
function upsertWrong(q, status){
  let w = wrongBook.find(x=>x.id===q.id);
  if (!w){
    wrongBook.push({id:q.id, ty:q.ty, ch:q.ch, kp:q.kp, src:q.src, q:q.q, opts:q.opts,
      ans:q.ans, sol:q.sol, status:status, ts:Date.now(), tries:1});
  }else{
    w.status = status; w.ts = Date.now(); w.tries = (w.tries||1)+1;
  }
  LS.set('wrong', wrongBook);
}
function markFixed(q){
  const w = wrongBook.find(x=>x.id===q.id);
  if (!w) return;                     // 没做错过的题答对不记录
  w.status = 'fixed'; w.ts = Date.now(); w.tries = (w.tries||1)+1;
  LS.set('wrong', wrongBook);
}
function wrongPool(includeFixed){
  return wrongBook.filter(w=> w.status==='open' || (!!includeFixed && w.status==='fixed'));
}
function renderWrong(){
  const open = wrongBook.filter(w=>w.status!=='fixed');
  const fixed = wrongBook.filter(w=>w.status==='fixed');
  const cnt = $('#wrong-count');
  if (cnt) cnt.textContent = open.length ? `${open.length} 题待巩固` : '';
  const fc = $('#wrong-fixed-count');
  if (fc) fc.textContent = fixed.length ? `${fixed.length} 题` : '';
  const fw = $('#wrong-fixed-wrap');
  if (fw) fw.hidden = !fixed.length;
  const card = w=>{
    const ty = TY[w.ty] || {name:''};
    return `<details class="rv-card"><summary>
      <span class="tychip t-${w.ty}">${ty.name}</span>
      <span class="bk-meta">${w.kp||''} · ${w.src||''}${w.status==='fixed'?' · 已攻克':''}</span></summary>
      <div class="rv-b"><div>${w.q}</div>
        ${w.opts?`<p class="cmp">选项：${w.opts.map((o,j)=>'ABCD'[j]+'．'+o).join('　')}</p>`:''}
        ${w.ans?`<p class="cmp">参考答案：<b>${fmtAns(w.ty==='choice'?'ABCD'[w.ans]:w.ans)}</b></p>`:''}
        ${w.sol?`<div class="sol-box">${w.sol}</div>`:''}</div>
    </details>`;
  };
  const host = $('#wrong-open');
  if (host) host.innerHTML = open.length ? open.map(card).join('')
    : '<p class="muted">暂无待巩固错题——组卷开刷吧！</p>';
  const fhost = $('#wrong-fixed');
  if (fhost) fhost.innerHTML = fixed.map(card).join('');
  const wb = $('#wrongbook-panel');
  if (wb) renderMath(wb);
}
renderWrong();
renderHistory();

function startWrong(mode){
  const inc = $('#wfix-join') && $('#wfix-join').checked;
  const pool = wrongPool(inc).map(w=>{
    const q = BYID[w.id];
    const base = q ? Object.assign({}, q) : Object.assign({}, w);
    base.pts = pts[base.ty] || (TY[base.ty] ? TY[base.ty].score : 5);
    return base;
  });
  if (!pool.length) return alert(inc ? '错题本是空的' : '没有待巩固的错题');
  const list = mode==='all' ? shuffle(pool.slice()) : shuffle(pool.slice()).slice(0, 10);
  paper = list; answers = {}; graded = null;
  startRecord();
  showRun();
}
(function(){
  const r = $('#btn-practice-wrong'), a = $('#btn-wrong-all');
  if (r) r.onclick = ()=>startWrong('random');
  if (a) a.onclick = ()=>startWrong('all');
  const c = $('#btn-clear-wrong');
  if (c) c.onclick = ()=>{
    if (!wrongBook.length) return;
    if (confirm('确定清空错题本？已攻克的记录也会一起清掉。')){
      wrongBook = []; LS.set('wrong', []); renderWrong();
    }
  };
})();

/* ---------- 导航 ---------- */
$('#btn-start').onclick = ()=>{
  if (Object.values(counts).reduce((a,b)=>a+b,0)===0) return alert('请先设置至少 1 道题，或在题库里自选题目');
  buildPaper(null);
  if (!paper.length){
    if (curRec && window.KBPaper) KBPaper.del(curRec.id);
    return alert('该筛选范围下没有可用题目，放宽章节或来源试试');
  }
  askMode();
};
$('#btn-submit').onclick = ()=>{
  const n = answeredCount();
  if (n < paper.length && !confirm(`还有 ${paper.length-n} 题未作答，确定交卷？未答题按 0 分计。`)) return;
  submitPaper();
};
function submitPaper(){
  graded = computeResult();
  const g = graded;
  /* 统计：交卷时只统计客观题，主观题在自评时单独记 */
  let objAnswered = 0;
  paper.forEach(q=>{ if (TY[q.ty].客观 && answers[q.id] && answers[q.id].ans!=null) objAnswered++; });
  if (window.KBStats) KBStats.batch(objAnswered, g.objRight);
  paper.forEach(q=>{
    const r = g.byId[q.id];
    if (TY[q.ty].客观){
      if (!r || r.ans==null) return;
      if (r.ok) markFixed(q); else upsertWrong(q, 'open');
    }
  });
  if (curRec && window.KBPaper){
    curRec.done = true;
    curRec.score = g.score;
    curRec.total = g.total;
    curRec.secs = Math.round((Date.now()-(curRec.ts||Date.now()))/1000);
    syncRecord();
    renderHistory();
  }
  renderWrong();
  showResult(false);
  window.scrollTo(0,0);
}
$('#btn-quit').onclick = ()=>{
  syncRecord();
  $('#quiz-run').hidden = true; $('#quiz-setup').hidden = false;
  renderHistory();
};
$('#btn-again').onclick = ()=>{ $('#quiz-result').hidden = true; $('#quiz-setup').hidden = false; renderHistory(); };
$('#btn-home').onclick = ()=>{ $('#quiz-result').hidden = true; $('#quiz-setup').hidden = false; renderHistory(); };

/* ---------- 导出（浏览器打印 → 另存为 PDF） ---------- */
function sheetHead(title, sub, withRule){
  const d = new Date();
  const dateStr = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
  return `<div class="ps-head"><h1>${title}</h1>
    <p class="ps-sub">${dateStr} · ${sub}</p>
    ${withRule===false?'':'<p class="ps-rule">姓名＿＿＿＿＿＿　学号＿＿＿＿＿＿　得分＿＿＿＿＿＿</p>'}
  </div>`;
}
function ansOf(q){
  if (q.ty==='judge') return q.ans;
  if (q.ty==='choice') return 'ABCD'[q.ans];
  return String(q.ans==null?'':q.ans);
}
function psNo(q, i){
  return `<p class="ps-no"><b>${i+1}.</b>［${TY[q.ty].name} · ${ptsOf(q)}分］${q.src?`<span class="ps-src">［${q.src}］</span>`:''}</p>`;
}
function buildPrintSheet(mode){
  const isAns = (mode==='sol');
  let h = '';

  if (mode==='wrong'){
    const all = wrongBook.slice();
    h = sheetHead('《线性代数》错题本', `共 ${all.length} 题 · 待巩固 ${all.filter(w=>w.status!=='fixed').length} · 已攻克 ${all.filter(w=>w.status==='fixed').length}`, false);
    all.forEach((w,i)=>{
      h += `<div class="ps-q">${psNo({ty:w.ty,src:w.src,pts:pts[w.ty]}, i)}
        <div class="ps-stem">${w.q}</div>`;
      if (w.opts) h += `<div class="ps-opts">${w.opts.map((o,j)=>`<p><b>${'ABCD'[j]}．</b>${o}</p>`).join('')}</div>`;
      h += `<p class="cmp">参考答案：<b>${fmtAns(w.ty==='choice'?'ABCD'[w.ans]:w.ans)}</b>
        ${w.kp?`　<span class="ps-kp">［考点：${w.kp}］</span>`:''}${w.status==='fixed'?'　<span class="ps-kp">［已攻克］</span>':''}</p>
        ${w.sol?`<div class="sol-box">${w.sol}</div>`:''}</div>`;
    });
    if (!all.length) h += '<p class="ps-sub">暂无错题。</p>';
    $('#print-sheet').innerHTML = h;
    renderMath($('#print-wrap'));
    return;
  }

  if (mode==='answers'){
    const g = graded || computeResult();
    const d = curRec && curRec.ts ? new Date(curRec.ts) : new Date();
    const stamp = `${d.getMonth()+1}月${d.getDate()}日 ${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}`;
    h = sheetHead('《线性代数》作答记录',
      `${stamp} 组卷 · 共 ${paper.length} 题 · ${g.score}/${g.total} 分 · 客观题 ${g.objScore}/${g.objTotal}`, false);
    paper.forEach((q,i)=>{
      const a = answers[q.id] || {};
      const r = g.byId[q.id] || {};
      let mine = '未作答', verdict = '';
      if (TY[q.ty].客观){
        if (q.ty==='judge') mine = a.ans || '未作答';
        else if (q.ty==='choice') mine = (a.ans===undefined || a.ans===null) ? '未作答' : ('ABCD'[a.ans] || '未作答');
        else mine = a.ans || '未作答';
        verdict = r.ok ? `　<b class="ok">✓ 得 ${r.pts} 分</b>` : `　<b class="no">✗ 得 0 分</b>　参考答案：<b>${fmtAns(ansOf(q))}</b>`;
      }else{
        mine = a.self==='ok' ? '自评：已掌握' : a.self==='no' ? '自评：还需巩固' : '未自评';
        verdict = a.self==='ok' ? '　<b class="ok">✓ 自评掌握</b>' : a.self==='no' ? '　<b class="warn">自评待巩固</b>' : '';
      }
      h += `<div class="ps-q">${psNo(q,i)}
        <div class="ps-stem">${q.q}</div>
        ${(q.ty==='choice' && q.opts)?`<div class="ps-opts">${q.opts.map((o,j)=>`<p><b>${'ABCD'[j]}．</b>${o}</p>`).join('')}</div>`:''}
        <p class="cmp">我的作答：<b>${fmtAns(mine)}</b>${verdict}</p>
        ${q.kp?`<p class="cmp"><span class="ps-kp">［考点：${q.kp}］</span></p>`:''}
        ${q.sol?`<div class="sol-box">${q.sol}</div>`:''}</div>`;
    });
    $('#print-sheet').innerHTML = h;
    renderMath($('#print-wrap'));
    return;
  }

  const total = paperTotal();
  h = sheetHead('《线性代数》模拟试卷', `共 ${paper.length} 题 · 满分 ${total} 分`, true);
  paper.forEach((q,i)=>{
    h += `<div class="ps-q">${psNo(q,i)}
      <div class="ps-stem">${q.q}</div>`;
    if (q.ty==='judge'){
      h += `<p class="ps-bracket">（　　　　　）</p>`;
    } else if (q.ty==='choice' && q.opts){
      h += `<div class="ps-opts">${q.opts.map((o,j)=>`<p><b>${'ABCD'[j]}．</b>${o}</p>`).join('')}</div>`;
    } else if (q.ty==='blank'){
      h += `<div class="ps-space" style="min-height:56px"></div>`;
    } else if (q.ty==='solve'){
      h += `<div class="ps-space" style="min-height:300px"></div>`;
    } else if (q.ty==='proof'){
      h += `<div class="ps-space" style="min-height:240px"></div>`;
    }
    h += `</div>`;
  });
  if (isAns){
    h += `<h2 class="ps-sol-head">参考答案与解析</h2>`;
    paper.forEach((q,i)=>{
      const ans = ansOf(q);
      h += `<div class="ps-q"><p class="ps-no"><b>${i+1}.</b>［${TY[q.ty].name} · ${ptsOf(q)}分］${ans?`　答案：<b>${fmtAns(ans)}</b>`:''}${q.kp?`<span class="ps-kp">［考点：${q.kp}］</span>`:''}</p>
        <div class="ps-stem">${q.q}</div>
        ${q.sol?`<div class="sol-box">${q.sol}</div>`:''}</div>`;
    });
  }
  $('#print-sheet').innerHTML = h;
  renderMath($('#print-wrap'));
}
function doPrint(mode){
  if (mode==='answers' && !paper.length) return alert('还没有试卷');
  if (mode==='wrong' && !wrongBook.length) return alert('错题本是空的');
  buildPrintSheet(mode);
  printAfterFonts();
}
$('#btn-export').onclick = ()=>doPrint('blank');
$('#btn-export-ans').onclick = ()=>doPrint('sol');
$('#btn-export-sol').onclick = ()=>doPrint('sol');
$('#btn-export-my') && ($('#btn-export-my').onclick = ()=>doPrint('answers'));
$('#btn-export-my2') && ($('#btn-export-my2').onclick = ()=>doPrint('answers'));
$('#btn-export-wrong') && ($('#btn-export-wrong').onclick = ()=>doPrint('wrong'));
$('#btn-offline') && ($('#btn-offline').onclick = ()=>{
  if (!curRec) return alert('还没有试卷记录');
  if (!window.KBPaper) return alert('离线作答模块未加载');
  KBPaper.openAtt(curRec, ()=>{ renderHistory(); });
});

/* ---------- 题库总览（含自选组卷） ---------- */
const ALL = [];
Object.keys(TY).forEach(ty=>BANK[ty].forEach(q=>ALL.push(Object.assign({ty}, q))));
const BSZ = 30;
let bkTy='', bkCh='', bkSrc='', bkKw='', bkPage=1;
function bkPlain(s){
  return (s||'').replace(/<[^>]+>/g,' ').replace(/\s+/g,'');
}
function bkFiltered(){
  return ALL.filter(q=>
    (!bkTy || q.ty===bkTy) &&
    (!bkCh || q.ch==+bkCh) &&
    (!bkSrc || (q.src||'').includes(bkSrc)) &&
    (!bkKw || bkPlain(q.q).includes(bkKw))
  );
}
function renderBank(){
  const arr = bkFiltered();
  const pages = Math.max(1, Math.ceil(arr.length/BSZ));
  if (bkPage>pages) bkPage = pages;
  const slice = arr.slice((bkPage-1)*BSZ, bkPage*BSZ);
  $('#bank-stat').textContent = `题库共 ${ALL.length} 题 · 当前筛选 ${arr.length} 题 · 已选 ${picks.length} 题`;
  const host = $('#bank-list');
  host.innerHTML = slice.length ? slice.map((q,i)=>{
    const no = (bkPage-1)*BSZ + i + 1;
    let ans = '';
    if (q.ty==='judge') ans = q.ans;
    else if (q.ty==='choice') ans = 'ABCD'[q.ans];
    else if (q.ty==='blank') ans = String(q.ans||'');
    const on = picks.indexOf(q.id)>=0;
    return `<details class="rv-card bk-item${on?' picked':''}" data-id="${q.id}"><summary>
      <label class="bk-ck" title="选中加入自组卷"><input type="checkbox" class="bk-pick" data-id="${q.id}"${on?' checked':''}></label>
      <span class="tychip t-${q.ty}">${TY[q.ty].name}</span>
      <span class="bk-meta">第${q.ch}章 · ${q.kp} · ${q.src}</span></summary>
      <div class="rv-b"><div class="q-stem"><b class="bk-no">${no}.</b>${q.q}</div>
        ${ans?`<p class="cmp">答案：<b>${fmtAns(ans)}</b></p>`:''}
        ${q.sol?`<div class="sol-box">${q.sol}</div>`:''}</div>
    </details>`;
  }).join('') : '<p class="muted">没有符合条件的题目——放宽筛选或换个关键词试试</p>';
  renderMath(host);
  $$('#bank-list .bk-ck').forEach(lb=>{
    lb.addEventListener('click', e=>{ e.preventDefault(); e.stopPropagation(); });
  });
  $$('#bank-list .bk-pick').forEach(cb=>{
    cb.onclick = e=>{ e.preventDefault(); e.stopPropagation(); togglePick(cb.dataset.id); };
  });
  const pager = $('#bank-pager');
  pager.innerHTML = pages>1 ? `
    <button class="chip" id="bk-prev"${bkPage<=1?' disabled':''}>‹ 上一页</button>
    <span class="pg-info">${bkPage} / ${pages}</span>
    <button class="chip" id="bk-next"${bkPage>=pages?' disabled':''}>下一页 ›</button>` : '';
  const prev=$('#bk-prev'), next=$('#bk-next');
  const goListTop = ()=>{
    const el = $('#bank-list');
    if (!el) return;
    const t = el.getBoundingClientRect().top + window.scrollY - 60;
    window.scrollTo({top:Math.max(0,t), behavior:'smooth'});
  };
  if (prev) prev.onclick = ()=>{ bkPage--; renderBank(); goListTop(); };
  if (next) next.onclick = ()=>{ bkPage++; renderBank(); goListTop(); };
  syncPickBar();
}
function togglePick(id){
  const i = picks.indexOf(id);
  if (i>=0) picks.splice(i,1); else picks.push(id);
  const card = document.querySelector('.bk-item[data-id="'+id+'"]');
  if (card) card.classList.toggle('picked', picks.indexOf(id)>=0);
  const cb = document.querySelector('.bk-pick[data-id="'+id+'"]');
  if (cb) cb.checked = picks.indexOf(id)>=0;
  syncPickBar();
  const st = $('#bank-stat');
  if (st) st.textContent = `题库共 ${ALL.length} 题 · 当前筛选 ${bkFiltered().length} 题 · 已选 ${picks.length} 题`;
}
function pickedPts(){
  let t = 0;
  picks.forEach(id=>{ const q = BYID[id]; if (q) t += (pts[q.ty]||0); });
  return Math.round(t*10)/10;
}
function syncPickBar(){
  const bar = $('#pickbar');
  if (!bar) return;
  bar.hidden = !picks.length;
  if (!picks.length) return;
  const n = $('#pick-n'), p = $('#pick-pts');
  if (n) n.textContent = picks.length;
  if (p) p.textContent = pickedPts();
}
(function(){
  const b = $('#pick-build');
  if (b) b.onclick = ()=>{
    if (!picks.length) return;
    const list = picks.map(id=>BYID[id]).filter(Boolean);
    if (!list.length) return alert('选中的题目已不在题库中');
    buildPaper(list);
    showView('quiz');
    history.replaceState(null,'','#quiz');
    askMode();
  };
  const c = $('#pick-clear');
  if (c) c.onclick = ()=>{ picks = []; renderBank(); };
})();
$$('#bty-row .chip').forEach(b=>b.onclick=()=>{
  $$('#bty-row .chip').forEach(x=>x.classList.remove('on'));
  b.classList.add('on'); bkTy=b.dataset.ty; bkPage=1; renderBank();
});
$$('#bch-row .chip').forEach(b=>b.onclick=()=>{
  $$('#bch-row .chip').forEach(x=>x.classList.remove('on'));
  b.classList.add('on'); bkCh=b.dataset.ch; bkPage=1; renderBank();
});
$$('#bsrc-row .chip').forEach(b=>b.onclick=()=>{
  $$('#bsrc-row .chip').forEach(x=>x.classList.remove('on'));
  b.classList.add('on'); bkSrc=b.dataset.src; bkPage=1; renderBank();
});
let kwTimer=null;
$('#bank-kw').addEventListener('input', function(){
  clearTimeout(kwTimer);
  const v = this.value.trim();
  kwTimer=setTimeout(()=>{
    const y = window.scrollY;
    bkKw=v; bkPage=1; renderBank();
    window.scrollTo(0, y);
  }, 300);
});
renderBank();

/* ---------- 题库统计 ---------- */
const statHost = $('#bank-stats');
if (statHost) statHost.innerHTML =
  `全题库 ${BANK_COUNT} 题：` +
  Object.keys(TY).map(ty=>`${TY[ty].name} ${BANK[ty].length}`).join(' · ');

})();
