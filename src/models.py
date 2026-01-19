from typing import TypedDict, List, Literal
from pydantic import BaseModel

class SeminarState(TypedDict):
    topic: str
    outline: List[str]
    current_section_index: int
    current_section: str
    key_points: List[str]
    rag_context: str
    web_context: str
    draft: str
    section_drafts: List[str]
    final_paper: str
    is_valid: bool
    feedback: str
    revision_count: int

class Plan(BaseModel):
    Plan: List[str]

class Keypoints(BaseModel):
    Keypoints: List[str]
