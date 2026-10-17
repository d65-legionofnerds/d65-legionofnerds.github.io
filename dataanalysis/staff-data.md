---
title: Staff Data
layout: default
parent: Data Analysis
---

# Staff Data Analysis

## District 65 Staff and Teacher Distribution

This analysis examines the distribution of current staff and teachers across District 65. Understanding staffing levels and ratios helps contextualize resource allocation and supports informed discussion about district operations. Some staff are located at multiple locations. For simplicity, staff assigned to multiple locations are excluded. SY 2025 enrollment data is taken from the baseline utilization data table on the D65 School Closure Hub.

This data was scraped from the [D65 Staff Directory](https://www.district65.net/about/contact-us/staff-directory){:target="_blank"} on 12/19/2025. A previous version of these figures were posted on this website based on a scraping of the Staff Directory on 11/30/2025. The District updated the Staff Directory, so new figures were generated to reflect the new data. 

> **Update (October 16, 2026).** The charts on this page describe **SY2025-26** and have not been redrawn. Since then:
>
> - **Kingsley and Dr. Bessie Rhodes closed** at the end of SY2025-26, and Foster School opened. Both closed schools still appear in the charts below.
> - **The District has proposed closing Lincolnwood and Dewey** as part of its October 13, 2026 plan, "A Sustainable Path Forward" ([FOIA Gras doc 24535](https://ig.foiagras.com/api/public/chat/documents/24535/view){:target="_blank"}). That plan also proposes cutting 225.8 more FTE.
> - **The District's staff count fell by 45 FTE this year.** It counted 1,381 FTE in SY2025-26 and 1,335.93 in SY2026-27:
>
> | District FTE count | SY2025-26 | SY2026-27 | Change |
> |---|---:|---:|---:|
> | Certified staff (teachers, specialists, counselors and others in the DEC union) | 761 | 736.93 | −24.07 |
> | Administrators | 51 | 51 | 0 |
> | All other staff | 569 | 548 | −21 |
> | **Total** | **1,381** | **1,335.93** | **−45.07** |
>
> *SY2025-26 from District data published in the* [Evanston RoundTable](https://evanstonroundtable.com/2025/11/02/guest-essay-district-65-employees-enrollment/){:target="_blank"} *(Nov. 2, 2025); SY2026-27 from the District's "FTEs by Employee Category" file (October 2026). The SY2025-26 figures are the District's **count of employees** by category, while SY2026-27 is a **sum of FTE**, so part-time staff count as 1 in the first year and as a fraction in the second; the true change in FTE may be somewhat smaller than 45. The staff directory counts people, including part-time staff and staff listed at more than one location, so its totals are not directly comparable to either.*
>
> **Which "administrators"?** The District's FTE file (used on the [Staff Data](staff-data) page) and the state salary report (used on the [Salary Data](salary-data) page) define the group differently:
>
> | | FTE file (Staff Data) | State report (Salary Data) |
> |---|---|---|
> | Central-office administrators | 23 → 20 | 24 → 21 |
> | Principals and assistant principals | 28 → 31, counted as administrators | 28 → 30, counted separately |
> | IES and other coordinators, union president | Not counted as administrators | 12 → 9, counted as administrators |
> | **Headline** | **51 → 51** | **36 → 30** |
>
> Both show central office down 3. The FTE total holds at 51 because school administrators rose by 3. The salary count falls by 6 because it also includes 3 fewer coordinators and leaves principals out. For what changed in the year Kingsley and Bessie Rhodes closed, see [SY26 to SY27: What Changed](sy26-sy27-changes). For how the administrator count compares with the District's new "36% fewer admins" claim, see the [Admin Growth update](admin-growth-final#october-2026-update-sy2026-27-data-and-the-districts-new-plan).

## Total Staff by Location

<iframe src="assets/total_staff_by_location2.html" width="100%" height="850" frameborder="0"></iframe>

This chart shows the total number of staff members at each District 65 location, including elementary schools, middle schools, and administrative facilities.

## Total Enrollment by Location

<iframe src="assets/total_enrollment_by_location2.html" width="100%" height="850" frameborder="0"></iframe>

This visualization displays student enrollment numbers for each school location in SY 2025, providing context for understanding staffing ratios.

## Elementary School Enrollment

<iframe src="assets/elementary_enrollment_by_school2.html" width="100%" height="850" frameborder="0"></iframe>

Enrollment figures for general education elementary schools in District 65 for SY 2025.

## Elementary School Staff

<iframe src="assets/elementary_staff_by_school2.html" width="100%" height="850" frameborder="0"></iframe>

Total number of staff members at each general education elementary school, including teachers, administrators, support staff, and specialists.

## Elementary School Teachers

<iframe src="assets/elementary_teachers_by_school2.html" width="100%" height="850" frameborder="0"></iframe>

Number of teachers at each general education elementary school. This represents the subset of total staff with teaching positions.

## Staff per 100 Students by Elementary School

<iframe src="assets/elementary_staff_per_100_students_by_school2.html" width="100%" height="850" frameborder="0"></iframe>

This metric normalizes staffing levels by enrollment, showing how many staff members each school has per 100 students. This allows for comparison across schools of different sizes.

## Teachers per 100 Students by Elementary School

<iframe src="assets/elementary_teachers_per_100_students_by_school2.html" width="100%" height="850" frameborder="0"></iframe>

Similar to the staff ratio above, this shows the number of teachers per 100 students at each elementary school, providing insight into classroom teacher availability relative to student population.

## Average Class Size by Elementary School

<iframe src="assets/avg_class_size_fig.html" width="100%" height="850" frameborder="0"></iframe>

This data is taken from the latest [Illinois State Board of Education Report Card Data Set (SY25)](https://www.isbe.net/Pages/Illinois-State-Report-Card-Data.aspx){:target="_blank"}

Calculations for these figures can be viewed in the [interactive Jupyter notebook](dataanalysis/staff_directory_calculations.html).
