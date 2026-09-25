---
title: Classifying the sentiment of financial news headlines (study project)
short_name: News sentiment (study)
summary: Classifying financial news headlines as positive, neutral or negative, framed as an early-warning signal for a bank's risk department
kind: coursework
company: Master's programme coursework (public dataset)
status: completed study project
role: author
stack: [Python, scikit-learn, NLTK, Word2Vec, FinBERT, Hugging Face Transformers]
evidence: ["https://colab.research.google.com/drive/1TBwz1uwg5BLTcZAo3uW7aBbWvKxp56P7"]
---

## Situation and task
Framed as a request from a bank's risk department: flag negative financial news early. Data: 4,846 labelled headlines from Kaggle, strongly imbalanced (2,879 neutral, 1,363 positive, 604 negative).

## What I did
- I cleaned and lemmatised the text and added simple features (length, word count, count of risk words).
- I compared three text representations with the same classifier (logistic regression): TF-IDF, Word2Vec and FinBERT embeddings, from a language model trained on financial text.
- I used a stratified 80/20 split and macro F1 as the main metric, because accuracy hides the rare negative class.

## Result
- FinBERT embeddings were clearly best: macro F1 0.66 and accuracy 0.72, against macro F1 0.37 for the TF-IDF baseline.
- The extra hand-made features added almost nothing.
- Her own next steps: fine-tune the model instead of using frozen embeddings, use cross-validation instead of one split, and address class imbalance.

## What I learned
- On imbalanced classes, macro F1 tells the truth that accuracy hides.
