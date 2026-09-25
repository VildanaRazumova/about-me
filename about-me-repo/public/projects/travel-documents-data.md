---
title: Vouchers and e-ticket receipts for travellers, live in two days
short_name: Travel documents
summary: A web service for travellers' vouchers and e-ticket receipts, launched in two days with a developer and an infrastructure engineer; she owned the data and document logic
kind: work
company: Fun&Sun
status: in production
role: owner of the data layer and document data; a developer built the page, an infrastructure engineer deployed it
period: 2026-06 – 2026-07
skills: [SQL, PostgreSQL, data modelling, data quality, fast delivery under pressure]
---

## Situation and task
The business needed an additional channel for issuing vouchers and e-ticket receipts, at very short notice. Some flight times in the source were incomplete or inconsistent. The task: launch within days, with correct data.

## What I did
- Built the data behind the documents: bookings, flights, hotels and the fields each document needs.
- Took flight times from a more reliable source and handled edge cases such as overnight flights.
- Brought in traveller and payment data, and tourist registration codes generated through the state service's API (see Registration API).
- Owned the data in a team of three: a developer built the page, an infrastructure engineer deployed it.
- Kept every data change reversible, with a visible list of differences for the business to approve.

### Key decisions
- Correctness over speed where it matters: a wrong flight time on a document is worse than a late one.
- Identify travellers by document, not by name: family members in one booking can share a name.

## Result
- Live in two days and in production since. Staff issued documents for thousands of travellers through it, and travellers flew on time with all the documents they needed.

## What I learned
- Speed is no excuse to skip version control.

## Good to discuss
Delivering under pressure in a small team, and safely changing the data everyone relies on.
