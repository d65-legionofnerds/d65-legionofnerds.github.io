# What Happens When Parents Get Serious About Public Records

## A guest post by the Legion of Data Nerds

---

The Legion of Data Nerds is a group of District 65 parents who are focused on data and transparency. We are economists, data scientists, engineers, and policy analysts. We have built Python scripts, scraped salary disclosures, and cross-referenced state financial databases. And we have published our work publicly (methodology, code, and all) so that anyone can verify every figure we cite.

---

## What We Found

Over the past month, we published two analyses of D65's administrative structure. Together, they tell a single story: over the past decade, D65's central office more than tripled in size, increasing costs while enrollment fell.

**[The Org Chart That Ate Our Budget](https://d65-legionofnerds.github.io/dataanalysis/d65_org_structure_analysis.html)** traces D65's administrative growth from 2016 to today using board-approved org charts, state salary disclosures, and [ISBE financial data](https://www.isbe.net/Pages/Annual-Financial-Report.aspx). The headline findings:

- Enrollment fell **25%** — the steepest decline among [21 peer K-8 districts](https://d65-legionofnerds.github.io/dataanalysis/enrollment-data.html)
- Per-student administrative spending rose **55%** after adjusting for inflation
- The sub-cabinet (the layer of directors, coordinators, and program managers below the superintendent) grew **7 times its 2016 size** and was barely touched by the District's cost-cutting plan
- The District officially reports **52** central administrators; cross-referencing three public state disclosure lists reveals at least **64**
- D65 spends **$619 per pupil** on Special Area Administration against a peer average of **$176**

| Metric | Value |
|---|---|
| Enrollment decline | **-25%** · steepest among 21 peer districts |
| Sub-cabinet growth since 2016 | **7×** · left largely intact by SDRP |
| Per-pupil admin spending (inflation-adjusted) | **+55%** |
| Official vs. actual admin count | **52→64+** · cross-referencing public lists |
| Per-pupil Special Area Admin | **$619** · vs. peer average of $176 |

*From [The Org Chart That Ate Our Budget](https://d65-legionofnerds.github.io/dataanalysis/d65_org_structure_analysis.html)*

The figure below shows the exponential growth in central office positions during the Horton years. The SDRP only partially reversed the damage at the cabinet level while the sub-cabinet remained largely intact.

![Two-Tier Administrative Growth: Cabinet vs. Sub-Cabinet, 2016–2026](chart-two-tier-growth.jpg)

*Stacked bar chart showing cabinet and sub-cabinet administrative positions at D65 from 2016–17 through 2025–26. The SDRP dramatically cut the cabinet but left sub-cabinet largely intact. Cabinet: 8, 8, 9, 10, 12, 6. Sub-cabinet: 6, 9, 20, 38, 48, 42.*

**Legend:** Cabinet (asst. superintendents, chiefs, deputy superintendent) · Sub-cabinet (directors, coordinators, managers) · Post-SDRP (2025–26) · Horton era (2019–2023)

> \* 2020–21 sub-cabinet figure (~20) is a partial estimate. The 2020-21 org chart documents cabinet-level expansion but does not enumerate all sub-cabinet positions with the same specificity as later years. The true figure likely falls between the 2019 Summer baseline (9) and the 2021-22 count (38); ~20 reflects a conservative midpoint estimate. All other data points are drawn from named positions in primary source documents.
>
> Sources: D65 org charts (FOIA Gras docs 4479, 3906, 3180), [PA 96-0434](https://www.ilga.gov/Legislation/publicacts/view/096-0434) TRS Administrator reports (docs 1640, 4133), [Gavin budget document analysis](https://github.com/d65-legionofnerds/d65-legionofnerds.github.io/blob/main/dataanalysis/data/Gavin%20FOIA%20Response%205.14.24-6.pdf) (May 2024 FOIA response). **Note:** figures reflect named positions traceable through org charts and budget documents (cabinet + sub-cabinet = 48 for 2025–26). The separately documented count of 64 total administrators draws on all three state disclosure lists and captures additional positions not visible in org charts — see the Undercounting Problem callout [in our original post](https://d65-legionofnerds.github.io/dataanalysis/d65_org_structure_analysis.html#3-tell-the-community-what-the-administrative-structure-actually-costs-and-does).
>
> ‡ FOIA Gras document numbers refer to records in the [FOIAGras](https://foiagras.com) D65 document library. Documents can be searched by number or keyword using the [FOIAGras MCP integration](https://foiagras.com/mcp/).

The chart makes the asymmetry of the District's cost-cutting visible in a way raw numbers cannot. The cabinet (the superintendent's senior leadership team, seen on the dais at board meetings) was cut 50% under the SDRP, finishing below its 2016 starting point. The sub-cabinet contracted by just 13% while remaining seven times its original size. A conservative right-sizing of the sub-cabinet to peer-district norms would save $2.8 to $3.8 million annually without touching a single teacher, counselor, or librarian.

**[District 65 Administrative Growth Over Time](https://d65-legionofnerds.github.io/dataanalysis/admin-growth-final.html)** is a companion budget analysis documenting the compensation trends in granular detail using salary compensation reports required to be posted by the state of Illinois ([PA 96-0434](https://www.ilga.gov/Legislation/publicacts/view/096-0434) and [PA 97-0609](https://www.ilga.gov/Legislation/publicacts/view/097-0609)) and [ISBE Annual Financial Reports](https://www.isbe.net/Pages/Annual-Financial-Report.aspx). All three Python scripts used in the analysis are published so that anyone can download the data, run the code, and see exactly how every figure was calculated.

The chart below shows the administrative compensation pool growing in inflation-adjusted dollars over a decade of enrollment decline. This is a structural mismatch that impacts the District's budget crisis.

*From [District 65 Administrative Growth Over Time](https://d65-legionofnerds.github.io/dataanalysis/admin-growth-final.html)*

![D65 Total Admin Compensation Pool — Real 2026 Dollars (FY2012–FY2025)](chart-admin-compensation-pool.jpg)

*Source: [ISBE Annual Financial Reports](https://www.isbe.net/Pages/Annual-Financial-Report.aspx) (AFR), inflation-adjusted to 2026 dollars using [BLS CPI-U](https://www.bls.gov/cpi/). Categories: General Administration, School Administration, Business, Operations. Full methodology: [admin-growth-final.html](https://d65-legionofnerds.github.io/dataanalysis/admin-growth-final.html#methodology-notes)*

The compensation data puts a price on the role growth. While peer districts held per-pupil administrative spending roughly flat in inflation-adjusted terms, D65's rose steadily. This increase was driven not by rising salaries at the top but by the accumulation of positions across the second tier. Notably, the 24 administrators that also maintain a teaching certificate (labeled TRS-enrolled) now carry combined total compensation of approximately $3.74 million annually.

---

## Why This Matters 

The D65 administration claims it has cut itself "to the bone" and this is why remaining budget cuts must now be student-facing, closing schools and cutting positions like school counselors and librarians. Our analysis shows that our district was previously able to operate with a much smaller central office staff. 

The members of the Legion of Data Nerds cross many disciplines but we do not have specific expertise in school district administration. It may take more administrators to run a district now than it did ten years ago. But, the administration has not offered any transparency into the current scope of roles to help clarify this for the community. 

We highlight this information to show another area for potential savings. We are concerned parents who are offering our analytical expertise to the District, Board, and community in service of optimal outcomes for every student. We are ready and willing to partner with the Board and Administration to refine these findings or turn them into meaningful change.

---

## FOIAGras Made This Possible

Tom Hayden maintains a FOIAGras D65 document library including hundreds of board presentations, salary disclosures, budget documents, FOIA responses, and financial reports which served as a primary source foundation for this work. This analysis was powered by AI to query the FOIAGras document library directly and surface information we would not have found manually.

---

*The Legion of Data Nerds is a parent group conducting data-driven accountability work on Evanston/Skokie School District 65 budget and governance. All analyses, data, and code are publicly available at [d65-legionofnerds.github.io](https://d65-legionofnerds.github.io).*
