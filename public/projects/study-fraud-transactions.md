---
title: Detecting fraudulent card transactions (study project)
short_name: Fraud classification (study)
summary: Comparing classic models for detecting fraudulent transactions, framed as a task for a bank's risk department
kind: coursework
company: Master's programme coursework (public dataset)
status: completed study project
role: author
stack: [Python, scikit-learn, XGBoost]
evidence: ["https://gist.github.com/VildanaRazumova/c84334373f6dcb14fdb207dadfe3c345"]
---

## Situation and task
Framed as a request from a bank's risk department. Data: a public Kaggle dataset of 50,000 transactions, about 30% of them fraudulent.

## What I did
- I used a stratified split and outlier-resistant scaling.
- I removed a feature that leaked the answer: the count of failed transactions over 7 days.
- I compared logistic regression, Random Forest and XGBoost, and tuned logistic regression.

## Result
- All three models reached ROC AUC of about 0.73–0.74; tuned logistic regression: 0.739 on test, 0.73 on validation, accuracy 0.79.
- A simple model was as good as the complex ones on this data.

## What I learned
- Removing a leaking feature lowers the score and makes it honest.
