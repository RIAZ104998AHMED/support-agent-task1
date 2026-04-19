import json

from support_agent.models import ReflectionResult
from support_agent.prompts.templates import IMPROVEMENT_PROMPT, REFLECTION_PROMPT


class ReflectionEngine:
    def __init__(self, llm) -> None:
        self.llm = llm

    async def improve(self, draft: str, ticket_data: dict) -> tuple[ReflectionResult, str, list[str]]:
        critique = await self.llm.complete_json(
            REFLECTION_PROMPT.format(
                draft=draft,
                ticket_data=json.dumps(ticket_data, indent=2, ensure_ascii=False),
            ),
            ReflectionResult,
        )

        improved = await self.llm.complete_text(
            IMPROVEMENT_PROMPT.format(
                draft=draft,
                critique=json.dumps(critique.model_dump(), indent=2, ensure_ascii=False),
                ticket_data=json.dumps(ticket_data, indent=2, ensure_ascii=False),
            )
        )

        change_log = []
        if critique.weaknesses:
            change_log.append("Addressed weaknesses found during reflection.")
        if critique.improvement_suggestions:
            change_log.append("Applied specific improvement suggestions.")
        change_log.append("Second pass improved clarity, completeness, and tone.")

        return critique, improved, change_log