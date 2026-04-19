# Support Agent Task 1

This project implements an automated customer support ticket processor for the foundation patterns assignment.

## Patterns covered

### 1. Prompt Chaining
Three sequential LLM calls:
- preprocessing
- classification
- response generation

### 2. Routing
After classification, tickets are routed to one of:
- order_cancel
- technical_issue
- billing_refund
- general_inquiry
- complaint_escalation

### 3. Parallelization
Two independent subtasks run concurrently using `asyncio.gather()`:
- sentiment analysis
- keyword/entity extraction

### 4. Reflection
The system:
- generates a first draft
- critiques it
- improves it
- prints a visible change log

## Dataset
The main dataset uses `cancel_order` examples from the provided data.
Extra manually added tickets are included to cover additional routes required by the rubric.

Files:
- `data/cancel_order_dataset.tsv`
- `data/extra_routes.json`

## Setup

Create and activate a virtual environment if desired, then install dependencies:

```bash
pip install -r requirements.txt