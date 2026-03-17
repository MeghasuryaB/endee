from typing import TypedDict, List

class ResearchState(TypedDict):
    question: str
    sub_questions: List[str]
    search_results: List[dict]
    analysis: List[dict]
    report: str
    status: str