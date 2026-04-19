import asyncio

from support_agent.branches.handlers import BranchHandler
from support_agent.models import (
    ClassificationResult,
    KeywordResult,
    PipelineResult,
    PreprocessResult,
    SentimentResult,
)
from support_agent.prompts.templates import (
    CLASSIFICATION_PROMPT,
    KEYWORD_PROMPT,
    PREPROCESS_PROMPT,
    SENTIMENT_PROMPT,
)
from support_agent.reflection.engine import ReflectionEngine


class TicketProcessor:
    def __init__(self, llm) -> None:
        self.llm = llm
        self.branch_handler = BranchHandler(llm)
        self.reflection_engine = ReflectionEngine(llm)

    async def preprocess(self, raw_message: str) -> PreprocessResult:
        print("\n[CHAIN 1/3] Preprocessing started")
        result = await self.llm.complete_json(
            PREPROCESS_PROMPT.format(message=raw_message),
            PreprocessResult,
        )
        print("[CHAIN 1/3] Preprocessing completed")
        return result

    async def classify(self, normalized_message: str) -> ClassificationResult:
        print("\n[CHAIN 2/3] Classification started")
        result = await self.llm.complete_json(
            CLASSIFICATION_PROMPT.format(message=normalized_message),
            ClassificationResult,
        )
        print("[CHAIN 2/3] Classification completed")
        print(f"[ROUTING CANDIDATE] {result.category}")
        return result

    async def analyze_sentiment(self, message: str) -> SentimentResult:
        print("[PARALLEL] Sentiment analysis started")
        result = await self.llm.complete_json(
            SENTIMENT_PROMPT.format(message=message),
            SentimentResult,
        )
        print("[PARALLEL] Sentiment analysis completed")
        return result

    async def extract_keywords(self, message: str) -> KeywordResult:
        print("[PARALLEL] Keyword extraction started")
        result = await self.llm.complete_json(
            KEYWORD_PROMPT.format(message=message),
            KeywordResult,
        )
        print("[PARALLEL] Keyword extraction completed")
        return result

    def select_route(self, classification: ClassificationResult) -> str:
        route = classification.category
        print(f"\n[ROUTING] Selected branch: {route}")
        return route

    async def generate_response(self, route: str, ticket_data: dict) -> str:
        print(f"[CHAIN 3/3] Response generation through '{route}' started")
        response = await self.branch_handler.handle(route, ticket_data)
        print(f"[CHAIN 3/3] Response generation through '{route}' completed")
        return response

    async def process_ticket(self, raw_message: str) -> dict:
        preprocess_result = await self.preprocess(raw_message)
        classification_result = await self.classify(preprocess_result.normalized_message)

        print("\n[PARALLEL] Launching concurrent tasks")
        sentiment_result, keyword_result = await asyncio.gather(
            self.analyze_sentiment(preprocess_result.normalized_message),
            self.extract_keywords(preprocess_result.normalized_message),
        )
        print("[PARALLEL] Concurrent tasks completed")

        selected_route = self.select_route(classification_result)

        ticket_data = {
            "raw_input": raw_message,
            "preprocess": preprocess_result.model_dump(),
            "classification": classification_result.model_dump(),
            "sentiment": sentiment_result.model_dump(),
            "keywords": keyword_result.model_dump(),
        }

        first_draft = await self.generate_response(selected_route, ticket_data)

        print("\n[REFLECTION] Evaluating first draft")
        reflection, improved_draft, change_log = await self.reflection_engine.improve(
            first_draft,
            ticket_data,
        )
        print("[REFLECTION] Improvement completed")

        print("\n--- BEFORE REFLECTION ---")
        print(first_draft)
        print("\n--- AFTER REFLECTION ---")
        print(improved_draft)
        print("\n--- CHANGE LOG ---")
        for item in change_log:
            print(f"- {item}")

        result = PipelineResult(
            raw_input=raw_message,
            preprocess=preprocess_result,
            classification=classification_result,
            sentiment=sentiment_result,
            keywords=keyword_result,
            selected_route=selected_route,
            first_draft=first_draft,
            reflection=reflection,
            improved_draft=improved_draft,
            change_log=change_log,
        )

        return result.model_dump()