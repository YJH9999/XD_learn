(function(){
  var $=function(s){return document.querySelector(s)};
  var $$=function(s){return Array.prototype.slice.call(document.querySelectorAll(s))};
  var toc=$('.toc'), side=$('.side'), mask=$('.mask');
  var topBtn=$('#topbtn');
  var input=$('#q'), sres=$('#sres'), srch=$('.srch');
  var contentEl=$('#content');
  var MF=window.CK_MANIFEST||[], HM=window.CK_HEADMAP||{}, TT=window.CK_TITLES||{};
  var cache={}, lastIdx=-1, loadingNext=false;

  /* ---------- KaTeX 公式渲染（内容注入后调用） ---------- */
  function renderMath(root){
    if(!window.renderMathInElement) return;
    try{
      renderMathInElement(root||contentEl,{
        delimiters:[
          {left:'$$',right:'$$',display:true},
          {left:'\\[',right:'\\]',display:true},
          {left:'\\(',right:'\\)',display:false}
        ],
        throwOnError:false,
        strict:false,
        macros:{"\\bm":"\\boldsymbol","\\R":"\\mathbb{R}","\\E":"\\mathbb{E}"}
      });
    }catch(e){/* 渲染失败时保留原始文本 */}
  }
  window.addEventListener('load',function(){ renderMath(contentEl); });

  /* ================================================================
     目录折叠：用户手动展开/折叠的状态存 localStorage，下次打开恢复
     ================================================================ */
  var OKEY='xd-kb-toc-open', tocT=null;
  function saveTocState(){
    clearTimeout(tocT);
    tocT=setTimeout(function(){
      var ids=$$('.node.open').map(function(n){return n.dataset.id})
        .filter(Boolean);
      try{localStorage.setItem(OKEY,JSON.stringify(ids))}catch(e){}
    },300);
  }
  function restoreTocState(){
    var ids=null;
    try{ ids=JSON.parse(localStorage.getItem(OKEY)||'null'); }catch(e){}
    if(!ids || !ids.length){ 
      /* 默认：展开 0 篇与当前进度所在分支 */
      return false;
    }
    $$('.node.open').forEach(function(n){n.classList.remove('open')});
    ids.forEach(function(id){
      var n=toc.querySelector('.node[data-id="'+id+'"]');
      if(n) n.classList.add('open');
    });
    return true;
  }
  new MutationObserver(saveTocState).observe(toc,{
    subtree:true, attributes:true, attributeFilter:['class']});

  function closeAll(){
    $$('.node.open').forEach(function(n){ n.classList.remove('open') });
  }
  function collapseTo(id){
    var keep=[];
    var el=toc.querySelector('.node[data-id="'+id+'"]');
    var p=el;
    while(p && p!==toc){
      if(p.classList && p.classList.contains('node')) keep.push(p);
      p=p.parentElement;
    }
    $$('.node.open').forEach(function(n){
      if(keep.indexOf(n)===-1) n.classList.remove('open');
    });
    if(el && el.querySelector(':scope > .kids')) el.classList.add('open');
    return el;
  }
  function ensureVisible(el){
    var d=el && el.closest ? el.closest('details') : null;
    if(d && !d.open) d.open=true;
  }

  /* ---------- 目录内快速筛选（仅匹配标题） ---------- */
  var tq=$('#tq');
  function filterToc(){
    var q=tq.value.trim().toLowerCase();
    toc.classList.toggle('tf-on',!!q);
    document.querySelector('.tfbox').classList.toggle('has',!!q);
    $$('.node').forEach(function(n){n.classList.remove('tmatch','tanc')});
    if(!q){ restoreTocState(); return; }
    $$('.node').forEach(function(n){
      var a=n.querySelector(':scope > .row > .tx');
      if(a && a.textContent.toLowerCase().indexOf(q)!==-1) n.classList.add('tmatch');
    });
    $$('.node.tmatch').forEach(function(n){
      var p=n.parentElement;
      while(p && p!==toc){
        if(p.classList.contains('node')){ p.classList.add('tanc','open'); }
        p=p.parentElement;
      }
    });
  }
  tq.addEventListener('input',filterToc);
  $('#tclr').addEventListener('click',function(){
    tq.value=''; filterToc(); tq.focus();
  });

  /* ================================================================
     我的收藏：标题旁星标 + 侧栏面板
     ================================================================ */
  var VKEY='xd-kb-favs';
  var favbtn=$('#favbtn'), favcount=$('#favcount'),
      favpanel=$('#favpanel'), favlist=$('#favlist');
  function getFavs(){try{return JSON.parse(localStorage.getItem(VKEY)||'[]')}catch(e){return[]}}
  function setFavs(a){try{localStorage.setItem(VKEY,JSON.stringify(a))}catch(e){}}
  function toggleFav(id){
    var f=getFavs(), i=f.indexOf(id);
    if(i>=0) f.splice(i,1); else f.unshift(id);
    setFavs(f); syncFavUI();
  }
  function syncFavUI(){
    var f=getFavs();
    $$('.fav').forEach(function(b){b.classList.toggle('on',f.indexOf(b.dataset.fav)>=0)});
    favcount.textContent=f.length;
    favcount.classList.toggle('has',f.length>0);
  }
  function renderFavPanel(){
    var f=getFavs();
    if(!f.length){
      favlist.innerHTML='<div class="fp-none">还没有收藏。<br>点击标题右侧的 ★ 即可收藏薄弱知识点。</div>';
      return;
    }
    favlist.innerHTML=f.map(function(id){
      return '<a class="fv" data-id="'+id+'" href="#'+id+'">'
        +'<svg width="10" height="10" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.8l2.8 5.9 6.4.8-4.7 4.4 1.2 6.3-5.7-3.1-5.7 3.1 1.2-6.3L2.8 9.5l6.4-.8z"/></svg>'
        +(TT[id]||id)+'</a>';
    }).join('');
  }
  favbtn.addEventListener('click',function(){
    var on=side.classList.toggle('favmode');
    favbtn.classList.toggle('on',on);
    if(on) renderFavPanel();
  });
  $('#favclear').addEventListener('click',function(){ setFavs([]); syncFavUI(); renderFavPanel(); });
  favlist.addEventListener('click',function(e){
    var a=e.target.closest('.fv'); if(!a) return;
    e.preventDefault(); go(a.dataset.id);
  });

  /* ================================================================
     分章内容加载（懒加载 + 向下续载 + 跳转时补齐之前所有分块）
     ================================================================ */
  var VER='20261109c';
  function furl(i){ return 'assets/content/' + MF[i].f + '?v=' + VER; }
  function fetchChunk(i, cb){
    if(cache[i]!==undefined){ cb(cache[i]); return; }
    fetch(furl(i)).then(function(r){
      if(!r.ok) throw new Error(r.status);
      return r.text();
    }).then(function(t){ cache[i]=t; cb(t); })
      .catch(function(){
        contentEl.insertAdjacentHTML('beforeend',
          '<div class="callout c-error" style="margin:30px 0"><b>内容加载失败</b>'
          +'：本站正文按章节分文件加载，需通过 HTTP 访问（GitHub Pages、线上地址，'
          +'或本地运行 <code>python -m http.server</code>）；直接双击 index.html 无法加载。</div>');
      });
  }
  function rebindHeads(){
    heads=$$('.main h1,.main h2,.main h3,.main h4');
  }
  function afterInject(anchor, terms){
    rebindHeads();
    renderMath(contentEl);
    rebuildOutline();
    syncFavUI();
    if(anchor){
      var el=document.getElementById(anchor);
      if(el){ ensureVisible(el); el.scrollIntoView({block:'start'}); }
      else window.scrollTo(0,0);
      if(terms) markScope(el, terms);
    }
    applyFocus();
    maybeAppend();
  }
  /* 并行加载 0..k 中缺失的分块，然后按序挂载——保证跳转目标之前的内容全部就位 */
  function ensureUpTo(k, anchor, terms){
    var missing=[];
    for(var i=0;i<=k;i++) if(cache[i]===undefined) missing.push(i);
    if(!missing.length) return mount(k, anchor, terms);
    var done=0;
    missing.forEach(function(i){
      fetchChunk(i, function(){
        if(++done===missing.length) mount(k, anchor, terms);
      });
    });
  }
  function mount(k, anchor, terms){
    var html='';
    for(var i=0;i<=k;i++) html+=cache[i];
    contentEl.innerHTML=html;
    lastIdx=k;
    afterInject(anchor, terms);
  }
  function appendNext(){
    if(loadingNext || lastIdx+1 >= MF.length) return;
    loadingNext = true;
    var i = lastIdx+1;
    fetchChunk(i, function(t){
      loadingNext = false;
      if(i === lastIdx+1){
        contentEl.insertAdjacentHTML('beforeend', t);
        lastIdx = i;
        rebindHeads(); renderMath(contentEl); rebuildOutline(); syncFavUI(); applyFocus();
        onScroll();
      }
    });
  }
  function maybeAppend(){
    var doc=document.documentElement;
    if(doc.scrollHeight - window.innerHeight - window.scrollY < 900) appendNext();
  }

  /* ---------- 跳转（目录 / 搜索 / 大纲 / 收藏共用） ---------- */
  function go(id, terms){
    if(HM[id]===undefined) return;
    collapseTo(id);
    setCur(id);
    var el=document.getElementById(id);
    if(el){
      ensureVisible(el); el.scrollIntoView({block:'start'});
      if(terms){ clearKw(); markScope(el, terms); }
    }
    else ensureUpTo(HM[id], id, terms);
    savePos(id);
    if(window.innerWidth<=1024) closeDrawer();
  }

  toc.addEventListener('click',function(e){
    var tw=e.target.closest('.tw');
    if(tw && !tw.classList.contains('sp')){
      tw.closest('.node').classList.toggle('open');
      e.preventDefault();
      return;
    }
    var a=e.target.closest('a.tx');
    if(a){
      e.preventDefault();
      var node=a.closest('.node');
      if(node && node.querySelector(':scope > .kids')){
        if(node.classList.contains('open')){
          node.classList.remove('open');
        }else{
          node.classList.add('open');
          [].forEach.call(node.querySelectorAll('.node'),function(d){
            d.classList.add('open');
          });
        }
        return;
      }
      go(a.getAttribute('href').slice(1));
    }
  });

  /* ---------- 当前项高亮（滚动联动，同步目录与右栏大纲） ---------- */
  var heads=[], curId=null;
  function setCur(id){
    if(id===curId) return;
    curId=id;
    $$('.node.cur, .node.canc').forEach(function(n){n.classList.remove('cur','canc')});
    var n=toc.querySelector('.node[data-id="'+id+'"]');
    if(n){
      var p=n.parentElement;
      while(p && p!==toc){
        if(p.classList && p.classList.contains('node')) p.classList.add('open','canc');
        p=p.parentElement;
      }
      n.classList.add('cur');
      var row=n.querySelector('.row');
      if(row){
        var tr=row.getBoundingClientRect(), sr=toc.getBoundingClientRect();
        if(tr.top<sr.top+10||tr.bottom>sr.bottom-10)
          toc.scrollTop+=tr.top-sr.top-toc.clientHeight/2;
      }
    }
    $$('.ol.cur').forEach(function(a){a.classList.remove('cur')});
    var oa=$('#ollist .ol[data-id="'+id+'"]');
    if(oa){
      oa.classList.add('cur');
      var or=oa.getBoundingClientRect(), osr=$('#ollist').getBoundingClientRect();
      if(or.top<osr.top||or.bottom>osr.bottom)
        oa.scrollIntoView({block:'nearest'});
    }
  }

  function onScroll(){
    var st=window.scrollY;
    topBtn.classList.toggle('on',st>500);
    var y=st+130, best=null;
    for(var i=0;i<heads.length;i++){
      if(heads[i].offsetTop<=y) best=heads[i]; else break;
    }
    if(best) setCur(best.id);
    maybeAppend();
  }

  topBtn.addEventListener('click',goTop);
  function goTop(){
    window.scrollTo(0,0);
    if(lastIdx!==0) ensureUpTo(0,null);
    savePos('');
  }

  /* ---------- 右栏大纲（当前已加载内容的 H2/H3） ---------- */
  function rebuildOutline(){
    var box=$('#ollist'); if(!box) return;
    box.innerHTML=heads
      .filter(function(h){return h.tagName==='H2'||h.tagName==='H3'})
      .map(function(h){
        return '<a class="ol'+(h.tagName==='H3'?' lv3':'')+'" data-id="'+h.id+'" href="#'+h.id+'">'
          +h.textContent.replace(/^[\s\u200b]+/,'')+'</a>';
      }).join('') || '<div class="ol-none">加载章节后显示大纲</div>';
  }
  document.addEventListener('click',function(e){
    var ol=e.target.closest('.ol');
    if(ol){ e.preventDefault(); go(ol.dataset.id); }
  });

  /* ---------- 考点筛选（冲刺模式 · 以小知识块为单位） ---------- */
  var FKEY='xd-kb-focus';
  var FOCUS={def:false,err:false,hot:false,ex:false};
  var FTAG={def:['只看定义','tg-def'],err:['只看易错点','tg-err'],
            hot:['只看高频考点','tg-hot'],ex:['只看例题','tg-ex']};
  var HLVL={H1:1,H2:2,H3:3,H4:4};
  var fbPop=$('#fb-pop'), fbBtn=$('#fb-open'), focusBar=$('#focusbar');
  function focusAny(){
    return FOCUS.def||FOCUS.err||FOCUS.hot||FOCUS.ex;
  }
  function kindOf(el){
    if(FOCUS.def && el.querySelector('.rkchip.rk-def')) return true;
    if(FOCUS.err && el.querySelector('.rkchip.rk-error,.callout.c-error,.badge.b-error')) return true;
    if(FOCUS.hot && el.querySelector('.rkchip.rk-hot,.callout.c-hot,.badge.b-hot')) return true;
    if(FOCUS.ex && (el.classList.contains('ex')||el.querySelector('.ex'))) return true;
    return false;
  }
  function applyFocus(){
    var any=focusAny();
    document.body.classList.toggle('focus-on',any);
    var n=0; for(var k in FOCUS) if(FOCUS[k]) n++;
    $$('#fbar .fk').forEach(function(b){ b.classList.toggle('on',!!FOCUS[b.dataset.k]); });
    var fbarEl=document.getElementById('fbar');
    if(fbarEl){
      fbarEl.classList.toggle('has',n>0);
      fbarEl.classList.toggle('on',n>0);
      var badge=document.getElementById('fb-badge');
      if(badge) badge.textContent=n||'';
    }
    /* 状态条 */
    if(focusBar){
      focusBar.hidden=!any;
      var tags=document.getElementById('focus-tags');
      if(tags) tags.innerHTML=Object.keys(FTAG)
        .filter(function(k){return FOCUS[k]})
        .map(function(k){return '<b class="'+FTAG[k][1]+'">'+FTAG[k][0]+'</b>'}).join('');
    }
    /* 退出键等：选择了类型才出现 */
    var exitBtn=document.getElementById('fb-exit');
    var tipEl=fbPop ? fbPop.querySelector('.fb-tip') : null;
    if(exitBtn) exitBtn.style.display=any?'':'none';
    if(tipEl) tipEl.textContent=any?'Esc 也可退出':'点选上方类型进入冲刺';
    $$('#content>.nf').forEach(function(el){el.classList.remove('nf')});
    if(!any) return;
    /* 分块规则：
       - h3/h4 标题 = 一个小知识块的起点：命中则保留「标题 + 直到下一个同级/更高级标题」的整块；
         未命中则整块隐藏
       - h1/h2 章标题始终保留，作为结构导航
       - 其余独立块（callout / .ex / .fml / 表格等）逐一判定 */
    var kids=contentEl.children, i=0;
    while(i<kids.length){
      var el=kids[i], tag=el.tagName;
      if(tag==='H3'||tag==='H4'){
        var L=HLVL[tag], j=i+1;
        while(j<kids.length){
          var tj=kids[j].tagName;
          if(HLVL[tj] && HLVL[tj]<=L) break;
          j++;
        }
        if(!kindOf(el)) for(var k2=i;k2<j;k2++) kids[k2].classList.add('nf');
        i=j;
      }else if(tag==='H1'||tag==='H2'){
        i++;
      }else{
        if(!kindOf(el)) el.classList.add('nf');
        i++;
      }
    }
  }
  function exitFocus(){
    for(var k in FOCUS) FOCUS[k]=false;
    try{localStorage.setItem(FKEY,JSON.stringify(FOCUS))}catch(e){}
    applyFocus();
  }
  $$('#fbar .fk').forEach(function(b){
    b.addEventListener('click',function(){
      FOCUS[b.dataset.k]=!FOCUS[b.dataset.k];
      try{localStorage.setItem(FKEY,JSON.stringify(FOCUS))}catch(e){}
      applyFocus();
    });
  });
  fbBtn.addEventListener('click',function(){
    fbPop.hidden=!fbPop.hidden;
  });
  document.addEventListener('click',function(e){
    if(!e.target.closest('#fbar') && fbPop && !fbPop.hidden) fbPop.hidden=true;
  });
  $('#fb-exit').addEventListener('click',function(){ exitFocus(); fbPop.hidden=true; });
  /* 状态条点击 = 重新打开冲刺面板（换类型 / 取消勾选即可退出） */
  if(focusBar){
    focusBar.addEventListener('click',function(e){
      e.stopPropagation();
      fbPop.hidden=false;
    });
  }
  document.addEventListener('keydown',function(e){
    if(e.key==='Escape' && focusAny() && fbPop.hidden) exitFocus();
  });
  (function(){
    var s=null;
    try{s=JSON.parse(localStorage.getItem(FKEY)||'null')}catch(e){}
    if(Array.isArray(s)&&s.length===4){
      FOCUS.def=!!s[2]; FOCUS.err=!!s[0]; FOCUS.hot=!!s[1]; FOCUS.ex=!!s[3];
    }else if(s&&typeof s==='object'){
      for(var k in FOCUS) FOCUS[k]=!!s[k];
    }
    applyFocus();
  })();

  /* ---------- 阅读进度：localStorage 保存当前锚点 ---------- */
  var RKEY='xd-kb-progress', saveT=null;
  function savePos(id){
    try{ localStorage.setItem(RKEY,id||''); }catch(e){}
  }
  window.addEventListener('scroll',function(){
    if(saveT) return;
    saveT=setTimeout(function(){
      saveT=null;
      if(curId) savePos(curId);
    },250);
  },{passive:true});

  /* ---------- 搜索（索引懒加载） ---------- */
  var sReady=false, pendQ=null, sel=-1, results=[], lastTerms=[];
  function ensureSearch(cb){
    if(sReady){ cb(); return; }
    if(pendQ){ pendQ.push(cb); return; }
    pendQ=[cb];
    var s=document.createElement('script');
    s.src='assets/search-index.js?v=20261109c';
    s.onload=function(){ sReady=true; var qs=pendQ; pendQ=null; qs.forEach(function(f){f()}); };
    s.onerror=function(){ pendQ=null;
      sres.innerHTML='<div class="none">搜索索引加载失败</div>'; sres.classList.add('on'); };
    document.head.appendChild(s);
  }
  function esc(s){return s.replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function hl(s,terms){
    var e=esc(s), re=new RegExp('('+terms.map(function(t){return t.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')}).join('|')+')','gi');
    return e.replace(re,'<mark>$1</mark>');
  }
  function doSearch(){
    var q=input.value.trim().toLowerCase();
    srch.classList.toggle('has',!!q);
    if(!q){
      sres.classList.remove('on'); toc.classList.remove('filtering');
      $$('.node').forEach(function(n){n.classList.remove('match')});
      return;
    }
    ensureSearch(function(){ runSearch(q); });
  }
  function runSearch(q){
    var terms=q.split(/\s+/).filter(Boolean);
    lastTerms=terms;
    var IDX=window.CK_SEARCH||[];
    results=IDX.filter(function(x){
      var t=x.t.toLowerCase();
      return terms.every(function(w){return t.indexOf(w)!==-1 || (x.s||'').toLowerCase().indexOf(w)!==-1;});
    }).slice(0,40);
    toc.classList.add('filtering');
    $$('.node').forEach(function(n){n.classList.remove('match','anc')});
    var firstMatch=null;
    results.forEach(function(r){
      var n=toc.querySelector('.node[data-id="'+r.id+'"]');
      if(n){
        n.classList.add('match');
        if(!firstMatch) firstMatch=n;
        var p=n.parentElement;
        while(p && p!==toc){
          if(p.classList.contains('node')){
            p.classList.add('anc'); p.classList.add('open');
          }
          p=p.parentElement;
        }
      }
    });
    if(firstMatch){
      var fr=firstMatch.getBoundingClientRect(), sr=toc.getBoundingClientRect();
      if(fr.top<sr.top||fr.bottom>sr.bottom)
        toc.scrollTop+=fr.top-sr.top-toc.clientHeight/2;
    }
    if(!results.length){
      sres.innerHTML='<div class="none">没有匹配的内容</div>';
    }else{
      sres.innerHTML=results.map(function(r,i){
        return '<a class="r" data-i="'+i+'" href="#'+r.id+'">'
          +'<span class="rt"><span class="lv">H'+r.lv+'</span>'+hl(r.t,terms)+'</span>'
          +'<span class="rs">'+hl(r.s||'',terms)+'</span></a>';
      }).join('');
    }
    sres.classList.add('on'); sel=-1;
  }

  var tmr;
  input.addEventListener('input',function(){ clearTimeout(tmr); tmr=setTimeout(doSearch,110); });
  input.addEventListener('focus',function(){ if(input.value.trim()) doSearch(); });
  $('.srch .clr').addEventListener('click',function(){
    input.value=''; doSearch(); input.focus();
  });
  document.addEventListener('click',function(e){
    if(!e.target.closest('.srch')) sres.classList.remove('on');
  });
  sres.addEventListener('click',function(e){
    var a=e.target.closest('.r'); if(!a) return;
    e.preventDefault();
    var r=results[+a.dataset.i];
    sres.classList.remove('on');
    go(r.id, lastTerms);
  });
  document.addEventListener('keydown',function(e){
    if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k'){e.preventDefault();input.focus();input.select();}
    if(e.key==='Escape'){ if(sres.classList.contains('on')) sres.classList.remove('on'); else {input.value='';doSearch();input.blur();} }
    if(sres.classList.contains('on')&&results.length){
      if(e.key==='ArrowDown'||e.key==='ArrowUp'){
        e.preventDefault();
        sel=(sel+(e.key==='ArrowDown'?1:-1)+results.length)%results.length;
        $$('.sres .r').forEach(function(x,i){x.classList.toggle('sel',i===sel)});
        var el=$$('.sres .r')[sel]; if(el) el.scrollIntoView({block:'nearest'});
      }
      if(e.key==='Enter'&&sel>=0){
        e.preventDefault();
        var r=results[sel];
        sres.classList.remove('on');
        go(r.id, lastTerms);
      }
    }
  });

  /* ---------- 跳转后关键词标黄（搜索触发时） ---------- */
  function clearKw(){
    $$('#content mark.kw').forEach(function(m){
      var p=m.parentNode;
      while(m.firstChild) p.insertBefore(m.firstChild,m);
      p.removeChild(m); p.normalize();
    });
  }
  function markScope(el,terms){
    clearKw();
    if(!el||!terms||!terms.length) return;
    lastTerms=terms;
    var test=new RegExp(terms.map(function(t){return t.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')}).join('|'),'i');
    var gre=new RegExp('('+terms.map(function(t){return t.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')}).join('|')+')','gi');
    var node=el;
    while(node){
      if(node!==el && /^H[1-4]$/.test(node.tagName)) break;
      markWithin(node);
      node=node.nextElementSibling;
    }
    function markWithin(root){
      var w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT,{acceptNode:function(t){
        if(!t.nodeValue.trim()) return 2;
        if(t.parentNode && (t.parentNode.nodeName==='MARK'||t.parentNode.nodeName==='SCRIPT'||t.parentNode.nodeName==='STYLE')) return 2;
        if(t.parentNode && t.parentNode.closest && t.parentNode.closest('pre,code,mark,.katex')) return 2;
        return test.test(t.nodeValue)?1:2;
      }});
      var nodes=[], n;
      while((n=w.nextNode())) nodes.push(n);
      nodes.forEach(function(t){
        var s=t.nodeValue, frag=document.createDocumentFragment(), last=0, m;
        gre.lastIndex=0;
        while((m=gre.exec(s))){
          if(m.index>last) frag.appendChild(document.createTextNode(s.slice(last,m.index)));
          var mk=document.createElement('mark'); mk.className='kw';
          mk.textContent=m[0]; frag.appendChild(mk);
          last=m.index+m[0].length;
        }
        if(last<s.length) frag.appendChild(document.createTextNode(s.slice(last)));
        t.parentNode.replaceChild(frag,t);
      });
    }
  }

  /* ---------- 主题（默认浅色，body.dark 深色） ---------- */
  var mL=$('#m-light'), mD=$('#m-dark');
  function applyTheme(t){
    document.body.classList.toggle('dark',t==='dark');
    mL.classList.toggle('on',t==='light');
    mD.classList.toggle('on',t==='dark');
    try{localStorage.setItem('xd-kb-theme',t)}catch(e){}
  }
  var saved=(function(){try{return localStorage.getItem('xd-kb-theme')}catch(e){return null}})();
  if(saved!=='light' && saved!=='dark'){
    saved=(window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)?'dark':'light';
  }
  applyTheme(saved);
  mL.addEventListener('click',function(){ applyTheme('light'); });
  mD.addEventListener('click',function(){ applyTheme('dark'); });

  /* ---------- 展开/收起全部 ---------- */
  var exp=$('#expall2');
  exp.addEventListener('click',function(){
    var anyClosed=!!toc.querySelector('.node:not(.open) .kids');
    if(anyClosed){ $$('.node').forEach(function(n){n.classList.add('open')}); exp.textContent='全部收起'; }
    else { closeAll(); exp.textContent='展开全部'; }
  });

  /* ---------- 移动端：抽屉 + 底部工具栏 + 右滑关闭 ---------- */
  function openDrawer(){
    side.classList.add('open'); mask.classList.add('on');
    document.body.classList.add('drawer-open');
  }
  function closeDrawer(){
    side.classList.remove('open'); mask.classList.remove('on');
    document.body.classList.remove('drawer-open');
  }
  function toggleDrawer(){
    if(side.classList.contains('open')) closeDrawer(); else openDrawer();
  }
  $('#mob').addEventListener('click',toggleDrawer);
  mask.addEventListener('click',closeDrawer);
  $('#mb-toc').addEventListener('click',toggleDrawer);
  $('#mb-q').addEventListener('click',function(){
    window.scrollTo({top:0,behavior:'smooth'});
    setTimeout(function(){ input.focus(); },80);
  });
  $('#mb-top').addEventListener('click',goTop);
  $('#mb-sprint') && $('#mb-sprint').addEventListener('click',function(){
    fbPop.hidden=false;
  });
  (function(){
    var x0=null,y0=null;
    side.addEventListener('touchstart',function(e){
      x0=e.touches[0].clientX; y0=e.touches[0].clientY;
    },{passive:true});
    side.addEventListener('touchmove',function(e){
      if(x0===null) return;
      var dx=e.touches[0].clientX-x0, dy=e.touches[0].clientY-y0;
      if(dx>64 && Math.abs(dx)>Math.abs(dy)*1.4){
        closeDrawer();
        x0=null;
      }
    },{passive:true});
    side.addEventListener('touchend',function(){ x0=null; },{passive:true});
  })();

  /* ---------- 例题解答：details 折叠初始态 ---------- */
  /* 无需 JS：HTML 直接用 <details>；跳转时 ensureVisible 自动展开 */

  /* ---------- 启动：先恢复目录/进度，再挂滚动监听 ---------- */
  (function boot(){
    restoreTocState();
    syncFavUI();
    var target=null;
    if(location.hash.length>1){
      try{ target=decodeURIComponent(location.hash.slice(1)); }catch(e){ target=null; }
    }
    if(!target){
      try{ target=localStorage.getItem(RKEY)||''; }catch(e){ target=''; }
    }
    if(target && HM[target]!==undefined){
      go(target);
    }else{
      ensureUpTo(target&&HM[target]!==undefined?HM[target]:0,null);
    }
  })();
  window.addEventListener('scroll',onScroll,{passive:true});
})();
