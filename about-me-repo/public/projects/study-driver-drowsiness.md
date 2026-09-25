---
title: Spotting drowsy drivers from face images (study project)
short_name: Drowsiness detection (study)
summary: A convolutional neural network (CNN) that sorts driver face images into drowsy or alert, framed as a task for a logistics department
kind: coursework
company: Master's programme coursework (public dataset)
status: completed study project
role: author
stack: [Python, TensorFlow/Keras, scikit-learn]
evidence: ["https://gist.github.com/VildanaRazumova/7e4ee7c1699933c47f56fe9374b1c9d1"]
---

## Situation and task
Framed as a request from a logistics department: detect drowsy drivers from camera images. Data: the public Kaggle Driver Drowsiness Dataset (41,790 images), of which I used a balanced subset of 6,450.

## What I did
- I resized images to 64×64 and split them 60/20/20 into train, validation and test.
- I built a CNN with augmentation, dropout, batch normalisation and early stopping, and ran 10 experiments.
- An early validation accuracy of about 99% looked too good, so I treated it as possible data leakage and changed the setup.

## Result
Test accuracy 0.94, F1 0.94.

## What I learned
- A suspiciously high score is a reason to look for leakage, not to celebrate.
