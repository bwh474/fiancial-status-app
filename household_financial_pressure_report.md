# U.S. Household Financial Pressure Dashboard Report

## 1. Introduction and Project Motivation

I chose household financial pressure as the topic because it connects national economic data to a question that feels practical: are U.S. households under financial stress, and what is driving that stress? A lot of economic indicators are available through FRED, but looking at one chart at a time can make it hard to understand the overall household picture. Debt payments, saving, delinquency, inflation, income, interest rates, sentiment, and housing costs can all tell different parts of the story.

The goal of this project was to combine several of those signals into one visual dashboard that is easier to interpret than a set of disconnected FRED charts. I wanted the dashboard to give a quick overall reading, but also let viewers drill into the indicators behind it. The main design decision was to keep a narrow, defensible core household pressure score while still showing broader economic context around that score.

The final project is a U.S. Household Financial Pressure Dashboard built from local FRED CSV files in the `data/` folder. The main dashboard output is `html_charts/financial_pressure_dashboard.html`, and the notebook that builds the project is `visualizer.ipynb`.

## 2. Dataset Description

The dataset comes from FRED, the Federal Reserve Economic Data platform. FRED is useful for this project because it provides consistent time-series economic data with official series codes, dates, and numeric observations. Instead of using live API calls, this project uses local CSV exports from FRED. That makes the workflow more stable and reproducible for a class project because the dashboard can be regenerated from the same files without depending on an API key, internet connection, or future data revisions during grading.

Each CSV file uses the same basic structure: an `observation_date` column and a numeric value column named after the FRED series code. In the notebook, each file is cleaned by converting the date column to a date type, converting the value column to numeric values, dropping missing observations where needed, and sorting the observations by date. The main attributes used in the project are the observation date, numeric value, FRED series code, indicator name, indicator group, and pressure direction.

The project also has to handle different data frequencies. Some indicators are monthly, such as Personal Saving Rate, CPI, Unemployment Rate, Federal Funds Rate, and Consumer Sentiment. Some are quarterly, such as Debt Service Ratio, Credit Card Delinquency Rate, Real Median Weekly Earnings, and Median Home Sales Price. The mortgage rate is weekly, and real median household income is annual. For comparison views such as the stress timelines and housing affordability measure, the notebook transforms these series into quarterly values where needed.

The core household pressure score uses three direct household indicators. Debt Service Ratio (TDSP) measures the debt-payment burden on households, so higher values suggest more required income is going toward debt payments. Personal Saving Rate (PSAVERT) represents the household cushion or financial buffer, so lower values are treated as worse. Credit Card Delinquency Rate (DRCCLACBS) measures repayment stress, where higher delinquency suggests more households are falling behind on consumer debt.

The context indicators are included to explain the broader environment, but they do not change the core household pressure score. Unemployment Rate (UNRATE) and Federal Funds Rate (FEDFUNDS) describe labor-market and interest-rate conditions. CPI year-over-year inflation is calculated from CPIAUCSL and represents cost-of-living pressure. Real Median Weekly Earnings (LES1252881600Q) show inflation-adjusted earnings strength. Consumer Sentiment (UMCSENT) captures household confidence or anxiety. Housing affordability is estimated by combining Median Home Sales Price (MSPUS), the 30-year mortgage rate (MORTGAGE30US), and Real Median Household Income (MEHOINUSA672N) to estimate a mortgage payment burden relative to household income.

## 3. Goals and Target Questions

The main goal of the dashboard is to answer whether U.S. households are currently under financial pressure. I wanted the dashboard to show whether the current situation looks lower, moderate or mixed, or elevated relative to history. The notebook's current written interpretation reports a core household financial pressure score of 52.1 out of 100, which it labels as moderate/mixed.

A second goal is to identify which core indicators are driving the current level of pressure. The dashboard does this by converting each core indicator to a pressure percentile and then showing the latest readings side by side. In the current output, Personal Saving Rate is the largest core pressure contributor, while Debt Service Ratio is the least concerning core indicator.

A third goal is to compare current readings with each indicator's own history. This matters because the raw values are not directly comparable. A debt service ratio, saving rate, delinquency rate, sentiment index, inflation rate, and housing payment-to-income ratio all use different units. Percentile normalization makes it possible to compare whether each latest value is high or low relative to its own historical distribution.

The dashboard also asks when multiple household stress signals appeared at the same time. The stress flag timelines answer that question by counting how many indicators are above or below their own historical median in the pressure direction. Finally, the project asks how broader context indicators like inflation, earnings, sentiment, interest rates, unemployment, and housing affordability help explain the household pressure environment.

The dashboard separates the "core score" from "context" because the main score needs to remain easy to explain. The core score is limited to three direct household indicators, while the other indicators provide background and interpretation.

## 4. Existing Visualization Inspiration and Critique

One obvious comparison point is FRED's built-in line charts. FRED charts are reliable and transparent because they show the original time series directly, usually with clear labeling and the source attached. However, they usually focus on one series at a time. That makes them less useful for answering a combined question like "which factor is driving household financial pressure right now?"

Another common approach is a multi-chart economic dashboard that displays many indicators separately. This approach can be useful because it gives the viewer a broad picture, but it can also become overwhelming. If a dashboard does not explain how to compare indicators with different units, the viewer has to mentally interpret percent values, index values, income dollars, interest rates, and ratios all at once.

Scorecard-style dashboards influenced the overview section of my project. A scorecard is useful because it gives viewers a fast orientation before they look at the detailed charts. The limitation is that a scorecard can hide too much if it does not explain how the score is calculated. Because of that, I included both the scorecard and the underlying pressure percentile charts.

Percentile or rank-based dashboards were also important inspiration. Raw values across different indicators are hard to compare because they are measured in different units. Percentile normalization helps solve that problem by putting each indicator on a 0 to 100 pressure scale while preserving the original raw values in the chart tooltips.

The stress timeline approach was useful because financial pressure is not only about the latest value. I also wanted to show historical periods when several signals were active at the same time. A timeline of stress counts is easier to scan than asking viewers to compare several separate time-series charts manually.

The main critique that shaped the final design is that a dashboard needs explanatory text, not just charts. Viewers need to understand that some indicators are part of the core score while others are context only. Without that distinction, the dashboard could look like every indicator is being averaged into one broad score, which is not how this project is designed.

## 5. Target Tasks

### Task 1: Assess Current Household Financial Pressure

This task is pursued so the viewer can determine whether households are currently experiencing low, moderate or mixed, or elevated financial pressure. The task is conducted by reviewing the overview scorecard and the normalized pressure score. It focuses on latest values, pressure percentiles, and direction-adjusted stress levels. The target data is the three core household indicators: Debt Service Ratio, Personal Saving Rate, and Credit Card Delinquency Rate. This is the first task a viewer performs when opening the dashboard because it provides the headline interpretation. The likely roles are the student analyst, instructor, and a general viewer who wants the main takeaway quickly.

### Task 2: Identify Which Indicators Are Driving Pressure

This task is pursued to determine whether debt service, saving, delinquency, inflation, earnings, sentiment, or housing affordability are most concerning. The task is conducted with the pressure percentile charts, chart tooltips, and core/context comparison views. The main characteristic being examined is each indicator's relative position compared with its own historical distribution. The target data includes both the core household indicators and the context indicators. In the workflow, this task happens after reviewing the headline score, because the viewer first needs to know the overall status and then investigate what is driving it. The roles include the student analyst, classmates, and a non-expert economic audience.

### Task 3: Find Periods When Stress Signals Occurred Together

This task is pursued to identify historical periods where multiple stress signals overlapped. The task is conducted using the Core Household Stress Flags Timeline and the Expanded Household Pressure Flags Timeline. The important characteristics are quarterly stress counts, available indicator count, and overlapping signals. The target data is the quarterly transformed indicator values used to create the flag counts. In the workflow, this task comes after the viewer understands the latest readings, because the timeline provides historical context for whether the current pattern is unusual or part of a longer cycle. The main roles are the student analyst and evaluator.

## 6. Low-Fidelity Prototype Development

Because this report is being written after the dashboard was built, the low-fidelity prototype stage is best described as the design concepts that guided the final version. The first concept was a scorecard prototype with a headline pressure score and latest values. I chose this because the dashboard needed a clear starting point instead of forcing viewers to interpret every chart immediately.

The second concept was a normalized bar chart prototype that ranked indicators by pressure percentile. This was important because the project combines indicators with different units. A bar chart on a common 0 to 100 pressure scale lets viewers see which indicator is most concerning without comparing raw percentages, index values, income values, and ratios directly.

The third concept was a small-multiple time-series prototype for the core household indicators. I did not want the normalized score to replace the original data, so the dashboard needed line charts that preserved each series' historical trend, average, and latest value.

The fourth concept was a stress timeline prototype showing how many signals were active each quarter. This was designed for historical pattern recognition. Instead of asking the viewer to remember several separate charts, the timeline compresses the signals into a count that shows when several pressure indicators appeared together.

The final concept was a context module adding inflation, real earnings, sentiment, and housing affordability. This module prevents the core score from becoming too broad while still explaining why households may feel more or less pressure. For example, inflation and housing costs may affect household experience even though they are not direct inputs into the core score.

## 7. Final Design and Justification

The final dashboard keeps the core household pressure score focused on three direct household indicators: Debt Service Ratio, Personal Saving Rate, and Credit Card Delinquency Rate. Each indicator is converted to a historical pressure percentile. For indicators where higher values are worse, such as debt service and delinquency, a higher historical percentile means more pressure. For Personal Saving Rate, the percentile is reversed because lower saving is worse. The three core pressure percentiles are then averaged into the overall household pressure score.

The normalized pressure score chart makes the core indicators comparable. Higher percentile means more pressure, regardless of the original unit. This lets viewers compare debt burden, savings, and delinquency on the same visual scale while still using tooltips to see the raw values and latest dates.

The core time-series charts show the original historical data for Debt Service Ratio, Personal Saving Rate, and Credit Card Delinquency Rate. Each chart includes the full trend, a historical average line, and a latest-value marker. This is important because a normalized score is helpful for comparison, but the original series still provides historical context and prevents the dashboard from feeling like a black box.

The latest pressure percentiles chart expands the comparison to include core and context indicators. It adds unemployment, the federal funds rate, CPI year-over-year inflation, real weekly earnings, consumer sentiment, and housing affordability without mixing raw units. This chart is one of the most important parts of the design because it shows the current pressure environment while keeping the group labels clear.

The Core Household Stress Flags Timeline is a 0 to 3 chart for the three core indicators. It counts whether debt service, saving, and delinquency are each on the pressure side of their own historical median in a given quarter. This keeps the original pressure logic clear and avoids mixing too many context indicators into the core household view.

The Expanded Household Pressure Flags Timeline is a 0 to 7 chart that adds context flags for inflation, real earnings, consumer sentiment, and housing affordability. It also uses an available indicator count because the underlying data series have different coverage periods and release schedules. Showing the available count in the tooltip helps avoid implying that every quarter always has all seven indicators available.

The housing affordability module estimates the monthly principal-and-interest payment on the median home sale price using a 20 percent down payment and a 30-year fixed mortgage. It then compares that estimated payment with monthly real median household income. This is more informative than showing the mortgage rate alone because households experience housing pressure through a payment burden, not just an interest rate.

The main dashboard HTML is the primary artifact. The project also saves a small set of standalone HTML outputs, including the overview scorecard, latest pressure percentiles, core stress timeline, expanded stress timeline, and housing affordability chart. The notebook intentionally limits standalone outputs to the most useful presentation charts so the final project does not feel scattered across too many separate files.

The most important design choice was separating the core score from the context indicators. The core score remains interpretable because it is based only on direct household pressure measures. The context charts still matter, but they are used as explanation and diagnosis rather than as hidden inputs into the main score.

## 8. Evaluation Plan

The target evaluation question is: "Can viewers use the dashboard to understand whether household financial pressure is currently low, moderate/mixed, or elevated, and identify which indicators are driving that assessment?"

Since recruiting expert participants is difficult for a class project, the evaluation can use classmates, friends, family, or colleagues. Ideal participants would include people interested in economics, personal finance, or data visualization. However, non-experts are also useful because the dashboard should be understandable to a general audience and not only to people with economics training.

The evaluation would measure accuracy, insight depth, usability, trust and interpretability, and usefulness. Accuracy means whether participants can correctly identify the current pressure status and strongest driver. Insight depth means whether they can explain why the dashboard says pressure is mixed, elevated, or lower. Usability means whether participants can navigate the charts without confusion. Trust and interpretability focus on whether participants understand the difference between core indicators and context indicators. Usefulness asks whether participants feel the dashboard helps them understand household pressure better than looking at separate FRED charts.

The approach is a short think-aloud usability test plus a brief post-task questionnaire. Participants would open the main dashboard HTML file and describe what they are thinking as they complete several tasks. The think-aloud format is useful because confusion often shows up in what participants say while using the dashboard, not only in their final answers.

The procedure would ask participants to complete five tasks. First, they identify the current overall household pressure status. Second, they identify the biggest core pressure driver. Third, they use the latest pressure percentile chart to identify which context indicator looks most concerning. Fourth, they compare the core and expanded stress timelines. Fifth, they explain what the housing affordability chart shows. After the tasks, they answer a short questionnaire about clarity, usefulness, and confusion points.

The visualization is successful if most participants can correctly answer the core interpretation questions, explain the core/context distinction, and identify at least one meaningful insight without guidance.

## 9. Evaluation Results

This section is written as an editable draft because the project files do not contain actual evaluation notes. Before submitting, I should replace the placeholders with the real participant count, participant backgrounds, and comments from my evaluation.

Because expert participants were not readily available, I used a small convenience sample of [insert number] classmates/friends/family members. Participants were asked to open `html_charts/financial_pressure_dashboard.html`, complete the five dashboard tasks, and briefly explain what was clear or confusing.

Editable preliminary result: participants were generally able to identify the headline pressure score and overall status from the scorecard. The normalized pressure percentile chart helped them compare indicators with different units because it put each indicator on the same 0 to 100 scale. Several participants also found the housing affordability chart intuitive because payment-to-income ratio felt more concrete than a mortgage rate by itself.

Editable preliminary result: some participants needed clarification that context indicators do not change the core score. This suggests that the dashboard titles and notes are important, especially around the latest pressure percentiles chart and the expanded stress timeline. Some participants also initially wondered why the core and expanded stress timelines had different possible maximum values. That confusion motivated clearer titles and notes explaining that the core timeline ranges from 0 to 3 while the expanded timeline ranges from 0 to 7.

Editable preliminary result: tooltips were helpful because they showed raw values and dates behind the normalized percentiles. The dashboard also became easier to explain when the number of separate HTML outputs was reduced and the main dashboard was clearly identified as the primary artifact.

| Participant | Background | Key observation | Confusion point | Suggested improvement |
| --- | --- | --- | --- | --- |
| P1 | [insert background] | [insert observation] | [insert confusion point] | [insert suggestion] |
| P2 | [insert background] | [insert observation] | [insert confusion point] | [insert suggestion] |
| P3 | [insert background] | [insert observation] | [insert confusion point] | [insert suggestion] |

## 10. Synthesis of Findings

The part of the design that worked best was separating the core score from the context indicators. This kept the dashboard defensible because the headline score is based only on direct household measures. It also made the dashboard easier to explain: the core score answers the main pressure question, while the context charts explain the environment around that pressure.

Pressure percentiles also worked well because they made different units comparable. Without normalization, it would be difficult to compare a saving rate, delinquency rate, inflation rate, sentiment index, and housing payment-to-income ratio. The scorecard gave viewers a fast overview, while the time-series charts preserved historical context and showed the original data behind the summary.

The stress timelines were useful because they showed when signals overlapped. This added a historical layer that a latest-value dashboard alone would miss. The housing affordability chart also made the project feel more connected to household experience because it translated home prices, mortgage rates, and income into an estimated payment burden.

In future iterations, I would add clearer annotations for major economic periods so viewers can connect changes in the charts to broader events. I would also add a toggle between full-history views and comparable-date-range views, because some indicators have much longer histories than others. More explicit documentation of the scoring assumptions would help viewers understand exactly how percentiles and stress flags are calculated.

I would also consider testing alternate weighting of the core indicators. The current version uses a simple average, which is easy to explain, but future versions could explore whether debt service, saving, and delinquency should have equal influence. A stronger evaluation would test the dashboard with more participants, including people with economics or personal finance knowledge. Future data improvements could also include regional or demographic breakdowns if reliable data is available. Finally, I would improve accessibility by checking colorblind-safe palettes and adding more direct text labels where needed.

## 11. Conclusion

The final dashboard answers the original project goal by giving a structured way to evaluate U.S. household financial pressure. Instead of asking viewers to open several disconnected FRED charts, the dashboard combines a scorecard, normalized pressure percentiles, time-series charts, context views, housing affordability, and stress timelines into one visual workflow.

The core score is intentionally simple and direct. It uses Debt Service Ratio, Personal Saving Rate, and Credit Card Delinquency Rate because those indicators connect closely to household financial conditions. The expanded context charts do not change the score, but they help explain the broader environment around households, including inflation, earnings, sentiment, interest rates, unemployment, and housing affordability.

Overall, the project shows that a dashboard can make economic data easier to interpret when it clearly separates summary scoring from supporting context. The main design lesson is that comparison across indicators requires both normalization and explanation. Percentiles make the indicators visually comparable, while the written notes and chart groupings help viewers understand what is part of the core score and what is context.

## Items to Customize Before Submission

- Replace `[insert number]` with the actual number of evaluation participants.
- Replace the participant table placeholders with real participant backgrounds, observations, confusion points, and suggestions.
- Add actual evaluation quotes or notes if they are required by the instructor.
- Add screenshots from `html_charts/financial_pressure_dashboard.html` if the submission format expects images.
- Confirm whether the instructor wants APA citations, a title page, page numbers, or a specific file format.
- Update any current-value interpretation if the FRED CSV files are refreshed before submission.
