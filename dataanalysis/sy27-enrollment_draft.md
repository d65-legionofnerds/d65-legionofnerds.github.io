---
title: SY27 Enrollment
layout: default
nav_exclude: true
search_exclude: true 
---

# SY 2026-27 Enrollment Analysis

**Fall enrollment** comes from the district's public dashboard, [data.district65.net](https://data.district65.net), pulled September 23, 2026. It was collected and analyzed by Jean for the Legion ([full analysis and source files](https://github.com/jmclip/enrollment_fall26)). **Projections** are the district's Scenario 1A (Kingsley closed) utilization table. The fall dashboard doesn't report low income, middle school Dual Language or permissive transfers. Those sections still use the [District 65 memo to the School Board](https://d65-legionofnerds.github.io/dataanalysis/data/sy27_enrollment/) of May 18, 2026 (registrations as of May 12), and each chart says which source it uses.

## Enrollment vs. Projections

<iframe src="assets/sy27_enrollment_vs_projection.html" width="100%" height="580" frameborder="0"></iframe>

Across all 14 schools, fall enrollment is **5,462 against 5,690 projected: 228 students (4.0%) below the district's plan**. Seven schools came in below projection: Foster (−91), Nichols (−74), Haven (−60), Dewey (−57), Washington (−54), Dawes (−49) and Oakton (−36). Five of the seven host TWI programs. Seven came in above: Lincolnwood (+51), Chute (+40), King Arts (+30), Orrington (+25), Lincoln (+22), Walker (+13) and Willard (+12).

Nearly every school gained students between the May registration count and the fall (5,108 → 5,462 in total; Chute and Haven were flat). Foster's shortfall shrank from about 136 to 91, but it is still the largest.

*Jean's write-up puts the gap at −61. It uses projections of 181 for Lincolnwood and 193 for Willard, taken from a capacity table built on a scenario that kept Kingsley open. Kingsley's 167 projected students aren't among the 14 schools here, so under that scenario the projected total is lower. Scenario 1A, the plan the district adopted, projects 280 and 261.*

| School | SY25 Actual | SY27 Projected (1A) | May Registered | Fall Enrolled | vs. Projection |
|---|---:|---:|---:|---:|---:|
| **Elementary** | | | | | |
| Dawes Elementary | 294 | 337 | 260 | 288 | −49 |
| Dewey Elementary | 316 | 372 | 285 | 315 | −57 |
| Lincoln Elementary | 334 | 328 | 301 | 350 | +22 |
| Lincolnwood Elementary | 283 | 280 | 310 | 331 | +51 |
| Oakton Elementary | 361 | 403 | 327 | 367 | −36 |
| Orrington Elementary | 218 | 226 | 234 | 251 | +25 |
| Walker Elementary | 345 | 304 | 287 | 317 | +13 |
| Washington Elementary | 403 | 441 | 348 | 387 | −54 |
| Willard Elementary | 345 | 261 | 246 | 273 | +12 |
| Foster School *(new)* | — | 452 | ~316 † | 361 | −91 |
| **Magnet / Choice** | | | | | |
| Dr. MLK Jr. Literary & Fine Arts | 415 | 415 | 428 | 445 | +30 |
| **Middle** | | | | | |
| Chute Middle School | 567 | 551 | 591 | 591 | +40 |
| Haven Middle School | 642 | 664 | 603 | 604 | −60 |
| Nichols Middle School | 609 | 656 | 572 | 582 | −74 |
| **Closed** | | | | | |
| Kingsley Elementary | 326 | — | — | — | — |
| Dr. Bessie Rhodes | 251 | — | — | — | — |
| **Total (14 open schools)** | | **5,690** | **5,108** | **5,462** | **−228** |

*† Several of Foster's May counts were reported as "<10" and were back-calculated.*

## Building Utilization

<iframe src="assets/sy27_building_utilization.html" width="100%" height="580" frameborder="0"></iframe>

Utilization is fall enrollment divided by capacity. For capacity we use the smaller of the district's Cap Total and Cordogan Clark's 2022 capacity study, the same rule Jean uses. That lowers capacity at Dewey, Oakton and Willard. **No school exceeds 83%.** Nichols MS (83%), Oakton (79%) and Lincolnwood (77%) are the most utilized. Willard (51%), Orrington (58%) and Dewey (59%) are the least. Across the 14 schools, 68% of seats are filled.

## Total Enrollment by School and Program

<iframe src="assets/sy27_enrollment_by_program.html" width="100%" height="580" frameborder="0"></iframe>

The fall dashboard reports each school's grade enrollment and its TWI (Two Way Immersion) students by type: TWE, TWS and TWX. It doesn't break out ACC (African Centered Curriculum), middle school Dual Language, RISE or STEP, so those are included in the blue bars.

## Class Size Concerns: DEC Contract Limits

The District 65 teachers' union (DEC) contract sets maximum class sizes: **K-2: 23 students, 3-5: 25 students, 6-8: 28 students**. Several schools have monolingual grade enrollments that either exceed or sit just below these limits. That creates a difficult choice: one oversized class that violates the contract, or two undersized classes that strain staffing resources.

**These are estimates.** The dashboard gives each grade's total and each school's TWI total, but not the TWI or monolingual count per grade. Following Jean's method, TWI students are spread evenly across K-5 and subtracted from each grade (and Oakton's 73 projected ACC students the same way). Washington uses the class counts parents reported. Jean's own class-size estimates use the district's 24-student capacity standard rather than the DEC limits used here.

<iframe src="assets/sy27_class_size_dilemma.html" width="100%" height="530" frameborder="0"></iframe>

Red bars show the class size as a single section (exceeding the DEC limit). Blue bars show the class size if split into the minimum sections needed to comply. In many cases, splitting creates classes of just 12-15 students, potentially too small to justify the staffing cost. Key examples:

- **Dawes** has an estimated 24 monolingual kindergartners, 26 1st graders and 29 3rd graders. Each would split to 12-15 per class.
- **Dewey** kindergarten (31) and 2nd grade (28) split to 15.5 and 14.
- **Oakton** grades 1 (30) and 3 (29) split to 15 and 14.5.
- **Orrington** grade 4 (27) splits to 13.5.
- **Washington** kindergarten (29) and 4th grade (31) split to about 15.

Dawes grade 2 (23) sits exactly at the K-2 max, and Foster grade 4 (24) sits one under the 3-5 max.

<iframe src="assets/sy27_class_size_elementary.html" width="100%" height="930" frameborder="0"></iframe>

Detailed view for each elementary school. The red dashed line is the DEC contract maximum for that grade band. Red bars exceed the limit; orange bars are within 15% of it. For real class counts, parents are reporting class sizes through [Jean's crowdsourcing form](https://docs.google.com/forms/d/e/1FAIpQLSepZPKRXOA8HTbEoWf8sUmXK_UlhWkK4_6y4cl9NQLNEYL1Bw/viewform?usp=dialog).

## Middle School: Dual Language Enrollment (May memo)

<iframe src="assets/sy27_middle_school_detail.html" width="100%" height="430" frameborder="0"></iframe>

*The fall dashboard doesn't break out middle school Dual Language, so this section still uses May registrations. The dashboard's TWI counts cover only the five elementary TWI schools.*

Haven's Dual Language middle school program appears significantly underenrolled, with fewer than 10 students in 7th grade and 12 in 8th grade. At Nichols, 39 6th graders in the DL program likely fill two classes of about 20, which aligns with projections. Chute has no DL program. These low DL numbers at Haven are worth scrutiny given the district's stated goal of expanding class sizes elsewhere to manage costs.

## TWI Program Enrollment

<iframe src="assets/sy27_dl_twi_enrollment.html" width="100%" height="480" frameborder="0"></iframe>

The five elementary TWI schools enroll 686 TWI students in 1,008 TWI seats, **68% full**. Dawes is the fullest (79%). Oakton is the emptiest at 52%, or about 12.5 students per TWI classroom. Foster (200) and Washington (195) run two strands each and carry the largest programs, but both are below 70% of their TWI seats.

## Student Demographics

<iframe src="assets/sy27_demographics.html" width="100%" height="580" frameborder="0"></iframe>

Racial composition varies substantially across schools. Willard (72% White), Lincolnwood (62%), Orrington (61%), Haven (53%) and Lincoln (50%) are half or more White. Foster is 36% Black and 44% Hispanic/Latino. King Arts (41%) and Oakton (40%) have the highest shares of Black students, and Washington (39%) has the second-highest share of Hispanic/Latino students. The dashboard hides any group under 10 students at a school (it's folded into "Other*"), so small groups such as Asian students at Foster, Lincolnwood, Washington and Willard don't appear.

## English Learners, IEPs, and Low Income

<iframe src="assets/sy27_el_iep_lowincome.html" width="100%" height="530" frameborder="0"></iframe>

Foster has the highest share of English Learners (29%), followed by Washington (24%) and Dawes (23%). King Arts has the highest IEP rate (28%). Lincolnwood and Willard have markedly fewer English Learners (4% each), and Willard and Orrington have the lowest IEP rates (11-12%). Low income isn't on the fall dashboard. In the May memo, Foster had the highest rate (65%), and Lincolnwood, Willard and Orrington were lowest.

## Permissive Transfers (May memo)

<iframe src="assets/sy27_transfer_sankey.html" width="100%" height="630" frameborder="0"></iframe>

Of 268 confirmed permissive transfers, Foster accounted for 100 outgoing (37%). Lincolnwood was the top destination with 53 incoming, followed by Walker and Willard at 39 each. The district notes that 49% of all transfers were families seeking to remain at their current school after boundary changes, not families choosing to leave. Lincolnwood's +51 over projection is consistent with it being the top destination.

## Kindergarten

<iframe src="assets/sy27_kindergarten.html" width="100%" height="480" frameborder="0"></iframe>

In May, kindergarten registrations were down 34% from the same point the year before (157 vs. 238). The district attributed this to registration opening later (February 1 instead of the usual December 1), the complexity of the new school-assignment process and staff reductions. Most of that gap closed by the fall. **534 kindergartners are enrolled against 604 projected (−70, −12%).** Foster accounts for more than half the shortfall: 46 enrolled vs. 84 projected. Oakton and King Arts hit their projections exactly, and Lincolnwood came in two over.

---

*Fall data: District 65 public dashboard, pulled 2026-09-23, via [jmclip/enrollment_fall26](https://github.com/jmclip/enrollment_fall26) ([snapshot used here](data/sy27_fall/)). Projections: district Scenario 1A utilization table. Capacity: smaller of the district's Cap Total and Cordogan Clark's February 2022 capacity study. May data: District 65 SY 2026-27 Projected Enrollment Update memo, May 18, 2026; values reported as "<10" were back-calculated from row totals where possible ([raw data](data/sy27_enrollment/)). Class sizes and per-grade program splits are estimates, not district counts.*
