# Support Agent Task 1

This project implements an automated customer support ticket processor using four foundational LLM design patterns: Prompt Chaining, Routing, Parallelization, and Reflection.

---

## Architecture Overview

The system processes a raw support message through multiple stages:

1. Preprocessing → cleans and normalizes input  
2. Classification → extracts structured data and determines category  
3. Parallel Analysis → sentiment + keyword extraction  
4. Routing → selects a specialized branch  
5. Response Generation → produces a draft reply  
6. Reflection → critiques and improves the response  

---

## Patterns Covered

### 1. Prompt Chaining
A sequential pipeline of 3 LLM calls:
- Preprocessing (clean text)
- Classification (structured JSON output)
- Response generation (based on structured data)

### 2. Routing
Tickets are dynamically routed into specialized branches:
- `order_cancel`
- `technical_issue`
- `billing_refund`
- `general_inquiry`
- `complaint_escalation`

Each branch uses a different prompt and logic.

### 3. Parallelization
Two independent tasks run concurrently using `asyncio.gather()`:
- Sentiment analysis
- Keyword & entity extraction

### 4. Reflection
The system:
- Generates a first draft
- Critiques it using the LLM
- Produces an improved version
- Logs the changes

---

## Dataset

- `data/cancel_order_dataset.tsv`
- `data/extra_routes.json`

Includes at least 10 support messages covering all routing categories.

---

## Setup

Install dependencies:

```bash
pip install -r requirements.txt