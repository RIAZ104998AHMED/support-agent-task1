import json

from support_agent.prompts.templates import (
    BILLING_BRANCH_PROMPT,
    COMPLAINT_BRANCH_PROMPT,
    GENERAL_BRANCH_PROMPT,
    ORDER_CANCEL_BRANCH_PROMPT,
    TECHNICAL_BRANCH_PROMPT,
)


class BranchHandler:
    def __init__(self, llm) -> None:
        self.llm = llm

    async def handle(self, route: str, ticket_data: dict) -> str:
        payload = json.dumps(ticket_data, indent=2, ensure_ascii=False)

        if route == "order_cancel":
            prompt = ORDER_CANCEL_BRANCH_PROMPT.format(ticket_data=payload)
        elif route == "technical_issue":
            prompt = TECHNICAL_BRANCH_PROMPT.format(ticket_data=payload)
        elif route == "billing_refund":
            prompt = BILLING_BRANCH_PROMPT.format(ticket_data=payload)
        elif route == "complaint_escalation":
            prompt = COMPLAINT_BRANCH_PROMPT.format(ticket_data=payload)
        else:
            prompt = GENERAL_BRANCH_PROMPT.format(ticket_data=payload)

        return await self.llm.complete_text(prompt)