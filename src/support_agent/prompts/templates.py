PREPROCESS_PROMPT = """
You are preprocessing a support ticket.

Tasks:
1. Clean the raw message
2. Fix obvious typos
3. Normalize casing and wording
4. Keep the meaning unchanged

Return valid JSON only:
{{
  "cleaned_message": "...",
  "normalized_message": "...",
  "corrections": ["..."]
}}

Raw message:
{message}
"""

CLASSIFICATION_PROMPT = """
You are a support ticket classifier.

Classify into one of:
- technical_issue
- billing_refund
- general_inquiry
- complaint_escalation
- order_cancel

Also extract:
- category
- intent
- product_name
- issue_type
- urgency
- order_number
- escalation_needed
- confidence

Rules:
- cancel order / cancel purchase -> order_cancel
- charged twice / refund / invoice / payment issue -> billing_refund
- crash / bug / error / app issue -> technical_issue
- angry / rude / supervisor / complaint -> complaint_escalation
- shipping / account info / how-to question -> general_inquiry

Return valid JSON only:
{{
  "category": "...",
  "intent": "...",
  "product_name": null,
  "issue_type": "...",
  "urgency": "low|medium|high",
  "order_number": null,
  "escalation_needed": false,
  "confidence": 0.0
}}

Normalized message:
{message}
"""

SENTIMENT_PROMPT = """
Analyze the sentiment of this support message.

Return valid JSON only:
{{
  "sentiment": "positive|neutral|negative",
  "score": 1,
  "explanation": "..."
}}

Message:
{message}
"""

KEYWORD_PROMPT = """
Extract keywords and entities from this support message.

Return valid JSON only:
{{
  "keywords": ["..."],
  "entities": {{
    "order_number": "...",
    "issue_type": "...",
    "product": "..."
  }}
}}

Message:
{message}
"""

ORDER_CANCEL_BRANCH_PROMPT = """
You are an order cancellation specialist.

Use this fictional company policy:
- Orders can be canceled before shipment
- If order number is missing, ask for it
- If already shipped, explain cancellation may not be possible and offer return guidance
- If customer sounds stressed, be empathetic

Write a customer-facing response.

Ticket data:
{ticket_data}
"""

TECHNICAL_BRANCH_PROMPT = """
You are a technical support specialist.

Give practical troubleshooting steps.
Be concise and helpful.

Ticket data:
{ticket_data}
"""

BILLING_BRANCH_PROMPT = """
You are a billing and refund specialist.

Use this fictional policy:
- Duplicate charge -> apologize and say billing team can review/refund
- Payment failed -> ask customer to verify payment method and retry
- Refund inquiry -> explain next steps clearly

Ticket data:
{ticket_data}
"""

GENERAL_BRANCH_PROMPT = """
You are a general customer support assistant.

Answer clearly and concisely.

Ticket data:
{ticket_data}
"""

COMPLAINT_BRANCH_PROMPT = """
You are a senior support specialist.

Be empathetic.
Acknowledge frustration.
Mention escalation if appropriate.

Ticket data:
{ticket_data}
"""

REFLECTION_PROMPT = """
Review the draft support response.

Evaluate:
- tone
- completeness
- clarity
- usefulness
- policy alignment

Return valid JSON only:
{{
  "strengths": ["..."],
  "weaknesses": ["..."],
  "improvement_suggestions": ["..."]
}}

Draft:
{draft}

Ticket data:
{ticket_data}
"""

IMPROVEMENT_PROMPT = """
Improve the support response using the critique below.

Original draft:
{draft}

Critique:
{critique}

Ticket data:
{ticket_data}

Write the improved final response.
"""