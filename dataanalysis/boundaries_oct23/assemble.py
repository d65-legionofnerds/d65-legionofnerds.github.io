# Assemble d65_boundaries.html on the Oct 23, 2026 draft: new data blobs, district Oct 28 counts, and matching text.
import sys, json, re
from geo import B, Z, SCH
src = sys.argv[1] if len(sys.argv) > 1 else B + 'orig.html'
out = sys.argv[2] if len(sys.argv) > 2 else B + 'oct23.html'
s = open(src).read()
NEWD = json.load(open(B + 'oct23_data.json')); TL = json.load(open(B + 'tiles_oct23.json'))
CNT = {}
def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (a[:90], c)
    s = s.replace(a, b)

# ---------- 1. data blobs ----------
def swap(name, obj):
    global s
    k = f'const {name}='
    i = s.index(k) + len(k)
    o, e = json.JSONDecoder().raw_decode(s[i:])
    s = s[:i] + json.dumps(obj, separators=(',', ':')) + s[i + e:]
swap('D', NEWD['D']); swap('MS', NEWD['MS']); swap('D2', NEWD['D2'])

# ---------- 2. elementary land tab: Lincolnwood district figures, descriptions ----------
rep('const LWS={total:331,to:{Willard:269,Walker:39,Orrington:23}};', 'const LWS={total:252,to:{Willard:154,Foster:38,Orrington:23}};')
rep('["Willard","Walker","Orrington"].map(k=>', '["Willard","Foster","Orrington"].map(k=>')
rep('<span class="st">${LWS.to[k]} of ${LWS.total} students (Oct 1, 2026 enrollment)</span>',
    '<span class="st">${LWS.to[k]} of ${LWS.total} current K-4 students${k==="Orrington"?" (STEP count covers all grades)":""}. District count, Oct 28, 2026</span>')
rep('Percent at right is share of land area. Student counts are district figures based on Oct 1, 2026 enrollment of ${LWS.total}.',
    'Percent at right is share of land area. Student counts are the district\'s Oct 28, 2026 counts of current K-4 students (${LWS.total} at Lincolnwood on Oct 1); the STEP count covers all grades.')
rep('<b>Students (district figures):</b> Willard ${LWS.to.Willard} (${stuPct("Willard")}%), Walker ${LWS.to.Walker} (${stuPct("Walker")}%), Orrington ${LWS.to.Orrington} (${stuPct("Orrington")}%, STEP program).',
    '<b>Students (district counts, current K-4):</b> Willard ${LWS.to.Willard} (${stuPct("Willard")}%), Foster ${LWS.to.Foster} (${stuPct("Foster")}%), plus ${LWS.to.Orrington} STEP students (all grades) to Orrington with the program.')
i = s.index('const STREETS={'); j = s.index('};', i) + 2
s = s[:i] + '''const STREETS={
 Dewey:{red:"North downtown and south campus: north of a line from about Emerson and Sherman southeast to Church at the lake",teal:"South downtown: east of about Elmwood from Church to Dempster, plus a wedge north of Church below the Orrington line",green:"Church to Dempster, Dodge to about Elmwood, around the Dewey building",maroon:"A small pocket north of Church St, Asbury to about Ridge"},
 Lincolnwood:{purple:"Central St down to about Payne St",maroon:"About Grant St (west of Central Park Ave) and Payne St (east of it) south to Golf Rd and the canal"}};''' + s[j:]
i = s.index('const DESC={'); j = s.index('};', i) + 2
s = s[:i] + '''const DESC={
 Dewey:"Building proposed to close. North downtown and south campus go to Orrington. South downtown, east of about Elmwood, goes to Lincoln. The middle, Church to Dempster from Dodge to about Elmwood, goes to Washington. A small pocket north of Church between Asbury and Ridge goes to Foster. King Arts' neighborhood west of Dodge is King Arts' area on both maps, so it is not counted here.",
 Lincolnwood:"Building proposed to close. Most of the area, Central St down to about Payne St, goes to Willard. The southern strip down to Golf Rd and the canal goes to Foster. STEP students go to Orrington with the program. Nothing goes to Walker on the Oct 23 draft.",
 Washington:"Washington splits about in half. The west side, Dempster to Main from McCormick to Dodge, plus Main to about Monroe from Dodge to Asbury, goes to Dawes. The rest stays at Washington, which picks up the middle of Dewey.",
 Oakton:"Most of Oakton stays. A pocket west of Asbury, about Monroe to South Blvd, goes to Dawes. Oakton picks up Lincoln's strip south of South Blvd.",
 Lincoln:"Most of Lincoln stays and adds south downtown from Dewey. The strip south of South Blvd, Sherman to about Hinman, goes to Oakton.",
 Walker:"No change. Walker gained part of Lincolnwood on the Oct 13 draft; on the Oct 23 draft it gains nothing.",
 Willard:"No change for current Willard families. Willard adds most of Lincolnwood.",
 Foster:"No change for current Foster families. Foster adds Lincolnwood's southern strip and a small pocket of Dewey.",
 Orrington:"No change for current Orrington families. Orrington adds north downtown and south campus from Dewey.",
 Dawes:"No change for current Dawes families. Dawes adds the west half of Washington and a pocket of Oakton."};''' + s[j:]
i = s.index('Object.assign(STREETS,{'); j = s.index('}});', i) + 4
s = s[:i] + '''Object.assign(STREETS,{
 Washington:{blue:"Dempster to Main, McCormick to Dodge, plus Main to about Monroe from Dodge to Asbury",green:"Dempster to Main, Dodge to about Elmwood"},
 Oakton:{orange:"Main to Howard, Asbury to Sherman",blue:"Pocket west of Asbury, about Monroe to South Blvd"},
 Lincoln:{teal:"Dempster to the Calvary line, about Elmwood/Sherman to the lake",orange:"South of South Blvd, Sherman to about Hinman"}});''' + s[j:]

# ---------- 3. middle school land tab ----------
i = s.index('const MDESC={'); j = s.index('};', i) + 2
s = s[:i] + '''const MDESC={"Nichols|Chute":"Areas that become part of the Dawes and Oakton zones: the west half of today's Washington area and Lincoln's strip south of South Blvd.",
 "Nichols|Haven":"Dewey's north end, which becomes part of the Orrington zone, and a small pocket that goes to Foster.",
 "Nichols|Nichols":"Areas that stay in the Washington and Lincoln zones, including the middle of Dewey and south downtown.",
 "Haven|Haven":"Areas in the Orrington, Foster and Willard zones, including all of Lincolnwood.",
 "Chute|Chute":"All of today's Chute area stays at Chute. Dawes, Oakton and Walker feed Chute today and under the Oct 23 draft."};''' + s[j:]

# ---------- 4. student tabs on the district's Oct 28 counts ----------
i = s.index('const PRJ={'); j = s.index('const CL=', i)
s = s[:i] + '''/* Oct 23 draft. Moves are the district's Oct 28, 2026 counts of current K-4 students (Boundary Impacts for LODN sheet).
   Program rows (Dewey dual-language, STEP) are our K-4 estimates: the district withheld program moves for privacy. */
const K4={Dawes:233,Dewey:264,Foster:286,Lincoln:285,Lincolnwood:252,Oakton:303,Orrington:194,Walker:274,Washington:301,Willard:225};
/* our projection for next fall on the district's counts (Oct 29 rerun, central case) and seats (LoDN rule: lower of district teaching stations x 24 and Cordogan Clark) */
const PROJ={Dawes:340,Foster:401,Lincoln:467,Oakton:393,Orrington:273,Walker:319,Washington:432,Willard:513,Dewey:0,Lincolnwood:0};
const SEATS={Dawes:432,Dewey:537,Foster:576,Lincoln:576,Lincolnwood:432,Oakton:467,Orrington:432,Walker:432,Washington:530,Willard:533};
const MENR={Chute:588,Haven:601,Nichols:570};
/* n = count, lo/hi = range, c = confidence */
const SF={
 Dewey:[{to:"Washington",n:73,c:"conf"},{to:"Lincoln",n:42,c:"conf"},{to:"Lincoln",n:85,c:"high",step:true,prog:"dual-language strand",all:102},{to:"Orrington",n:10,c:"conf"},{to:"Foster",n:5,lo:1,hi:9,c:"conf",lt10:true}],
 Lincolnwood:[{to:"Willard",n:154,c:"conf"},{to:"Foster",n:38,c:"conf"},{to:"Orrington",n:19,c:"high",step:true,prog:"STEP program",all:23}],
 Washington:[{to:"Dawes",n:37,c:"conf"}],
 Oakton:[{to:"Dawes",n:19,c:"conf"}],
 Lincoln:[{to:"Oakton",n:37,c:"conf"}]};
''' + s[j:]
rep('const CL={conf:["c-conf","Confirmed"],high:["c-high","High confidence"],range:["c-range","Range"]};',
    'const CL={conf:["c-conf","District count"],high:["c-high","Our estimate"],range:["c-range","Range"]};')
rep('const sp=(n,v)=>Math.round(v*100/ENR[n]);', 'const sp=(n,v)=>Math.round(v*100/K4[n]);')
rep('if(!RM.includes(n))out.unshift({to:n,n:ENR[n]-moving,', 'if(!RM.includes(n))out.unshift({to:n,n:K4[n]-moving,')
rep('lo:out[0].hi!=null?ENR[n]-out.reduce((s,f)=>s+(f.hi??f.n),0):null,hi:out[0].lo!=null?ENR[n]-out.reduce((s,f)=>s+(f.lo??f.n),0):null', 'lo:null,hi:null')
rep('''stroke="${f.step?Z.red.c:'#111'}"''', '''stroke="${f.step?Z[ZK[f.to]].c:'#111'}"''')
rep('''${f.step?` style="fill:${Z.red.c}"`:''}>${f.na?'few':f.n===0?'≈0':(f.lo!=null?'≈':'')+f.n}</text>`}''',
    '''${f.step?` style="fill:${Z[ZK[f.to]].c}"`:''}>${f.na?'few':f.lt10?'<10':f.n===0?'≈0':(f.step?'≈':'')+f.n}</text>`}''')
rep('''<div class="desc">October 1, 2026 enrollment: <b>${ENR[n]}</b> students</div>`''',
    '''<div class="desc">October 1, 2026 enrollment: <b>${ENR[n]}</b> students, <b>${K4[n]}</b> in K-4. Moves count current K-4 students.</div>`''')
rep('''${f.stay?'Stays at '+n:'To '+f.to+(f.step?' (STEP program)':'')}''', '''${f.stay?'Stays at '+n:'To '+f.to+(f.step?' ('+f.prog+')':'')}''')
rep('''`<b>${f.lo!=null?'About ':''}${f.n} students</b>`}${f.na?'':`${f.lo!=null?` <span class="rng">(range ${Math.max(0,f.lo)} to ${f.hi})</span>`:''}. ${lp!=null?`Land share: ${lp}%.`:'No land share: STEP moves with the program.'}`}''',
    '''`<b>${f.lt10?'Under 10 students':(f.step?'About ':'')+f.n+' students'}</b>`}${f.na?'':`${f.step?` <span class="rng">(${f.all} in all grades; the district withheld program moves)</span>`:''}. ${lp!=null?`Land share: ${lp}%.`:'No land share: moves with the program.'}`}''')
# method, comparison note, table
i = s.index('$("esmethod").innerHTML=`'); j = s.index('`;', i) + 2
s = s[:i] + '''$("esmethod").innerHTML=`<p><b>Where these numbers come from.</b> The district's own counts for the Oct 23 draft, shared Oct 28, 2026: current K-4 students whose school changes. 660 move in all, 23% of 2,855 K-4 students. The district lists 446 of them by area. The other 214 or so are program and transfer moves it withheld for privacy, including Dewey's dual-language strand going to Lincoln and the STEP program going to Orrington. Those two rows are our estimates (about 85 of Dewey's 102 dual-language students and about 19 of the 23 STEP students are in K-4) and are marked. The district also lists 31 students placed at King Arts by program or transfer (20 from Dewey, 11 from Lincolnwood); King Arts is not one of these attendance areas, so they are not drawn. Dewey to Foster is listed as under 10. This year's 5th graders are not counted because they move up to middle school anyway.</p><p><b>Shares</b> are of each school's current K-4 students on October 1, 2026. <b>Next fall</b> in the table is our projection on these counts: grades aged a year, the district's moves applied, program moves added. It is our projection, not a district figure.</p><p>${chip("conf")} district count ${chip("high")} our estimate (program moves the district withheld)</p>`;''' + s[j:]
rep('Each row is one group of families that changes school. The square is its share of the sending school\'s land; the dot is its estimated share of the sending school\'s students; the shaded band is the range where the estimate is uncertain.',
    'Each row is one group of families that changes school. The square is its share of the sending school\'s land; the dot is its share of the sending school\'s current K-4 students (district count); the shaded band is a range where the count is not exact.')
rep('<span><i style="background:#b3261e"></i>Share of students (estimate)</span>', '<span><i style="background:#b3261e"></i>Share of K-4 students (district count)</span>')
i = s.index('  // table\n  const inc={},out={};for(const n in SF)'); j = s.index('</p>`;\n}', i) + len('</p>`;\n}')
s = s[:i] + '''  // table
  const inc={},out={};for(const n in SF)for(const f of SF[n]){out[n]=(out[n]||0)+f.n;inc[f.to]=(inc[f.to]||0)+f.n}
  const order2=["Dewey","Lincolnwood","Dawes","Foster","Lincoln","Oakton","Orrington","Walker","Washington","Willard"];
  const RC=v=>`<td style="text-align:right">${v}</td>`;
  let t=`<table><thead><tr><th>School</th><th style="text-align:right">Oct 1, 2026 (K-5)</th><th style="text-align:right">Current K-4</th><th style="text-align:right">K-4 leaving</th><th style="text-align:right">K-4 arriving</th><th style="text-align:right">Next fall (our projection)</th><th style="text-align:right">Seats</th><th style="text-align:right">Seat use</th></tr></thead><tbody>`;
  let tot=[0,0,0,0];
  for(const n of order2){const rm=RM.includes(n),lv=out[n]||0,ar=inc[n]||0,pj=PROJ[n],u=pj?Math.round(pj*100/SEATS[n]):null;tot[0]+=ENR[n];tot[1]+=K4[n];tot[2]+=ar;tot[3]+=pj;
    t+=`<tr><td class="nm">${n}${rm?' <span class="st-tag st-close">Proposed closing</span>':''}</td>${RC(ENR[n])}${RC(K4[n])}${RC(rm?'all':lv?'−'+lv:'0')}${RC(ar?'+'+ar:'0')}${RC(rm?'closes':'<b>'+pj+'</b>')}${RC(SEATS[n])}<td style="text-align:right;${u>=90?'color:var(--accent);font-weight:600':''}">${u==null?'–':u+'%'}</td></tr>`}
  t+=`<tr><td class="nm">10 schools</td>${RC(tot[0])}${RC(tot[1])}${RC('')}${RC('+'+tot[2])}${RC('<b>'+tot[3]+'</b>')}${RC('')}${RC('')}</tr></tbody></table>`;
  $("estable").innerHTML=t+`<p class="desc" style="padding:10px 14px 14px;max-width:none">"K-4 leaving" and "K-4 arriving" are the district's counts plus the two program moves; the 31 students placed at King Arts and transfers the district withheld are not in these columns. "Next fall" is our projection on the district's counts (grades aged one year, 5th graders leave, kindergarten held at this fall's size, about 110 withheld program and transfer movers spread over the closing schools' destinations). Seats are the lower of the district's teaching stations × 24 and the 2022 Cordogan Clark capacity. <b>Willard</b> reaches about 96% of its seats; Willard and Oakton could run short of classrooms. These are our projections, not district figures.</p>`;
}''' + s[j:]
# middle school students
i = s.index('const MSF={'); j = s.index('Chute:[]};', i) + len('Chute:[]};')
s = s[:i] + '''const MSF={Nichols:[{to:"Chute",k5:89,lo:.5,hi:.6,why:"Areas moving from Washington to Dawes and from Lincoln to Oakton: 74 current K-4 students (district counts, 37 each), about 89 on a K-5 basis"},{to:"Haven",k5:18,lo:.5,hi:.6,why:"Dewey's north end moving to Orrington (10, district count) and a small pocket to Foster (under 10): about 15 current K-4 students, about 18 on a K-5 basis"}],
 Haven:[],Chute:[]};''' + s[j:]
i = s.index('$("mssmethod").innerHTML=`'); j = s.index('`;', i) + 2
s = s[:i] + '''$("mssmethod").innerHTML=`<p><b>How these estimates work.</b> A middle school zone changes only where an elementary area moves to a school with a different feeder. On the Oct 23 draft that happens in two places, both leaving Nichols: the Washington to Dawes and Lincoln to Oakton areas go to Chute, and Dewey's north end goes to Haven. All of Lincolnwood stays in Haven, because Willard and Foster both feed Haven, and so does STEP (Orrington feeds Haven). We start from the district's K-4 counts for those areas, put them on a K-5 basis (× 1.2), and scale to middle school students by 0.55 (three middle school grades for six elementary grades, with middle school grades about 10% larger). The range uses 0.50 to 0.60. The district's own count: 144 current K-4 students change both elementary and middle school, including 31 placed at King Arts (K-8) by program or transfer.</p><p><b>Phase-in.</b> These are end-state figures. Current 6th and 7th graders stay at their middle school until they finish, so the change arrives one grade at a time.</p>`;''' + s[j:]
rep('''<th style="text-align:right">End state, on Oct 1 basis</th><th style="text-align:right">District projection (phased)</th></tr></thead><tbody>`;''',
    '''<th style="text-align:right">End state, on Oct 1 basis</th></tr></thead><tbody>`;''')
rep('''<td style="text-align:right"><b>${MENR[n]-lv+ar}</b></td><td style="text-align:right">${MPRJ[n]}</td></tr>`}''', '''<td style="text-align:right"><b>${MENR[n]-lv+ar}</b></td></tr>`}''')
rep('''All middle school figures are rough estimates. The district's projection is lower for Chute and higher for Nichols than the end state, consistent with current students staying until they graduate.''',
    '''All middle school figures are rough end-state estimates. The district has not published middle school projections for the Oct 23 draft.''')
# flow tables
rep('''<p>One row per group of families that changes school, plus the share that stays for schools that split. Land is exact for the boundaries as drawn. Students use October 1, 2026 enrollment; where the number is not known, the estimate is the midpoint of the range in the last columns.</p>''',
    '''<p>One row per group of families that changes school, plus the share that stays for schools that split. Land is exact for the boundaries as drawn. Students are the district's Oct 28, 2026 counts of current K-4 students; program rows are our estimates, and "under 10" is shown as 5 with a range of 1 to 9. Shares are of each school's current K-4 students.</p>''')
rep('''f.stay?n+" (stays)":f.to+(f.step?" (STEP)":"")''', '''f.stay?n+" (stays)":f.to+(f.step?" ("+f.prog+")":"")''')
rep('''h+=`<tr class="grp"><td colspan="2">${n}${RM.includes(n)?' (proposed closing)':''}</td><td class="n">${Math.round(totA)}</td><td class="n">100%</td><td class="n">${tot}</td><td class="n">100%</td><td colspan="5"></td></tr>`;''',
    '''h+=`<tr class="grp"><td colspan="2">${n}${RM.includes(n)?' (proposed closing)':''}</td><td class="n">${Math.round(totA)}</td><td class="n">100%</td><td class="n">${K4[n]}</td><td class="n">100%</td><td colspan="5"></td></tr>`;''')

# ---------- 5. builder: seats on the LoDN rule, Oct 23 wording ----------
i = s.index('/* District FY28 utilization table (Oct 7, 2026)'); j = s.index('const UPC=', i)
s = s[:i] + '''/* Seats: lower of the district's teaching stations x 24 and the 2022 Cordogan Clark capacity (LoDN rule, the same on
   D65 School Circles and the Oct 23 map pages). Source: repo dataanalysis/data/sy27_fall/capacity_comparison.csv. */
const CAP={Dawes:432,Dewey:537,Foster:576,Lincoln:576,Lincolnwood:432,Oakton:467,Orrington:432,Walker:432,Washington:530,Willard:533};
''' + s[j:]
rep('<button type="button" id="dwfy28">FY28 tentative</button>', '<button type="button" id="dwfy28">Oct 23 draft</button>')
rep("<b>FY28 tentative</b> (the district's proposal)", "<b>Oct 23 draft</b> (the district's latest proposal)")
rep('''<th title="Students divided by the district's FY28 capacity">Util.</th>''', '''<th title="Students divided by seats (lower of teaching stations × 24 and Cordogan Clark capacity)">Util.</th>''')
rep('''Utilization is students divided by the district's FY28 capacity (the lower of homerooms × 24 and the building's square-footage limit), the same method as its utilization table;''',
    '''Utilization is students divided by seats: the lower of the district's teaching stations × 24 and the 2022 Cordogan Clark capacity, the same rule as the other LoDN maps;''')
rep('/* rasterize polygons to find each cell\'s share of each FY27 area and its FY28 zone */', '/* rasterize polygons to find each cell\'s share of each FY27 area and its Oct 23 zone */')

# ---------- 6. census tabs and transportation ----------
rep('const SCN=[["fy27","FY27 areas"],["fy28","FY28 tentative"],["mine","Your drawn map"]];', 'const SCN=[["fy27","FY27 areas"],["fy28","Oct 23 draft"],["mine","Your drawn map"]];', 2)
rep('This estimate for the FY28 tentative map is <b>${rng(costRange(f28))}</b>', 'This estimate for the Oct 23 draft is <b>${rng(costRange(f28))}</b>')
# demographics: rebuild the anchor table on district counts
RATES = {"Dawes": [47.3, 20.6, 18.2, 92.1, 14.8, 4.1], "Washington": [40.3, 24.8, 17.9, 94.0, 22.0, 3.4], "Lincoln": [38.1, 17.4, 16.2, 94.4, 9.2, 4.1],
         "Oakton": [52.0, 21.3, 15.8, 93.1, 26.5, 8.4], "Orrington": [20.5, 12.9, 17.0, 96.2, 8.1, None], "Walker": [36.0, 14.0, 14.9, 93.8, 16.0, None],
         "Willard": [22.4, 14.4, 17.3, 94.1, 8.2, None], "Foster": [39.0, 16.5, 18.1, None, None, None], "Dewey": [28.9, 19.2, 15.7, 94.6, 13.6, 5.0],
         "Lincolnwood": [34.6, 5.6, 16.4, 94.3, 12.4, None]}
D20 = NEWD['D2']; old_rc = json.loads(json.dumps(D20['rc']))
CUR = {z: old_rc['zones'][z]['current'] for z in old_rc['zones']}
FLOWS = {("Lincolnwood", "Willard"): 154, ("Lincolnwood", "Foster"): 38, ("Lincolnwood", "Orrington"): 23, ("Dewey", "Washington"): 73, ("Dewey", "Lincoln"): 42 + 102,
         ("Dewey", "Orrington"): 10, ("Dewey", "Foster"): 5, ("Washington", "Dawes"): 37, ("Oakton", "Dawes"): 19, ("Lincoln", "Oakton"): 37}
PROJ = {"Dawes": 340, "Foster": 401, "Lincoln": 467, "Oakton": 393, "Orrington": 273, "Walker": 319, "Washington": 432, "Willard": 513}
zones = {}
for z in PROJ:
    outf = sum(v for (a, b), v in FLOWS.items() if a == z)
    base = CUR[z] if CUR[z] else 353   # Foster has no report card yet: Oct 1, 2026 enrollment
    frm = [{"school": z, "students": round(base - outf)}] + [{"school": a, "students": v} for (a, b), v in FLOWS.items() if b == z]
    tot = sum(f["students"] for f in frm)
    def mix(k):
        vals = [(f["students"], RATES[f["school"]][k]) for f in frm]
        if any(v is None for _, v in vals): return None
        return round(sum(w * v for w, v in vals) / tot, 1)
    own = RATES[z]
    zones[z] = {"projected": PROJ[z], "current": CUR[z], "fromTotal": tot, "from": frm, "li": mix(0), "el": mix(1), "iep": mix(2), "att": mix(3), "tru": mix(4), "hl": mix(5),
                "cur_li": own[0], "cur_el": own[1], "cur_iep": own[2], "cur_att": own[3], "cur_tru": own[4], "cur_hl": own[5]}
rc = {"flows": {}, "zones": zones, "meta": {"moved": 660, "listed": 446, "withheld": 214, "both": 144, "k4": 2855}}
for (a, b), v in FLOWS.items(): rc["flows"].setdefault(a, []).append({"to": b, "students": v})
D20['rc'] = rc
swap('D2', D20)
rep('''<p class="sub" style="margin:0">Student counts are anchored to the district's own figure from the Oct 13, 2026 board presentation: <b>713 students changing schools</b>. Every Dewey and Lincolnwood student moves, which is about ${M.closing} by report-card enrollment. That leaves about ${M.split} students moving because of boundary shifts at Washington, Oakton and Lincoln. Within each school, students are split by where its elementary-age kids live (2020 Census). Movers carry their current school's low-income, English learner and IEP rates.</p>''',
    '''<p class="sub" style="margin:0">Student counts are anchored to the district's own counts for the Oct 23 draft (shared Oct 28, 2026): <b>660 current K-4 students changing schools</b>, ${M.listed} of them listed by area. Each new zone is made of its own students who stay plus the district's counts of students arriving, with Dewey's dual-language strand (102) to Lincoln and STEP (23) to Orrington added. Movers carry their current school's low-income, English learner and IEP rates. "Next fall" is our projection on the same counts.</p>''')
rep('''<div class="v">713</div><div class="d">District figure, Oct 13 board deck</div></div>`+''',
    '''<div class="v">660</div><div class="d">District count, current K-4 (Oct 28, 2026)</div></div>`+''')
rep('''`<div class="kpi"><div class="k">Marginalized students changing</div><div class="v">329</div><div class="d">District figure (46% of movers)</div></div>`+''',
    '''`<div class="kpi"><div class="k">Change elementary and middle school</div><div class="v">144</div><div class="d">District count, current K-4</div></div>`+''')
rep('''`<div class="kpi"><div class="k">From closing schools</div><div class="v">~${M.closing}</div><div class="d">Dewey ~313 · Lincolnwood ~287</div></div>`+''',
    '''`<div class="kpi"><div class="k">Listed by area</div><div class="v">${M.listed}</div><div class="d">District sheet, by area</div></div>`+''')
rep('''`<div class="kpi"><div class="k">From boundary shifts</div><div class="v">~${M.split}</div><div class="d">Washington, Oakton, Lincoln</div></div></div>`;''',
    '''`<div class="kpi"><div class="k">Program and transfer moves</div><div class="v">~${M.withheld}</div><div class="d">Withheld by area for privacy</div></div></div>`;''')
rep('<th>New school</th><th>Today</th><th>Projected</th><th>Change</th>', '<th>New school</th><th>Today</th><th>Next fall (our projection)</th><th>Change</th>')
rep('${r.from.map(x=>`<span style="width:${x.students*100/r.projected}%;', '${r.from.map(x=>`<span style="width:${x.students*100/(r.fromTotal||r.projected)}%;')
rep('''The district puts overall K-5 utilization at 75.7% after consolidation. Program moves in the deck are not modeled here: the Dewey TWI strand moves to Lincoln as a cohort, Lincolnwood STEP moves to Orrington as a cohort, current permissive transfers can stay, and all TWI students keep their program. Those will shift some counts between schools. King Arts (about 433 students) is a district-wide magnet with no attendance boundary, so it is not on these maps and does not gain or lose area. Its students live in every zone, which is one reason only 42% to 73% of each area's resident kids attend their neighborhood school. The deck keeps King Arts open with a neighborhood preference zone, not an assigned area.''',
    '''"Made up of" counts this year's students who stay plus the district's arrivals (current K-4) and the two program moves; rates are weighted by that mix. Current permissive transfers can stay, and all TWI students keep their program. King Arts (about 445 students) draws from across the district; the Oct 23 layer also draws its small neighborhood area west of Dodge, which is King Arts' area today too, so it does not change. Its students live in every zone, which is one reason only 42% to 73% of each area's resident kids attend their neighborhood school.''')
rep('<b>Demographics.</b> Student counts are anchored to the district\'s figure of 713 students changing schools.', '<b>Demographics.</b> Student counts are anchored to the district\'s Oct 28 counts for the Oct 23 draft (660 current K-4 students changing schools).')

# ---------- 7. static tiles and text ----------
fmt = lambda v: f"{v:,.0f}"
ac = TL['acres']; ch, bo, eo, sa = TL['change'], TL['both'], TL['elemonly'], TL['same']
pct = lambda v: f"{v * 100 / ac:.1f}%"
area_tiles_old = s[s.index('<div class="dtile dt-main"><div class="dv">33.7%</div>'):s.index('where the 2026-27 and 2027-28 maps don\'t line up.</p>') + len('where the 2026-27 and 2027-28 maps don\'t line up.</p>')]
area_tiles_new = f'''<div class="dtile dt-main"><div class="dv">{pct(ch)}</div><div class="dl">District area disruption rate</div><div class="ds">about {fmt(round(ch, -1))} acres</div></div>
  <div class="dtile"><div class="dv">{pct(bo)}</div><div class="dl">Elementary and middle school change</div><div class="ds">about {fmt(round(bo, -1))} acres</div></div>
  <div class="dtile"><div class="dv">{pct(eo)}</div><div class="dl">Elementary only (same middle school)</div><div class="ds">about {fmt(round(eo, -1))} acres</div></div>
  <div class="dtile"><div class="dv">{pct(sa)}</div><div class="dl">No change</div><div class="ds">about {fmt(round(sa, -1))} acres</div></div>
  </div>
  <p class="dn">Out of about {fmt(round(ac, -1))} district acres. King Arts' neighborhood area (west of Dodge, Church to Dempster) is left out: it is King Arts' area on both maps. Every middle school change also changes elementary school, so the elementary figure is the total. Land area, not students. Both maps come from the same district layer, so they line up along the lakefront.</p>'''
rep(area_tiles_old, area_tiles_new, 2)
L = TL
lines_old = s[s.index('<div class="dtile dt-main"><div class="dv">73.5%</div>'):s.index('<div class="lzwrap">')]
rate = (L['removed'] + L['new']) / L['total']
lines_new = f'''<div class="dtile dt-main"><div class="dv">{rate * 100:.1f}%</div><div class="dl">District boundary disruption rate</div><div class="ds">about {L['removed'] + L['new']:.1f} of {L['total']:.1f} miles of lines</div></div>
  <div class="dtile"><div class="dv">{L['removed'] / L['Lo'] * 100:.0f}%</div><div class="dl">FY27 lines removed</div><div class="ds">about {L['removed']:.1f} of {L['Lo']:.1f} miles</div></div>
  <div class="dtile"><div class="dv">{L['new'] / L['Ln'] * 100:.0f}%</div><div class="dl">Oct 23 lines that are new</div><div class="ds">about {L['new']:.1f} of {L['Ln']:.1f} miles</div></div>
  <div class="dtile"><div class="dv">{L['unchanged'] / L['total'] * 100:.1f}%</div><div class="dl">Lines unchanged</div><div class="ds">about {L['unchanged']:.1f} miles</div></div>
  </div>
  <p class="dms"><b>9 of 10 elementary zones change:</b> 2 close and 7 of the 8 continuing schools have edges that move. Walker's lines are unchanged on the Oct 23 draft. Compare {pct(ch)} of land area: small shifts of land can move long lines, so lines change far more than area.</p>
  '''
rep(lines_old, lines_new)
rows = []
for n, r in sorted(L['per'].items(), key=lambda kv: -kv[1]['moved']):
    if n in ("Dewey", "Lincolnwood"):
        rows.append(f'<tr><td>{n} (proposed closing)</td><td class="n">{r["old"]:.1f}</td><td class="n">{r["moved"] * 100:.0f}%</td><td class="n">n/a</td><td class="n">n/a</td></tr>')
    else:
        rows.append(f'<tr><td>{n}</td><td class="n">{r["old"]:.1f}</td><td class="n">{r["moved"] * 100:.0f}%</td><td class="n">{r["new"]:.1f}</td><td class="n">{r["newshare"] * 100:.0f}%</td></tr>')
i = s.index('<div class="lzwrap"><table class="lzt">'); j = s.index('</tbody></table></div>', i) + len('</tbody></table></div>')
s = s[:i] + '<div class="lzwrap"><table class="lzt"><thead><tr><th>School</th><th class="n">FY27 edges (mi)</th><th class="n">Share moved</th><th class="n">Oct 23 edges (mi)</th><th class="n">Share new</th></tr></thead><tbody>\n  ' + '\n  '.join(rows) + '\n  </tbody></table></div>' + s[j:]
i = s.index('<p class="dn">Lines are the internal edges between attendance zones;'); j = s.index('</p>', i) + 4
s = s[:i] + '<p class="dn">Lines are the internal edges between attendance zones; the district\'s outer edge is left out. A line counts as unchanged if it stays within 100 feet of where it was. Each zone\'s edges are counted once per zone, so shared edges appear in two rows. Both maps are the district\'s own layers (FY28 Proposed Boundaries map, pulled Oct 23, 2026), so the comparison is not affected by tracing. This measures where lines are drawn, not which schools they separate: part of Dewey\'s and Lincolnwood\'s edges stay on the map as the edge between two other schools, so they count as unchanged.</p>' + s[j:]
MSL = TL['ms']; mrate = (MSL['removed'] + MSL['new']) / MSL['total']
ms_old = s[s.index('<div class="dtile dt-main"><div class="dv">91.7%</div>'):s.index('</div>\n  <p class="sub">2026-27 official middle school zones')]
ms_new = f'''<div class="dtile dt-main"><div class="dv">{mrate * 100:.1f}%</div><div class="dl">Middle school boundary disruption rate</div><div class="ds">about {MSL['removed'] + MSL['new']:.1f} of {MSL['total']:.1f} miles of lines</div></div>
  <div class="dtile"><div class="dv">{MSL['removed'] / MSL['Lo'] * 100:.0f}%</div><div class="dl">2026-27 lines removed</div><div class="ds">about {MSL['removed']:.1f} of {MSL['Lo']:.1f} miles</div></div>
  <div class="dtile"><div class="dv">{MSL['new'] / MSL['Ln'] * 100:.0f}%</div><div class="dl">2027-28 lines that are new</div><div class="ds">about {MSL['new']:.1f} of {MSL['Ln']:.1f} miles</div></div>
  <div class="dtile"><div class="dv">{MSL['unchanged'] / MSL['total'] * 100:.1f}%</div><div class="dl">Lines unchanged</div><div class="ds">about {MSL['unchanged']:.1f} miles</div></div>
  </div>
  <p class="dms"><b>All 3 middle school zones change.</b> Chute keeps the same three feeder schools, yet {MSL['per']['Chute']['moved'] * 100:.0f}% of its edges move, because Dawes and Oakton gain area from Nichols. Compare {pct(bo)} of land area.</p>
  <p class="dn">2027-28 zones are the Oct 23 elementary zones grouped by the feeder pattern on slide 18 of the October 13, 2026 deck (the Oct 23 draft keeps the same feeders). Lines are internal edges between middle school zones, excluding the district's outer edge, and count as unchanged if within 100 feet.</p>
  '''
rep(ms_old, ms_new)
stu_old = s[s.index('<div class="dtile dt-main"><div class="dv">25.6%</div>'):s.index('The linked flows move together, so the ranges are narrower than adding up each flow\'s range.</p>') + len('The linked flows move together, so the ranges are narrower than adding up each flow\'s range.</p>')]
stu_new = '''<div class="dtile dt-main"><div class="dv">23.1%</div><div class="dl">District student disruption rate</div><div class="ds">660 students</div><div class="dr">District count</div></div>
  <div class="dtile"><div class="dv">5.0%</div><div class="dl">Elementary and middle school change</div><div class="ds">144 students</div><div class="dr">District count, includes 31 placed at King Arts</div></div>
  <div class="dtile"><div class="dv">18.1%</div><div class="dl">Elementary only (same middle school)</div><div class="ds">516 students</div><div class="dr">District count</div></div>
  <div class="dtile"><div class="dv">76.9%</div><div class="dl">No change</div><div class="ds">2,195 students</div><div class="dr">District count</div></div>
  </div>
  <p class="dn">Out of 2,855 current K-4 students: the district's Oct 28, 2026 counts for the Oct 23 draft. Counts include about 214 program and transfer moves the district assigns by rule but does not list by area. The district's headline 13.7% divides by all 4,805 K-7 students; grades 5 to 7 cannot change school under its rules.</p>'''
rep(stu_old, stu_new, 2)
rep('''<p class="dsub">Share of K-5 students (October 1, 2026 enrollment) whose school assignment changes under the proposal</p>''',
    '''<p class="dsub">Share of current K-4 students whose school changes under the Oct 23 draft (district counts)</p>''', 2)
rep('''<p class="dms"><b>Middle school student disruption rate: about 9.2%.</b> About 162 of 1,759 current middle schoolers (range 148 to 177, or 8.4% to 10.1%) live in areas that switch middle school. Rough end-state figure using 0.55 middle schoolers per K-5 student; actual effects depend on how current students are phased in.</p>''',
    '''<p class="dms"><b>Middle school changes: 144 current K-4 students (district count).</b> By area, about 74 current K-4 students in the Washington to Dawes and Lincoln to Oakton areas switch from Nichols to Chute, and about 15 in Dewey's north end switch from Nichols to Haven; the rest are program and transfer placements, including 31 at King Arts. End state for today's middle school grades: about 59 students (range 53 to 64) once fully phased in. Current 6th and 7th graders stay at their school.</p>''')
rep('''<div class="viewnote vn-stu" role="note"><b>By estimated students.</b> Counts use October 1, 2026 enrollment, the district's Lincolnwood figures and its post-consolidation enrollment table. Each figure is marked confirmed, high confidence or a range.</div>''',
    '''<div class="viewnote vn-stu" role="note"><b>By estimated students.</b> Counts are the district's own figures for the Oct 23 draft: current K-4 students changing school (shared Oct 28, 2026). Program moves the district withheld are our estimates and are marked.</div>''')
rep('''<div class="viewnote vn-stu" role="note"><b>By estimated students.</b> Rough end-state estimates built from the elementary estimates, before current middle schoolers phase out.</div>''',
    '''<div class="viewnote vn-stu" role="note"><b>By estimated students.</b> Rough end-state estimates built from the district's elementary counts for the Oct 23 draft, before current middle schoolers phase out.</div>''')
rep('''<p class="sub">How many students move when Dewey and Lincolnwood are proposed to close, based on October 1, 2026 enrollment. Every school's outgoing students add up to its October 1 enrollment, so year-to-year changes in enrollment do not distort the shares.</p>''',
    '''<p class="sub">How many students move on the Oct 23 draft, from the district's counts of current K-4 students. Shares are of each school's K-4 students on October 1, 2026.</p>''')
rep('<h2 class="sec">Every school: October 1, 2026 enrollment and the district projection</h2>', '<h2 class="sec">Every school: October 1, 2026 enrollment and our projection for next fall</h2>')
rep('<h2 class="sec">Every middle school: October 1, 2026 enrollment and the district projection</h2>', '<h2 class="sec">Every middle school: October 1, 2026 enrollment and the end state</h2>')
rep('''"28% of Dewey goes to Foster" means 28% of Dewey's attendance-area land.''', '''"33% of Dewey goes to Lincoln" means 33% of Dewey's attendance-area land.''')
rep('''The exception is Lincolnwood, where the district's student counts are shown and labeled "Students."''', '''The exception is Lincolnwood, where the district's student counts (current K-4) are shown and labeled "Students."''')
rep('''so the implied middle school zones follow the tentative elementary map.''', '''so the implied middle school zones follow the Oct 23 elementary map.''')
rep('''They match the district's official 2026-27 middle school layer in Google Maps to within about 1% of area. The district has not published 2027-28 middle school zones, so they are the 2027-28 tentative elementary zones grouped by the feeder pattern on slide 18 of the Oct 13 board deck:''',
    '''They closely match the district's official 2026-27 middle school layer. The district has not published 2027-28 middle school zones, so they are the Oct 23 draft elementary zones grouped by the feeder pattern on slide 18 of the Oct 13 board deck (unchanged on Oct 23):''')
rep('''<p>All lines on both tabs come from the district's Google Maps layers (FY28 Tentative Boundaries and District 65 Boundaries, downloaded Oct 14, 2026), placed on the district's FY28 map image. Expect small offsets from the basemap,''',
    '''<p>All lines on both tabs come from the district's FY28 Proposed Boundaries Google map: its 2026-27 layer and its "Oct. 23, 2026 Proposed Boundaries" layer (pulled Oct 23, 2026), placed on the district's FY28 map image. Expect small offsets from the basemap,''')
rep('''<li><b>Boundary lines.</b> District 65 Google Maps layers "FY28 Tentative Boundaries" and "District 65 Boundaries," downloaded October 14, 2026, and placed by hand on the district's FY28 map image. The district's official 2026-27 middle school layer was used as a check.</li>''',
    '''<li><b>Boundary lines.</b> District 65's "FY28 Proposed Boundaries" Google map: the 2026-27 layer (today) and the "Oct. 23, 2026 Proposed Boundaries" layer, pulled October 23, 2026, and placed on the district's FY28 map image. The Oct 23 layer also draws King Arts' small neighborhood area west of Dodge; it is King Arts' area today too, so it is left out of Dewey's 2026-27 area. Earlier versions of this page used the Oct 13 layer ("FY28 Tentative Boundaries," downloaded October 14).</li>''')
rep('''<li><b>Closure flows.</b> The district's Lincolnwood figures (269 to Willard, 39 to Walker, 23 STEP students to Orrington) and its post-consolidation projected enrollment table.</li>''',
    '''<li><b>Student moves.</b> The district's counts for the Oct 23 draft, shared October 28, 2026 ("Boundary Impacts for LODN" sheet): 660 current K-4 students change school (Lincolnwood to Willard 154, Dewey to Washington 73, Dewey to Lincoln 42, Lincolnwood to Foster 38, Lincoln to Oakton 37, Washington to Dawes 37, Oakton to Dawes 19, Dewey to Orrington 10, Dewey to Foster under 10, 31 to King Arts); 144 change elementary and middle school. Program and transfer moves are withheld by area.</li>''')
rep('''and the district's figures of 713 students changing schools and 329 marginalized students changing (Oct 13, 2026 board deck).</li>''',
    '''and the district's Oct 28, 2026 counts of students changing schools on the Oct 23 draft.</li>''')
rep('''Each cell's students come from the FY27 area and FY28 zone it falls in,''', '''Each cell's students come from the FY27 area and Oct 23 zone it falls in,''')
rep('''Utilization divides students by the district's FY28 capacity from its October 7, 2026 utilization table (the lower of homerooms × 24 and the square-footage capacity). Dewey and Lincolnwood have no FY28 capacity because they are proposed to close, so the builder uses their homerooms × 24 (600 and 480).''',
    '''Utilization divides students by seats: the lower of the district's teaching stations × 24 and the 2022 Cordogan Clark capacity (the same rule as the other LoDN maps). The district's FY28 table (October 7, 2026) gives different numbers for some schools, for example Willard 512 and Orrington 360.''')
rep('''<code>CAP</code> holds the FY28 capacity used for utilization,''', '''<code>CAP</code> holds the seats used for utilization (lower of teaching stations × 24 and Cordogan Clark),''')
rep('''<code>D.new</code> (FY28 tentative zones)''', '''<code>D.new</code> (Oct 23 draft zones)''')
i = s.find('Student tabs split each school');
if i >= 0:
    j = s.index('.', s.index('midpoint', i)) + 1
    s = s[:i] + 'Student tabs use the district\'s Oct 28, 2026 counts of current K-4 students changing school on the Oct 23 draft; the two program moves (Dewey\'s dual-language strand to Lincoln, STEP to Orrington) are our K-4 estimates because the district withheld program moves.' + s[j:]
rep('''<li><b>See what the district's proposal changes:</b>''', '''<li><b>Every tab uses the district's latest draft, Oct 23, 2026</b>, with its own Oct 28 counts of students who change school. Dewey and Lincolnwood close.</li>
      <li><b>See what the district's proposal changes:</b>''')


# ---------- 9. method sentences that changed with the new walks and King Arts' area ----------
rep('Distance from each home to its assigned school building, measured along the street grid (blocks east-west plus blocks north-south). Each result is weighted by where elementary-age kids actually live (2020 Census blocks), so parks, campus and cemetery land count for nothing.',
    'Distance from each census block to its assigned school building, walking along streets, alleys and paths (2023 Census road file; expressways and ramps left out), the same walks as D65 School Circles. Each result is weighted by where elementary-age kids actually live (2020 Census blocks), so parks, campus and cemetery land count for nothing.')
rep('Kid-based walking distance is measured along the street grid from each home to its assigned school and ignores canal and rail crossings.',
    'Kid-based walking distance follows streets, alleys and paths from each census block to its assigned school (2023 Census road file; expressways and ramps left out), the same walks used on D65 School Circles.')
rep("King Arts is a district-wide magnet with no attendance area, so the boundary maps don't change its riders;", "King Arts draws from across the district, and its small neighborhood area is the same on every map, so the boundary maps don't change its riders;")
rep('Foster has no report card yet, so its own students are estimated from Census kids and use district-average rates.', 'Foster has no report card yet, so its rates are estimates.')
rep('End state for today\'s middle school grades: about 59 students (range 53 to 64) once fully phased in.', 'End state for today\'s middle school grades: about 59 students (range 54 to 64) once fully phased in.')


# ---------- 10. basemap: the old image was the district's Oct 13 map with its zones painted in ----------
import base64 as _b64
b1 = 'data:image/jpeg;base64,' + _b64.b64encode(open(B + 'basemap.jpg', 'rb').read()).decode()
b2 = 'data:image/jpeg;base64,' + _b64.b64encode(open(B + 'basemap2.jpg', 'rb').read()).decode()
m = re.search(r'(id="base"[^>]*?href=")(data:image/[^"]+)(")', s)
s = s[:m.start(2)] + b1 + s[m.end(2):]
m = re.search(r'(const BASE2=")(data:image/[^"]+)(")', s)
s = s[:m.start(2)] + b2 + s[m.end(2):]
for a, bb in [("placed on the district's FY28 map image. The Oct 23 layer", "drawn on a street basemap from the U.S. Census 2023 road file (the same map frame as D65 School Circles). The Oct 23 layer"),
              ("(pulled Oct 23, 2026), placed on the district's FY28 map image.", "(pulled Oct 23, 2026), drawn on a street basemap from the U.S. Census 2023 road file.")]:
    rep(a, bb)


rep("so student counts, class sizes and utilization here are rough estimates, not a forecast.</div>",
    "so student counts, class sizes and utilization here are rough estimates, not a forecast. Starting from the Oct 23 draft, this puts far more students at Dawes (about 530) than the district's counts do (about 340 next fall on our projection), because Washington's 195 dual-language students are spread over Washington's area and half of that area moves to Dawes. Use the By estimated students tab for the district's counts. King Arts' neighborhood area is left blank: it is King Arts' area on both maps.</div>")

# ---------- 8. version tile ----------
rep('<div><span class="vk">Last updated</span><span class="vv">Sunday, October 18, 2026</span></div>', '<div><span class="vk">Last updated</span><span class="vv">Monday, November 2, 2026</span></div>')
rep('<div><span class="vk">Time</span><span class="vv">7:30 PM CT</span></div>', '<div><span class="vk">Time</span><span class="vv">5:00 PM CT</span></div>')
rep('<div><span class="vk">Updated by</span><span class="vv">JC</span></div>', '<div><span class="vk">Updated by</span><span class="vv">Paul</span></div>')
rep('<div><span class="vk">Latest change</span><span>Added a race and ethnicity dot map, a Transportation tab, maps that fit the screen, and a credit line.</span>',
    '<div><span class="vk">Latest change</span><span>Every tab now uses the district\'s Oct 23 draft and its Oct 28 counts; new "Oct 23 draft" tabs.</span>')
rep('<details class="vlog"><summary>All updates</summary>', '''<details class="vlog"><summary>All updates</summary>
        <div class="vday"><b>Nov. 2, 2026, 5:00 PM CT</b> &middot; Paul
          <ul>
            <li>All tabs moved from the Oct 13 tentative lines to the district's Oct 23, 2026 draft. Today's and Oct 23 lines both come from the district's FY28 Proposed Boundaries map, so they line up. Walker no longer gains part of Lincolnwood; Lincolnwood's south end goes to Foster.</li>
            <li>Student tabs use the district's Oct 28 counts of current K-4 students (660 move, 144 change middle school) instead of estimates built from the Oct 13 deck; program moves the district withheld are marked as our estimates. The district projection column is replaced by our projection for next fall on the same counts.</li>
            <li>Land shares, walking distances, disruption rates, Census-based tabs, demographics and the boundary builder's Oct 23 starting map recomputed. The same methods reproduce the page's earlier Oct 13 figures.</li>
            <li>Seats use the LoDN rule (lower of teaching stations × 24 and Cordogan Clark), the same as the other maps.</li>
            <li>The basemap is now a plain street map (U.S. Census 2023 roads). The old one was the district's Oct 13 map image, which showed the Oct 13 zones underneath.</li>
            <li>New "Oct 23 draft" tabs: what changes, and the school circles explorer.</li>
          </ul></div>''')

open(out, 'w').write(s)
print('wrote', out, len(s))
