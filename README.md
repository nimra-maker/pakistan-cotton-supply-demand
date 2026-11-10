# Pakistan Cotton Supply and Demand: 2026/27 Scenario Analysis

A small research project on Pakistan's cotton supply and demand. I built it to learn the sector and to practise checking data, building a balance sheet, and testing scenarios.

Author: Nimra Shahab

## What I found

- Pakistan's cotton production peaked at about 8.2 million bales in 2017/18. USDA's 2026/27 forecast is about 5 million, roughly 39% lower.
- Mills use about 10 million bales a year, so imports fill the gap. Imports were about 31% of mill use in 2017/18 and are forecast at about 50% in 2026/27.
- I tested five scenarios on the 2026/27 forecast:

| Scenario | Yield change | Production (1,000 bales) | Imports needed (1,000 bales) |
|---|---|---|---|
| Base (USDA forecast) | 0% | about 5,000 | about 5,100 |
| Bad weather | -15% | about 4,250 | about 5,850 |
| Pest outbreak | -10% | about 4,500 | about 5,600 |
| Severe (heat + floods, area -5%) | -20% | about 3,800 | about 6,300 |
| Good season | +10% | about 5,500 | about 4,600 |

- The risk is lopsided: a bad year adds 500 to 1,200 thousand bales of imports, while a good year saves only about 500.
- I compared USDA with the Pakistan Economic Survey for 2015/16 to 2023/24. The two move together (correlation about 0.97), but USDA's production is lower in 8 of 9 years, typically by about 10%. So my levels may be conservative, while the trends hold.

## Files

| File | What it is |
|---|---|
| `Pakistan_Cotton_Scenario_Summary.pdf` | One-page summary of the analysis |
| `pakistan_cotton_model.xlsx` | The model: data, checks, chart, scenarios and the USDA vs Economic Survey cross-check |
| `check_psd.py` | Python script that checks a USDA download and logs revisions |
| `psd_cotton.csv` | The USDA PSD download used (Cotton, Pakistan, 2015/16 to 2026/27) |
| `cotton_data_checks.ipynb` | Colab notebook where I ran the script |

## How the data is checked

Before using the data I test that:

1. Beginning stocks + production + imports equals total supply.
2. Exports + domestic use + loss + ending stocks equals total distribution.
3. Each year's ending stocks equal the next year's beginning stocks.
4. Production x 217.72 kg per bale / area matches the yield column (within rounding).
5. The stocks-to-use percentage can be recomputed.

All five pass on the current download.

## How to run the script

1. Put `check_psd.py` and `psd_cotton.csv` in the same folder (or upload both to Google Colab).
2. Install pandas if needed: `pip install pandas`
3. Run: `python check_psd.py` (in Colab: `!python check_psd.py`)

It prints PASS or FAIL for each check and saves `psd_checked.csv`. If you also add last month's download named `psd_cotton_previous.csv`, it prints a revision log of every value that changed and any new years.

## Method notes

- USDA uses 480-lb bales (217.72 kg). Pakistan's official reports use a 170 kg bale, which I confirmed from the Economic Survey's own yield, area and production figures. I convert USDA bales to 170 kg bales when comparing.
- Scenario formula: imports needed = mill use + exports + ending stocks - beginning stocks - production. Production = area x yield, converted to bales.
- Shock sizes come from how much yield has varied in the data (the standard deviation is about 14% of the average) and from real cases such as the 2022 floods and the 2024 heat and pest losses. The probabilities are my own judgment.

## Limits

- Mill use, exports and ending stocks are held fixed. Prices and policy are not modelled.
- Shock sizes and probabilities are my judgment, not forecasts.
- The latest year is a USDA forecast and will be revised.
- The cross-check covers 2015/16 to 2023/24. Checking 2024/25 onward is a next step.
- USDA uses a market year and the Economic Survey uses a July to June fiscal year, so small timing differences are possible.

## Sources

- USDA Foreign Agricultural Service, PSD Online (Cotton, Pakistan), downloaded November 2026
- Pakistan Economic Survey 2023-24, Chapter 2 Agriculture (Pakistan Bureau of Statistics). The 2023/24 figures are provisional.
- Pakistan Economic Survey 2022-23 and press reports on the 2022 floods and the 2024 season

## How I worked

I used an AI assistant as a tutor and for drafting. I checked the numbers against USDA and the Economic Survey, and I can explain every formula and step in this project.

## Next steps

- Add textile and made-ups export values and cotton prices for the same years
- Extend the cross-check to 2024/25 onward
- Add a Power BI report page
