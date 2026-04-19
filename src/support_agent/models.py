from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class TicketRow(BaseModel):
    code: str
    user_message: str
    domain: str
    intent: str
    reference_response: str


class PreprocessResult(BaseModel):
    cleaned_message: str
    normalized_message: str
    corrections: List[str] = Field(default_factory=list)


class ClassificationResult(BaseModel):
    category: str
    intent: str
    product_name: Optional[str] = None
    issue_type: str
    urgency: str
    order_number: Optional[str] = None
    escalation_needed: bool = False
    confidence: float = 0.0


class SentimentResult(BaseModel):
    sentiment: str
    score: int
    explanation: str


class KeywordResult(BaseModel):
    keywords: List[str]
    entities: Dict[str, Any]


class ReflectionResult(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    improvement_suggestions: List[str]


class PipelineResult(BaseModel):
    raw_input: str
    preprocess: PreprocessResult
    classification: ClassificationResult
    sentiment: SentimentResult
    keywords: KeywordResult
    selected_route: str
    first_draft: str
    reflection: ReflectionResult
    improved_draft: str
    change_log: List[str]