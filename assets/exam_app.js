(function(){
  var $=function(s){return document.querySelector(s)};
  var $$=function(s){return Array.prototype.slice.call(document.querySelectorAll(s))};
  var REVIEW=window.XD_REVIEW||[], BANK=window.XD_BANK||[];
  var WKEY='xd-exam-wrong', wrong=[];
  try{ wrong=JSON.parse(localStorage.getItem(WKEY)||'[]'); }catch(e){}

  /* ---------- 主题（与知识库共用键） ---------- */
  var mL=$('#m-light'), mD=$('#m-dark');
  function applyTheme(t){
    document.body.classList.toggle('dark',t==='dark');
    mL.classList.toggle('on',t==='light');
    mD.classList.toggle('on',t==='dark');
    try{localStorage.setItem('xd-kb-theme',t)}catch(e){}
  }
  var saved=(function(){try{return localStorage.getItem('xd-kb-theme')}catch(e){return null}})();
  if(saved!=='light'&&saved!=='dark') saved='light';
  applyTheme(saved);
  mL.addEventListener('click',function(){applyTheme('light');renderMath()});
  mD.addEventListener('click',function(){applyTheme('dark');renderMath()});

  /* ---------- KaTeX ---------- */
  function renderMath(root){
    if(!window.renderMathInElement) return;
    try{
      renderMathInElement(root||document.body,{
        delimiters:[{left:'$$',right:'$$',display:true},{left:'\\(',right:'\\)',display:false}],
        throwOnError:false,strict:false,macros:{"\\R":"\\mathbb{R}","\\E":"\\mathbb{E}"}
      });
    }catch(e){}
  }
  window.addEventListener('load',function(){renderMath()});

  /* ---------- 视图切换 ---------- */
  $$('.tab').forEach(function(b){
    b.addEventListener('click',function(){
      $$('.tab').forEach(function(x){x.classList.remove('on')});
      b.classList.add('on');
      $$('.view').forEach(function(v){v.classList.remove('on')});
      $('#view-'+b.dataset.view).classList.add('on');
    });
  });

  /* ---------- 考点速览渲染 ---------- */
  function renderReview(){
    $('#review-list').innerHTML=REVIEW.map(function(ch,i){
      return '<div class="rcard'+(i===0?' open':'')+'"><h3>'+ch.ch+'</h3><div class="rb">'
        +ch.points.map(function(p){
          return '<div class="rpoint"><b>'+p.t+'</b><p>'+p.d+'</p></div>';
        }).join('')+'</div></div>';
    }).join('');
    $$('.rcard h3').forEach(function(h){
      h.addEventListener('click',function(){h.parentElement.classList.toggle('open')});
    });
    renderMath();
  }

  /* ---------- 题库统计 ---------- */
  function renderStats(){
    var by={'ch1':0,'ch2':0,'ch3':0,'ch4':0};
    BANK.forEach(function(q){by[q.ch]++});
    $('#bank-stats').innerHTML=
      '<div class="stat"><b>'+BANK.length+'</b>题库总数</div>'
      +'<div class="stat"><b>'+by.ch1+'</b>第 1 章</div>'
      +'<div class="stat"><b>'+by.ch2+'</b>第 2 章</div>'
      +'<div class="stat"><b>'+by.ch3+'</b>第 3 章</div>'
      +'<div class="stat"><b>'+by.ch4+'</b>第 4 章</div>';
  }

  /* ---------- 错题本 ---------- */
  function saveWrong(){try{localStorage.setItem(WKEY,JSON.stringify(wrong))}catch(e){}}
  function addWrong(id){if(wrong.indexOf(id)<0){wrong.push(id);saveWrong();renderWrongList();}}
  function delWrong(id){var i=wrong.indexOf(id);if(i>=0){wrong.splice(i,1);saveWrong();renderWrongList();}}
  function renderWrongList(){
    $('#wrong-count').textContent='（'+wrong.length+' 题）';
    var box=$('#wrong-list');
    if(!wrong.length){box.innerHTML='<div class="wrong-item">暂无错题，保持手感！</div>';return;}
    box.innerHTML=wrong.map(function(id){
      var q=BANK.find(function(x){return x.id===id});
      if(!q) return '';
      var stem=q.stem.replace(/\\\\/g,'\\');
      return '<div class="wrong-item"><b>'+stem.slice(0,60)+'…</b>'
        +'<span class="btnrow" style="margin:0"><button class="btn ghost" data-del="'+q.id+'">移除</button></span></div>';
    }).join('');
    $$('#wrong-list [data-del]').forEach(function(b){
      b.addEventListener('click',function(){delWrong(b.dataset.del)});
    });
    renderMath(box);
  }

  /* ---------- 随机组卷 ---------- */
  function shuffle(a){for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));
    var t=a[i];a[i]=a[j];a[j]=t;}return a;}
  var quiz=[], cur=0, answers=[], qs=$('#quiz-run'), qres=$('#quiz-result'), qsu=$('#quiz-setup');

  function startQuiz(list){
    quiz=list.slice(); cur=0; answers=[];
    qsu.hidden=true; qres.hidden=true; qs.hidden=false;
    showQ();
  }
  function showQ(){
    var q=quiz[cur];
    $('#run-progress').textContent=(cur+1)+' / '+quiz.length;
    $('#bar-fill').style.width=(cur/quiz.length*100)+'%';
    $('#q-panel').innerHTML=
      '<div class="qstem"><b>Q'+(cur+1)+'</b>　'+q.stem+'</div>'
      +q.options.map(function(o,i){
        return '<div class="opt" data-i="'+i+'"><span class="ab">'+'ABCD'[i]+'</span><span>'+o+'</span></div>';
      }).join('')
      +'<div class="qexp" id="qexp"><span class="tag">解析　</span>'+q.explanation
      +'<div style="margin-top:6px;color:var(--ink3);font-size:12px">来源：'+q.src+'</div></div>';
    $$('#q-panel .opt').forEach(function(o){
      o.addEventListener('click',function(){pick(+o.dataset.i)});
    });
    $('#btn-next').textContent=cur===quiz.length-1?'提交判分':'下一题';
    renderMath($('#q-panel'));
  }
  var picked=-1;
  function pick(i){
    if(picked>=0) return;
    picked=i;
    var q=quiz[cur];
    answers[i]=true;
    $$('#q-panel .opt').forEach(function(o,idx){
      o.classList.add('lock');
      if(idx===q.answer) o.classList.add('right');
      if(idx===i&&i!==q.answer) o.classList.add('wrong');
    });
    if(i!==q.answer) addWrong(q.id); else delWrong(q.id);
    $('#qexp').classList.add('show');
  }
  $('#btn-next').addEventListener('click',function(){
    if(picked<0) return;
    cur++; picked=-1;
    if(cur<quiz.length) showQ(); else showResult();
  });
  function showResult(){
    var right=0;
    BANK.forEach(function(){});
    /* answers 记录：answers[i] 表示第 i 次点击 —— 重建每题是否正确 */
    /* 改为在 pick 时记录对错 */
    qs.hidden=true; qres.hidden=false;
    var html='', ok=0;
    quiz.forEach(function(q,i){
      var hit=resultFlags[i];
      if(hit) ok++;
      html+='<div class="rrow"><span class="'+(hit?'ok':'no')+'">'+(hit?'✔ 正确':'✘ 错误')+'</span>'
        +'　'+q.stem.replace(/<strong>|<\/strong>/g,'')
        +'<div class="ansexp">正确答案：'+'ABCD'[q.answer]+'　'+q.explanation+'</div></div>';
    });
    $('#score-line').textContent='得分 '+ok+' / '+quiz.length;
    var rate=Math.round(ok/quiz.length*100);
    $('#score-sub').textContent=rate===100?'满分！可以进入下一章复习了':
      rate>=80?'不错，重点看看错题解析':rate>=60?'及格线附近，回正文补一下错题对应章节':'建议先回正文过一遍对应章节再练';
    $('#result-list').innerHTML=html;
    renderMath($('#result-list'));
  }
  $('#btn-start').addEventListener('click',function(){
    var n=+$('#in-n').value, ch=$('#in-ch').value;
    var pool=BANK.filter(function(q){return !ch||q.ch===ch});
    startQuiz(shuffle(pool.slice()).slice(0,Math.min(n,pool.length)));
  });
  $('#btn-practice-wrong').addEventListener('click',function(){
    var list=wrong.map(function(id){return BANK.find(function(q){return q.id===id})})
      .filter(Boolean);
    if(!list.length) return;
    startQuiz(shuffle(list));
  });
  $('#btn-clear-wrong').addEventListener('click',function(){
    wrong=[];saveWrong();renderWrongList();
  });
  $('#btn-quit').addEventListener('click',function(){
    qs.hidden=true;qsu.hidden=false;
  });
  $('#btn-again').addEventListener('click',function(){
    qres.hidden=true;qsu.hidden=false;
  });
  $('#btn-home').addEventListener('click',function(){
    qres.hidden=true;qsu.hidden=false;
  });

  /* resultFlags：作答对错记录（在 pick 中写入） */
  var resultFlags=[];
  var _start=startQuiz;
  startQuiz=function(list){resultFlags=[];_start(list)};
  var _pick=pick;
  pick=function(i){_pick(i);resultFlags.push(i===quiz[cur].answer)};

  /* ---------- 启动 ---------- */
  renderReview();
  renderStats();
  renderWrongList();
})();
