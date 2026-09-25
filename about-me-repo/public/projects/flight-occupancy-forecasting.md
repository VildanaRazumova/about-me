---
title: "How early can you predict how full a charter flight will be? (Master's thesis)"
short_name: Master's thesis
summary: Forecasting the share of seats sold on charter flights at different points before departure, to find how early a forecast becomes reliable
kind: thesis
company: GISMA University of Applied Sciences (Master's thesis on real booking data of a B2B tour operator; the data itself is confidential)
status: defended; dissertation and defence graded 96 out of 100
role: author
skills: [Python, scikit-learn, Random Forest, XGBoost, LightGBM, time-series validation, feature engineering]
evidence: []
---

## Situation and task
Tour operators commit to charter seats months before departure, without knowing the real demand. The research question: how early can an operator reliably forecast how full a flight will be?

## What I did
- Chose a forecast target that still carries information, although many flights sell out completely (right-censoring).
- Rebuilt each flight's booking curve from booking records, as no historical snapshots existed.
- Tested whether external signals help at all (currency rates, search interest, holidays, news sentiment scored by an LLM) by comparing the model with and without them (an ablation test).
- Compared several model families at two forecast points.

### Key decisions
- No future information may leak into the model: a strictly time-based split, validation that moves forward in time, feature selection on training data only.
- A strong simple baseline next to the naive one, to prove the model adds real value.

## Result
- Graded 96 out of 100 (dissertation and defence).
- Best model: tuned Random Forest 60 days before departure, error (RMSE) about 15 percentage points of load, R² 0.50.
- The best model beats the strong simple baseline by about 5%: most of the signal is in the current booking state.
- 90 days before departure the models barely beat the average, so 60 days is the earliest reliable forecast window.
- External signals added no measurable value.
- Business recommendation: two-layer pricing (ML forecast plus rules), later the basis of her work on price recommendations.

## What I learned
- A strong simple baseline is the honest test of a model; a small gain over it is a finding too.

## Examiner feedback (August 2026)
> "This dissertation represents a solid standard of Master's-level research. Vildana tackles a complex, noisy, real-world dataset from the B2B charter tourism industry. A major highlight is her high-level analytical maturity in diagnosing the right-censoring constraint […] and successfully pivoting the target variable to a 30-day pre-departure load factor. The methodology is executed with precision: point-in-time feature reconstruction, chronological data splitting, and walk-forward cross-validation eliminates the risk of temporal data leakage. The literature review is comprehensive, effectively bridging traditional airline revenue management with modern ML ensembles (though it could have featured slightly more critical debate on the limitations of external LLM-based sentiment signals). The results are presented with transparency and the residual analysis is solid for its depth, identifying phase-shifted destination biases rather than hiding behind aggregate model averages. The research translates into actionable business recommendations (specifically the two-layer dynamic pricing system). It is scientifically written, well structured according to guidelines, and sets a benchmark for industry-applied academic research."
> — her thesis examiner from Amazon

## Ask her about
Right-censored targets (flights that sell out), reconstructing history without snapshots, and why external signals did not help.
