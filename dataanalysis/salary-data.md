---
title: Salary Data
layout: default
parent: Data Analysis
---

# Administrative Salary Data Analysis

## Overview

Analyzing administrative staffing and compensation patterns across comparable school districts provides important context for understanding District 65's financial challenges. This analysis examines administrative headcount, total compensation, and per-student metrics to identify potential areas for cost optimization.

## Administrative Headcount Trends

<iframe src="assets/fig_admin.html" width="100%" height="650" frameborder="0"></iframe>

This chart shows the absolute number of administrative staff employed by each district over time. The raw headcount provides a baseline view of administrative staffing levels, though it should be interpreted alongside enrollment data for meaningful comparison.

## Administrative Headcount per 1,000 Students

<iframe src="assets/fig_admin_per_1000.html" width="100%" height="650" frameborder="0"></iframe>

Normalizing administrative headcount by enrollment allows for fair comparison across districts of different sizes. This metric reveals the administrative staffing ratio relative to student population. Districts with higher values employ more administrators per student, which directly impacts per-student spending on administration.

### Key Observations

When comparing administrative staffing ratios, it's important to note that significant variation exists among peer districts. Districts with lower ratios demonstrate that similar sized school systems can operate effectively with leaner administrative structures.

## Total Administrative Salary Expenditure

<iframe src="assets/fig_admin_salary.html" width="100%" height="650" frameborder="0"></iframe>

This visualization tracks total administrative salary spending over time. While absolute spending naturally correlates with district size, the trajectory of spending growth provides insight into budgetary priorities and cost management.

## Administrative Salary per 1,000 Students

<iframe src="assets/fig_admin_salary_per_1000.html" width="100%" height="650" frameborder="0"></iframe>

Normalizing administrative salary expenditure by enrollment enables direct comparison of administrative cost efficiency across districts. This metric indicates how much each district spends on administrative personnel per 1,000 students, controlling for differences in district size.

### Analysis

Districts with lower per-student administrative costs demonstrate that effective oversight and management can be achieved with more efficient resource allocation. The variation across comparable districts suggests opportunities exist for cost optimization while maintaining educational quality.

## Estimated Excess Administrative Cost

<iframe src="assets/fig_extra_admin.html" width="100%" height="1000" frameborder="0"></iframe>

### Methodology

This analysis calculates the potential cost difference if each district's administrative staffing ratio matched the average across all peer districts. The calculation:

1. Determines the average administrative headcount per 1,000 students across all districts
2. Applies this ratio to each district's enrollment
3. Multiplies the difference in headcount by each district's average administrative salary
4. Results shown as positive (above average) or negative (below average) values

### Interpretation

District 65 shows the highest opportunity for admin cost savings compared to peer districts if staffing levels were adjusted to match peer norms.

This metric provides a data-driven framework for evaluating whether administrative staffing levels align with comparable districts. It should be considered alongside other factors such as district-specific needs, programmatic requirements, and operational complexity.

## Implications for Financial Planning

The data presented here offers context for discussions about cost management strategies. While administrative positions serve important functions, the significant variation in staffing ratios and costs among peer districts suggests that different organizational models can effectively serve similar student populations.

When evaluating budget reduction strategies, comparing administrative cost structures to peer districts provides an objective benchmark. Districts operating above peer averages in administrative spending per student may have opportunities to achieve cost savings through organizational efficiency without necessarily impacting classroom instruction.

---

*Calculations for these figures can be viewed in the [interactive Jupyter notebook](calculations.html).*
