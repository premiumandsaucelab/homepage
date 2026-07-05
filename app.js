/* ============================================================
   pslab 강동·송파 — 교육용 토스 (v1)
   ============================================================ */
'use strict';

const $ = (s, r=document) => r.querySelector(s);
const $$ = (s, r=document) => Array.from(r.querySelectorAll(s));
const el = (t,c,h)=>{const n=document.createElement(t); if(c)n.className=c; if(h!=null)n.innerHTML=h; return n;};
const REGION_LABEL={gangdong:"강동",songpa:"송파"};
const RESERVE="https://script.google.com/macros/s/AKfycbwwUCtVHDbJmhxCk6w9qoKm1ny0ZeItyA_ywS9umickhlVRZS3mY_FzqGzRYLGi67Lx/exec";
const KAKAO="https://open.kakao.com/o/siqpqtli";

/* ---------- 저장소 ---------- */
const KEY="pslab_gdsp_v1";
const DEFAULT={ profile:null, diag:null, roadmap:{}, plans:[], streak:1, lastVisit:null, missionDone:null, points:0 };
let S = load();
function load(){ try{ return Object.assign({}, DEFAULT, JSON.parse(localStorage.getItem(KEY)||"{}")); }catch(e){ return Object.assign({},DEFAULT); } }
function save(){ try{ localStorage.setItem(KEY, JSON.stringify(S)); }catch(e){} }
function todayStr(){ const d=new Date(); return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0"); }

/* ---------- 화면 전환 ---------- */
const TABS=["home","diag","roadmap","planner","more"];
function go(tab){
  $$(".screen").forEach(s=>s.classList.remove("active"));
  const scr=$("#s-"+tab); if(scr)scr.classList.add("active");
  $$(".bottomnav button").forEach(b=>{
    const t=b.dataset.tab;
    b.classList.toggle("on", t===tab || (t==="more" && ["more","school","mentor","academy"].includes(tab)));
  });
  $("#bottomnav").style.display = TABS.includes(tab)||["school","mentor","academy"].includes(tab) ? "flex":"flex";
  $("#scroll").scrollTo({top:0});
  location.hash=tab;
  if(tab==="diag") renderDiag();
  if(tab==="roadmap") renderRoadmap();
  if(tab==="planner") renderPlanner();
  if(tab==="topics") renderTopics();
}
function toast(m){ const t=$("#toast"); t.textContent=m; t.classList.add("show"); clearTimeout(t._t); t._t=setTimeout(()=>t.classList.remove("show"),1700); }

/* ============================================================
   온보딩
   ============================================================ */
let onbStep=0, onbData={name:"",school:"",grade:"",track:""};
function initOnboarding(){
  // 학교 select
  const sel=$("#obSchool");
  sel.innerHTML='<option value="">학교 선택</option>'+SCHOOLS.map(s=>`<option value="${s.id}">${s.name} (${REGION_LABEL[s.region]})</option>`).join('')+'<option value="etc">기타 / 목록에 없음</option>';
  // 학년
  $("#obGrade").innerHTML=["1","2","3"].map(g=>`<button class="ob-o" data-g="${g}" onclick="pickGrade('${g}',this)"><span class="oe">${g==='1'?'🌱':g==='2'?'🚀':'🎯'}</span>${g}학년</button>`).join('')+`<button class="ob-o" data-g="예비" onclick="pickGrade('예비',this)"><span class="oe">✨</span>예비고1</button>`;
  // 계열
  $("#obTrack").innerHTML=TRACKS.map(t=>`<button class="ob-o" data-t="${t.id}" onclick="pickTrack('${t.id}',this)"><span class="oe">${t.emoji}</span>${t.label}</button>`).join('');
  // 이름 입력
  $("#obName").addEventListener("input",e=>{ onbData.name=e.target.value.trim(); $("#obBtn0").disabled=!onbData.name; });
  $("#obSchool").addEventListener("change",e=>{ onbData.school=e.target.value; });
  setOnbStep(0);
}
function setOnbStep(n){ onbStep=n; $$(".ob-step").forEach(s=>s.classList.toggle("active", +s.dataset.step===n)); $("#obProg").style.width=((n+1)/4*100)+"%"; }
function onbNext(){ if(onbStep===1 && !onbData.school){ onbData.school="etc"; } setOnbStep(onbStep+1); }
function pickGrade(g,btn){ onbData.grade=g; $$("#obGrade .ob-o").forEach(b=>b.classList.remove("sel")); btn.classList.add("sel"); $("#obBtn2").disabled=false; }
function pickTrack(t,btn){ onbData.track=t; $$("#obTrack .ob-o").forEach(b=>b.classList.remove("sel")); btn.classList.add("sel"); $("#obBtn3").disabled=false; }
function onbFinish(){
  S.profile={ name:onbData.name||"학생", school:onbData.school||"etc", grade:onbData.grade||"1", track:onbData.track||"이공" };
  save();
  $("#onb").classList.add("hide");
  renderAll();
  toast("환영해요, "+S.profile.name+"님! 🎉");
}
function editProfile(){
  if(S.profile){ onbData={name:S.profile.name,school:S.profile.school,grade:S.profile.grade,track:S.profile.track}; }
  $("#onb").classList.remove("hide");
  $("#obName").value=onbData.name||"";
  $("#obSchool").value=onbData.school||"";
  $("#obBtn0").disabled=!onbData.name;
  $$("#obGrade .ob-o").forEach(b=>b.classList.toggle("sel", b.dataset.g===onbData.grade));
  $$("#obTrack .ob-o").forEach(b=>b.classList.toggle("sel", b.dataset.t===onbData.track));
  $("#obBtn2").disabled=!onbData.grade; $("#obBtn3").disabled=!onbData.track;
  setOnbStep(0);
}
function schoolName(id){ const s=SCHOOLS.find(x=>x.id===id); return s?s.name:"우리 학교"; }
function schoolObj(id){ return SCHOOLS.find(x=>x.id===id)||null; }

/* ============================================================
   홈 대시보드
   ============================================================ */
function bumpStreak(){
  const t=todayStr();
  if(S.lastVisit!==t){
    const y=new Date(Date.now()-864e5); const yStr=y.getFullYear()+"-"+String(y.getMonth()+1).padStart(2,"0")+"-"+String(y.getDate()).padStart(2,"0");
    S.streak = (S.lastVisit===yStr) ? (S.streak||0)+1 : 1;
    S.lastVisit=t; save();
  }
}
function renderHome(){
  const p=S.profile;
  $("#homeHi").innerHTML = `${p.name}님 👋<small>${schoolName(p.school)} · ${p.grade}학년 · ${p.track}</small>`;
  $("#homeStreak").textContent = `🔥 ${S.streak}일`;
  renderAsset();
  renderMission();
  renderFeed();
}
function renderAsset(){
  const box=$("#assetBox");
  if(!S.diag){
    box.innerHTML=`<div class="asset empty">
      <div class="lab">내 생기부 완성도</div>
      <h3>아직 진단 전이에요</h3>
      <p>7개 질문 1분이면, 내 생기부 완성도와<br>지금 뭘 채워야 하는지 알 수 있어요.</p>
      <button class="go" onclick="go('diag')">1분 진단 시작 →</button>
    </div>`;
    return;
  }
  const d=S.diag, cats=Object.keys(DIAG_CAT);
  const deltaHtml = d.prev!=null ? `<span class="delta">${d.total>=d.prev?'▲':'▼'} 지난 진단 대비 ${Math.abs(d.total-d.prev)}점</span>` : `<span class="delta" style="color:var(--ink-3)">첫 진단 완료</span>`;
  box.innerHTML=`<div class="asset tap" onclick="go('diag')">
    <div class="lab">내 생기부 완성도 · ${schoolName(S.profile.school)} ${S.profile.grade}학년</div>
    <div class="big"><span class="num">${d.total}</span><span class="pct">점</span></div>
    ${deltaHtml}
    <div class="bars">${cats.map(c=>`<div class="b"><div class="track"><div class="fill" style="height:${d.cat[c]}%"></div></div><div class="bl">${DIAG_CAT[c].label.replace(/\(.*\)/,'')}</div><div class="bv">${d.cat[c]}</div></div>`).join('')}</div>
    <div class="asset-cta">다시 진단하고 완성도 올리기 →</div>
  </div>`;
}
function renderMission(){
  const done = S.missionDone===todayStr();
  // 오늘의 미션: 날짜 기반 고정 선택
  const idx = (new Date().getDate()) % MISSIONS.length;
  const m = MISSIONS[idx];
  $("#missionCard").innerHTML=`
    <div class="mc">${done?'✅':'🎯'}</div>
    <div class="mt"><div class="k">오늘의 미션</div><div class="v">${m}</div></div>
    <button class="mbtn ${done?'done':''}" onclick="event.stopPropagation();doMission()">${done?'완료!':'완료'}</button>`;
  $("#missionCard").onclick=()=>{};
}
function doMission(){
  if(S.missionDone===todayStr()){ toast("오늘 미션은 이미 완료했어요 😎"); return; }
  S.missionDone=todayStr(); S.points=(S.points||0)+10; save();
  renderMission();
  toast("미션 완료! +10P 🎉");
}
function ddayInfo(dateStr){
  if(!dateStr) return null;
  const t=new Date(todayStr()+"T00:00:00"), d=new Date(dateStr+"T00:00:00");
  const diff=Math.round((d-t)/864e5);
  const label = diff===0?"D-DAY":diff>0?("D-"+diff):("D+"+(-diff));
  const cls = diff<0?"far":diff<=3?"":diff<=7?"soon":"far";
  return {diff,label,cls};
}
function renderFeed(){
  const feed=$("#homeFeed"); feed.innerHTML="";
  const p=S.profile;

  // 1) 임박한 플래너 항목
  const upcoming = (S.plans||[]).map(x=>({...x,dd:ddayInfo(x.date)})).filter(x=>x.dd && x.dd.diff>=0).sort((a,b)=>a.dd.diff-b.dd.diff)[0];
  if(upcoming){
    feed.appendChild(fc("📅","",`가장 가까운 일정`,upcoming.name,`<span class="dday ${upcoming.dd.cls}">${upcoming.dd.label}</span>`,()=>go("planner")));
  } else {
    feed.appendChild(fc("📅","",`이번 주 일정 등록하기`,"수행평가·활동 마감을 놓치지 않게 플래너에 추가해요.","",()=>go("planner")));
  }

  // 2) 진단 유도 or 약점 팁
  if(!S.diag){
    feed.appendChild(fc("🩺","",`생기부 완성도 진단`,"1분이면 내 강점·약점이 한눈에 보여요.","",()=>go("diag")));
  } else {
    const weak = Object.keys(DIAG_CAT).sort((a,b)=>S.diag.cat[a]-S.diag.cat[b])[0];
    feed.appendChild(fc("⚡","",`지금 가장 약한 건 '${DIAG_CAT[weak].label}'`,DIAG_CAT[weak].tip,"",()=>go("diag")));
  }

  // 3) 내 학교 정보
  const sc=schoolObj(p.school);
  if(sc){
    feed.appendChild(fc("",sc.logo,`내 학교 · ${sc.name} 입시 정보`,sc.intro,"",()=>{ go("school"); setTimeout(()=>openSchool(sc.id),120); }));
  } else {
    feed.appendChild(fc("🏫","",`강동·송파 학교 정보`,"우리 지역 학교별 입시 분석을 확인해요.","",()=>go("school")));
  }

  // 4) 맞춤 멘토 (같은 학교 우선 → 같은 계열)
  let mt = MENTORS.find(m=> sc && m.hs && m.hs.includes(sc.name));
  if(!mt) mt = MENTORS.find(m=> m.cat.includes(p.track));
  if(!mt) mt = MENTORS.find(m=>m.cat.includes("대표"));
  if(mt){
    const why = (sc && mt.hs && mt.hs.includes(sc.name)) ? `나랑 같은 ${sc.name} 선배예요` : `${p.track} 계열 선배 추천`;
    feed.appendChild(fc("",mt.uni,`멘토 추천 · ${mt.college}`,why,"",()=>go("mentor")));
  }

  // 5) 탐구주제
  feed.appendChild(fc("💡","",`${p.track} 세특 탐구주제`,"막막할 때 바로 쓰는 탐구 아이디어.","",()=>go("topics")));
}
function fc(emoji,img,title,sub,right,onclick){
  const n=el("div","fc");
  const icon = img ? `<div class="fi" style="background:var(--bg)"><img src="${img}" onerror="this.parentNode.textContent='🏫'"></div>` : `<div class="fi" style="background:var(--accent-tint)">${emoji}</div>`;
  n.innerHTML=`${icon}<div class="fx"><div class="ft">${title}</div><div class="fs">${sub}</div></div>${right?right:'<span class="fgo">›</span>'}`;
  n.onclick=onclick; return n;
}

/* ============================================================
   생기부 자가진단
   ============================================================ */
let diagIdx=0, diagAns={};
function renderDiag(){
  if(S.diag && diagIdx===0 && Object.keys(diagAns).length===0 && !diagResuming){ renderDiagResult(); return; }
  diagIdx=0; diagAns={};
  showDiagQ();
}
let diagResuming=false;
function startDiagFresh(){ diagResuming=true; diagIdx=0; diagAns={}; showDiagQ(); diagResuming=false; }
function showDiagQ(){
  const body=$("#diagBody");
  const q=DIAG_Q[diagIdx];
  const prog=((diagIdx)/(DIAG_Q.length)*100);
  body.innerHTML=`
    <div class="diag-wrap">
      <div class="diag-prog"><div class="pf" style="width:${prog}%"></div></div>
      <div class="diag-step">질문 ${diagIdx+1} / ${DIAG_Q.length}</div>
      <div class="diag-q">${q.q}</div>
      <div class="diag-sub">${q.sub}</div>
      <div class="diag-opts">
        ${q.opts.map((o,i)=>`<button class="opt ${diagAns[q.key]===i?'sel':''}" onclick="answerDiag(${i})"><span>${o.t}</span><span class="rc"></span></button>`).join('')}
      </div>
    </div>`;
}
function answerDiag(i){
  const q=DIAG_Q[diagIdx]; diagAns[q.key]=i;
  $$("#diagBody .opt").forEach((b,bi)=>b.classList.toggle("sel",bi===i));
  setTimeout(()=>{
    if(diagIdx<DIAG_Q.length-1){ diagIdx++; showDiagQ(); }
    else finishDiag();
  },230);
}
function finishDiag(){
  // 카테고리별 평균
  const acc={}, cnt={};
  Object.keys(DIAG_CAT).forEach(c=>{acc[c]=0;cnt[c]=0;});
  DIAG_Q.forEach(q=>{
    const ai=diagAns[q.key]; if(ai==null) return;
    acc[q.cat]+=q.opts[ai].s; cnt[q.cat]++;
  });
  const cat={};
  Object.keys(DIAG_CAT).forEach(c=> cat[c]= cnt[c]? Math.round(acc[c]/cnt[c]) : 50);
  let total=0, wsum=0;
  Object.keys(DIAG_CAT).forEach(c=>{ total+=cat[c]*DIAG_CAT[c].weight; wsum+=DIAG_CAT[c].weight; });
  total=Math.round(total/wsum);
  const prev = S.diag ? S.diag.total : null;
  S.diag={ total, cat, prev, date:todayStr() };
  S.points=(S.points||0)+30; save();
  renderDiagResult(true);
}
function gradeBadge(t){
  if(t>=85) return {t:"최상위권 궤도 🏆",bg:"#E7F5EC",c:"#12B886"};
  if(t>=70) return {t:"안정적인 상위권 💪",bg:"var(--accent-tint)",c:"var(--accent)"};
  if(t>=50) return {t:"성장 중, 지금이 골든타임 🌱",bg:"#FFF3E0",c:"#E8850C"};
  return {t:"지금 시작하면 충분해요 🔥",bg:"#FDECEC",c:"#F04452"};
}
function renderDiagResult(justFinished){
  const d=S.diag; if(!d){ startDiagFresh(); return; }
  const cats=Object.keys(DIAG_CAT);
  const gb=gradeBadge(d.total);
  const R=80, C=2*Math.PI*R, off=C*(1-d.total/100);
  const sorted=cats.slice().sort((a,b)=>d.cat[a]-d.cat[b]);
  const catColor=v=> v>=75?"var(--green)":v>=50?"var(--accent)":v>=35?"var(--amber)":"var(--red)";
  $("#diagBody").innerHTML=`
    <div class="result-score">
      <div class="result-ring">
        <svg width="180" height="180"><circle cx="90" cy="90" r="${R}" fill="none" stroke="var(--line)" stroke-width="14"/>
          <circle cx="90" cy="90" r="${R}" fill="none" stroke="url(#g)" stroke-width="14" stroke-linecap="round" stroke-dasharray="${C}" stroke-dashoffset="${C}" id="ringArc"/>
          <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7C7EE8"/><stop offset="1" stop-color="#5A5CD6"/></linearGradient></defs></svg>
        <div class="rt"><div class="n">${d.total}</div><div class="l">생기부 완성도</div></div>
      </div>
      <div class="grade-badge" style="background:${gb.bg};color:${gb.c}">${gb.t}</div>
    </div>
    <div class="sec-h" style="margin-top:22px">영역별 진단 <span style="font-size:12px;color:var(--ink-3);font-weight:600">약한 순</span></div>
    <div class="cat-list">
      ${sorted.map(c=>`<div class="cat"><div class="ch"><div class="cn">${DIAG_CAT[c].label}</div><div class="cv" style="color:${catColor(d.cat[c])}">${d.cat[c]}점</div></div>
        <div class="cbar"><div class="cf" style="width:${d.cat[c]}%;background:${catColor(d.cat[c])}"></div></div>
        <div class="ctip">💡 ${DIAG_CAT[c].tip}</div></div>`).join('')}
    </div>
    <div class="mx" style="margin-top:8px">
      <div class="card" style="padding:20px;background:linear-gradient(135deg,#5A5CD6,#3D3FB0);color:#fff;text-align:center">
        <div style="font-size:15px;font-weight:800;margin-bottom:6px">이 진단, 현역 선배가 더 깊게 봐줄 수 있어요</div>
        <div style="font-size:12.5px;opacity:.9;margin-bottom:16px;line-height:1.55">완성도 점수 뒤에 숨은 진짜 빈틈까지.<br>${schoolName(S.profile.school)} 출신 선배의 밀착 분석을 받아보세요.</div>
        <a href="${RESERVE}" target="_blank" rel="noopener" style="display:inline-block;background:#fff;color:var(--accent);font-weight:800;font-size:14px;padding:13px 26px;border-radius:13px">무료 사전예약하고 분석받기 →</a>
      </div>
    </div>
    <div style="text-align:center;padding:8px 20px 24px"><button onclick="startDiagFresh()" style="color:var(--ink-3);font-size:13.5px;font-weight:700">다시 진단하기</button></div>`;
  // 링 애니메이션
  requestAnimationFrame(()=>{ const arc=$("#ringArc"); if(arc){ arc.style.transition="stroke-dashoffset 1s cubic-bezier(.2,.8,.2,1)"; arc.style.strokeDashoffset=off; } });
  if(justFinished){ toast("진단 완료! +30P 🎉"); renderAsset(); renderFeed(); }
}

/* ============================================================
   로드맵
   ============================================================ */
let rmGrade=null;
function renderRoadmap(){
  if(!rmGrade){ rmGrade = (S.profile.grade==="예비")?"1":S.profile.grade; }
  $("#rmTabs").innerHTML=["1","2","3"].map(g=>`<button class="${rmGrade===g?'on':''}" onclick="setRmGrade('${g}')">${g}학년</button>`).join('');
  const items=ROADMAP[rmGrade]||[];
  const doneArr=S.roadmap[rmGrade]||[];
  const doneCount=doneArr.filter(Boolean).length;
  const pct=items.length?Math.round(doneCount/items.length*100):0;
  $("#rmProgress").innerHTML=`<div class="progress-pill"><div class="pt"><div class="a">${rmGrade}학년 로드맵 진행률</div><div class="b">${doneCount}/${items.length}</div></div><div class="ptrack"><div class="pfill" style="width:${pct}%"></div></div></div>`;
  $("#rmList").innerHTML=items.map((it,i)=>`<div class="check ${doneArr[i]?'done':''}" onclick="toggleRm(${i})"><div class="box">✓</div><div class="ct">${it}</div></div>`).join('');
}
function setRmGrade(g){ rmGrade=g; renderRoadmap(); }
function toggleRm(i){
  if(!S.roadmap[rmGrade]) S.roadmap[rmGrade]=[];
  S.roadmap[rmGrade][i]=!S.roadmap[rmGrade][i];
  if(S.roadmap[rmGrade][i]){ S.points=(S.points||0)+5; }
  save(); renderRoadmap();
}

/* ============================================================
   플래너
   ============================================================ */
function renderPlanner(){
  const list=$("#plList");
  const items=(S.plans||[]).map((x,idx)=>({...x,idx,dd:ddayInfo(x.date)}))
    .sort((a,b)=>{ if(!a.date)return 1; if(!b.date)return -1; return new Date(a.date)-new Date(b.date); });
  if(!items.length){ list.innerHTML=`<div class="empty-state"><div class="es-ic">📅</div><p>아직 등록한 일정이 없어요.<br>수행평가·대회·활동 마감을 추가해 보세요.</p></div>`; return; }
  list.innerHTML=items.map(x=>{
    const dd=x.dd; const past=dd&&dd.diff<0;
    const ddHtml = dd?`<span class="dday ${dd.cls}">${dd.label}</span>`:"";
    return `<div class="pl-item" style="${past?'opacity:.5':''}"><div class="pd">${ddHtml}</div><div class="px"><div class="pn">${x.name}</div><div class="pdt">${x.date||"날짜 미정"}</div></div><button class="del" onclick="delPlan(${x.idx})">✕</button></div>`;
  }).join('');
}
function addPlan(){
  const name=$("#plName").value.trim(), date=$("#plDate").value;
  if(!name){ toast("일정 이름을 입력해줘"); return; }
  S.plans.push({name,date}); save();
  $("#plName").value=""; $("#plDate").value="";
  renderPlanner(); if($("#s-home").classList.contains("active")) renderFeed();
  toast("일정을 추가했어요 📅");
}
function delPlan(idx){ S.plans.splice(idx,1); save(); renderPlanner(); }

/* ============================================================
   탐구주제
   ============================================================ */
let topicTrack=null;
function renderTopics(){
  if(!topicTrack) topicTrack=S.profile.track;
  $("#topicTrack").innerHTML=TRACKS.map(t=>`<button class="tchip ${topicTrack===t.id?'on':''}" onclick="setTopicTrack('${t.id}')"><span>${t.emoji}</span>${t.label}</button>`).join('');
  const data=TOPICS[topicTrack]||{};
  $("#topicList").innerHTML=Object.keys(data).map(subj=>`
    <div class="subj-group"><div class="sg-h">📗 ${subj}</div>
      ${data[subj].map((t,i)=>`<div class="topic-item"><div class="tn">${i+1}</div><div>${t}</div></div>`).join('')}
    </div>`).join('') + `<div class="mx" style="margin-top:14px"><a href="${RESERVE}" target="_blank" rel="noopener" class="school-cta" style="background:var(--accent)">내 생기부에 맞는 주제, 선배에게 받기 →</a></div>`;
}
function setTopicTrack(t){ topicTrack=t; renderTopics(); }

/* ============================================================
   Reference: 학교 / 멘토 / 플랜 / FAQ
   ============================================================ */
function stars(n){ return '★★★★★☆☆☆☆☆'.slice(5-n,10-n); }
function schoolCard(sc){
  const card=el("div","card school"); card.dataset.id=sc.id;
  const reg=sc.region==='gangdong'?'gd':'sp';
  const logo=sc.logo?`<img src="${sc.logo}" onerror="this.parentNode.textContent=this.parentNode.dataset.n">`:sc.name.slice(0,2);
  card.innerHTML=`<div class="head"><div class="logo" data-n="${sc.name.slice(0,2)}">${logo}</div>
    <div class="h-main"><div class="nm">${sc.name}<span class="reg-badge ${reg}">${REGION_LABEL[sc.region]}</span></div><div class="meta">${sc.type} · ${sc.loc}</div></div><div class="chev">⌄</div></div>
    <div class="body"><div class="body-inner">
      <div class="metric-row"><div class="metric"><div class="mv">${sc.jinhak}</div><div class="ml">4년제 진학률</div></div><div class="metric"><div class="mv stars">${stars(sc.naeshin)}</div><div class="ml">내신 경쟁</div></div><div class="metric"><div class="mv" style="font-size:11.5px">${sc.susi}</div><div class="ml">수시 강점</div></div></div>
      <div class="field"><div class="ft">🎯 한눈에</div><div class="fb">${sc.intro}</div></div>
      <div class="field"><div class="ft">📈 최근 실적</div><div class="fb">${sc.siljeok}</div></div>
      <div class="field"><div class="ft">🧭 핵심 전략</div><div class="fb">${sc.strategy}</div></div>
      <div class="field"><div class="ft">🎓 pslab 멘토</div><div class="fb">${sc.mentorNote}</div></div>
      <div class="tagline">${sc.tags.map(t=>`<span class="tg">${t}</span>`).join('')}</div>
      <a class="school-cta" href="${RESERVE}" target="_blank" rel="noopener">${sc.name} 맞춤 분석 신청 →</a>
    </div></div>`;
  card.querySelector(".head").addEventListener("click",()=>{
    const open=card.classList.contains("open");
    card.parentNode.querySelectorAll(".school.open").forEach(o=>{if(o!==card)o.classList.remove("open");});
    card.classList.toggle("open",!open);
  });
  return card;
}
function openSchool(id){ const c=$(`#schoolList .school[data-id="${id}"]`); if(c){ c.classList.add("open"); c.scrollIntoView({behavior:"smooth",block:"center"}); } }
let schoolFilter="all";
function renderSchool(){
  $("#schoolChips").innerHTML=[["all","전체"],["gangdong","강동"],["songpa","송파"]].map(([v,l])=>`<button class="chip ${schoolFilter===v?'on':''}" onclick="setSchoolFilter('${v}')">${l}</button>`).join('');
  const box=$("#schoolList"); box.innerHTML="";
  SCHOOLS.filter(s=>schoolFilter==="all"||s.region===schoolFilter).forEach(s=>box.appendChild(schoolCard(s)));
}
function setSchoolFilter(v){ schoolFilter=v; renderSchool(); }

function mentorCard(m){
  const c=el("div","card mentor");
  c.innerHTML=`<div class="m-top"><div class="uni"><img src="${m.uni}" onerror="this.style.display='none'"></div>
    <div class="m-name"><div class="cg">${m.college}${m.pass?`<span class="pass-badge">${m.pass}</span>`:''}</div><div class="mj">${m.major||'—'}</div></div>
    <div class="role">${m.role}</div></div>
    ${m.hs?`<div class="hs">📍 ${m.hs}</div>`:''}
    ${m.accepted?`<div class="accepted">${m.accepted}</div>`:''}
    <div class="m-tags">${m.tags.map(t=>`<span class="mt">${t}</span>`).join('')}</div>`;
  return c;
}
const MENTOR_CATS=[["all","전체"],["대표","대표 멘토진"],["의생명","의생명"],["이공","이공"],["상경사회","상경·사회"],["인문교육","인문·교육"],["정시","정시"]];
let mentorFilter="all";
function renderMentor(){
  $("#mentorChips").innerHTML=MENTOR_CATS.map(([v,l])=>`<button class="chip ${mentorFilter===v?'on':''}" onclick="setMentorFilter('${v}')">${l}</button>`).join('');
  const list=MENTORS.filter(m=>mentorFilter==="all"||m.cat.includes(mentorFilter));
  $("#mentorCount").textContent=`총 ${list.length}명의 선배`;
  const box=$("#mentorList"); box.innerHTML=""; list.forEach(m=>box.appendChild(mentorCard(m)));
}
function setMentorFilter(v){ mentorFilter=v; renderMentor(); }

let planTab="susi";
function switchPlan(t){ planTab=t; $("#tgSusi").classList.toggle("on",t==="susi"); $("#tgJeongsi").classList.toggle("on",t==="jeongsi"); renderPlans(); }
function renderPlans(){
  const box=$("#planList"); box.innerHTML="";
  PLANS[planTab].forEach(p=>{
    const c=el("div","card plan"+(p.best?" best":""));
    c.innerHTML=`${p.best?'<span class="best-badge">인기</span>':''}<div class="p-name">${p.name}</div><div class="p-desc">${p.desc}</div>
      <div class="p-price"><span class="amt">${p.amt}</span><span class="unit">${p.unit}</span>${p.launch?'<span class="launch">런칭가</span>':''}</div>
      <ul>${p.feats.map(f=>`<li>${f}</li>`).join('')}</ul>
      <a class="school-cta" href="${RESERVE}" target="_blank" rel="noopener" style="margin-top:16px;background:var(--accent)">이 플랜으로 사전예약 →</a>`;
    box.appendChild(c);
  });
}
function renderFaq(){
  const box=$("#faqList"); box.innerHTML="";
  FAQS.forEach(f=>{ const it=el("div","card faq"); it.innerHTML=`<div class="q"><span class="qmark">Q</span><span class="qt">${f.q}</span><span class="pm">+</span></div><div class="a"><div class="a-in">${f.a}</div></div>`; it.querySelector(".q").onclick=()=>it.classList.toggle("open"); box.appendChild(it); });
}

/* ============================================================
   init
   ============================================================ */
function renderAll(){
  if(S.profile){
    $("#mpName").textContent=`${S.profile.name}님`;
    $("#mpSub").textContent=`${schoolName(S.profile.school)} · ${S.profile.grade}학년 · ${S.profile.track}`;
  }
  renderHome();
  renderSchool(); renderMentor(); renderPlans(); renderFaq();
}
function init(){
  initOnboarding();
  if(!S.profile){ $("#onb").classList.remove("hide"); }
  else { $("#onb").classList.add("hide"); bumpStreak(); renderAll(); }

  const hash=(location.hash||"").replace("#","");
  if(S.profile && ["home","diag","roadmap","planner","topics","more","school","mentor","academy"].includes(hash)) go(hash);

  if("serviceWorker" in navigator && location.protocol.startsWith("http")){ navigator.serviceWorker.register("app.sw.js").catch(()=>{}); }
}
document.addEventListener("DOMContentLoaded", init);
