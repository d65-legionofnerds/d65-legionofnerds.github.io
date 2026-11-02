# Prototype: add an "Oct 23 draft" tab group to d65_boundaries.html with two lazy iframe tabs onto d65_circles.html.
import sys
src,out=sys.argv[1],sys.argv[2]; s=open(src).read()
def rep(a,b,n=1):
    global s; assert s.count(a)==n,(a[:70],s.count(a)); s=s.replace(a,b)
# tab group, first in the bar
rep('<div class="tg tg-stu"><div class="tgl" aria-hidden="true">By estimated students</div>',
 '<div class="tg tg-o23"><div class="tgl" aria-hidden="true">Oct 23 draft (latest)</div><div class="tgb">\n      <button type="button" role="tab" id="tab-oi-btn" aria-selected="false" aria-controls="tab-oi" aria-label="Oct 23 draft impact analysis">What changes</button>\n      <button type="button" role="tab" id="tab-oc-btn" aria-selected="false" aria-controls="tab-oc" aria-label="Students near each school, circles explorer">School circles</button>\n    </div></div>\n    <div class="tg tg-stu"><div class="tgl" aria-hidden="true">By estimated students</div>')
# panels, after the Kingsley/Rhodes panel opener
rep('<section id="tab-kr" role="tabpanel" aria-labelledby="tab-kr-btn" hidden>',
 '''<section id="tab-oi" role="tabpanel" aria-labelledby="tab-oi-btn" hidden>
  <div class="viewnote vn-o23" role="note"><b>Oct 23, 2026 draft.</b> Walks, hazard crossings, program moves, receiving schools and middle school feeders under the district's latest lines. Every tab on this page uses the same Oct 23 lines. <a href="d65_circles.html#proposed" target="_blank" rel="noopener">Open on its own page</a></div>
  <iframe class="o23frame" id="oiframe" title="Oct 23 draft: what changes" data-src="d65_circles.html#proposed"></iframe>
  </section>
  <section id="tab-oc" role="tabpanel" aria-labelledby="tab-oc-btn" hidden>
  <div class="viewnote vn-o23" role="note"><b>School circles.</b> Draw a circle around each school and count the students who live inside it, with the Oct 23 or today's lines underneath. <a href="d65_circles.html#circles" target="_blank" rel="noopener">Open on its own page</a></div>
  <iframe class="o23frame" id="ocframe" title="School circles explorer" data-src="d65_circles.html#circles"></iframe>
  </section>
  <section id="tab-kr" role="tabpanel" aria-labelledby="tab-kr-btn" hidden>''')
rep('const TABS=["es","mss","el","ms","kids","demo","draw","bus","kr"];','const TABS=["oi","oc","es","mss","el","ms","kids","demo","draw","bus","kr"];')
rep('function showTab(t){if(!TABS.includes(t))t="es";if(t==="kr")krLoad();',
 '''function o23Load(id){const f=$(id);if(f.dataset.on)return;f.dataset.on=1;
  f.addEventListener("load",()=>{let d;try{d=f.contentDocument}catch(e){}if(!d)return;
    const st=d.createElement("style");st.textContent="#vsel{display:none!important}body{padding-top:4px!important;background:transparent!important}";d.head.appendChild(st);
    const th=document.documentElement.getAttribute("data-theme");if(th)d.documentElement.setAttribute("data-theme",th);
    const fit=()=>{f.style.height=d.documentElement.scrollHeight+"px"};fit();try{new ResizeObserver(fit).observe(d.body)}catch(e){}setTimeout(fit,800)});
  f.src=f.dataset.src}
function showTab(t){if(!TABS.includes(t))t="es";if(t==="kr")krLoad();if(t==="oi")o23Load("oiframe");if(t==="oc")o23Load("ocframe");''')
rep('if(location.hash==="#closures")t0="kr";','if(location.hash==="#closures")t0="kr";if(location.hash==="#oct23")t0="oi";if(location.hash==="#circles")t0="oc";')
rep('.tg-area{--gc:var(--area)}.tg-stu{--gc:var(--stu)}','.tg-area{--gc:var(--area)}.tg-stu{--gc:var(--stu)}.tg-o23{--gc:#14212b}.vn-o23{--gc:#14212b}\n.o23frame{display:block;width:100%;border:0;min-height:900px;border-radius:8px}\n.tg{display:flex;flex-direction:column}.tgb{flex:1 1 auto}')
# how-to line
rep('<b>See what the district','<b>See the latest draft:</b> open <b>Oct 23 draft</b> for what the Oct 23 lines change (walks, crossings, programs, receiving schools, middle school feeders) and a circles explorer. <b>See what the district',0) if False else None
open(out,'w').write(s)
