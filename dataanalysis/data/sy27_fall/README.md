# SY27 fall enrollment data (snapshot)

Scraped by a Legion member; copied from [jmclip/enrollment_fall26](https://github.com/jmclip/enrollment_fall26), at commit `af552dc` (2026-09-25). Refresh by re-copying these files from that repo, then rerun `../../generate_sy27_charts.py`.

- **Source:** the district's public dashboard, [data.district65.net](https://data.district65.net), pulled 2026-09-23. Planning tables (1A utilization, Cordogan Clark capacity) were transcribed from district screenshots and checked against the February 2022 Cordogan Clark report. Full provenance is in that repo's `sources/sources.md`.
- **Suppression:** the dashboard merges groups under 10 students into "Other*".
- **Estimates:** the dashboard reports enrollment by grade and TWI by school, not by class or by program within a grade. The TWI, ACC and mainstream per-grade splits in `class_size_detail_by_school.csv` are estimates: TWI and ACC evenly spread across K-5, and Washington uses the class counts parents reported.

| File | Contents |
|---|---|
| `enrollment_by_school_grade.csv` | Fall enrollment by school and grade (grade_0 = K) |
| `enrollment_vs_utilization.csv` | SY25 enrollment, SY27 projection (1A table), Cap Total, fall enrollment |
| `utilization_current_vs_predicted.csv` | Capacity used (smaller of Cap Total and Cordogan Clark) and current utilization |
| `twi_strands.csv` | TWE/TWS/TWX by school, TWI seats, strands |
| `class_size_detail_by_school.csv` | Estimated TWI/ACC/mainstream students and sections by school and grade |
| `students_home_demographics.csv` | Dashboard home page by school: IEP, EL, race, grade, TWI, ADA, enrollment |
| `school_summary.csv` | One row per school: enrollment, attendance, IEP, EL, discipline |
| `capacity_cordogan_clark.csv` | District capacity table with Cordogan Clark floor-plan classroom counts (transcribed) |
| `cordogan_clark_2022_report.csv` | Cordogan Clark 2022 report, one row per building: classroom sq ft, teaching stations, capacity |
