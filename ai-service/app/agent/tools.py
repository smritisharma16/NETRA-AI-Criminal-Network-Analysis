"""
tools.py — LangGraph tool definitions for NETRA Investigation Agent (Phase A)

All 8 tool names are preserved exactly so the LLM's existing knowledge remains
valid.  Each tool delegates entirely to InvestigationService, which handles
input validation, error catching, and output truncation.

If a tool result contains {"tool_error": True, ...}, it is returned as-is so
the LLM can read the structured error and respond appropriately without
inventing facts.

No raw Python exceptions ever escape a tool function.
"""

import logging
from typing import List, Dict, Optional

from pydantic import BaseModel, Field
from langchain_core.tools import tool

from app.agent.tool_service import InvestigationService, get_session

logger = logging.getLogger(__name__)


@tool
def search_cases(query: str) -> List[Dict]:
    """Find cases matching an investigator's query."""
    with get_session() as db:
        svc = InvestigationService(db)
        return svc.search_cases(query)


@tool
def search_entities(query: str, case_id: Optional[str] = None) -> Dict:
    """Resolve investigator-mentioned entities against canonical NETRA entities. Returns a dictionary with truncated flag and results."""
    with get_session() as db:
        svc = InvestigationService(db)
        return svc.search_entities(query, case_id)


@tool
def get_entity(entity_id: str) -> Dict:
    """Return canonical entity details and authorized relationships/case memberships."""
    with get_session() as db:
        svc = InvestigationService(db)
        return svc.get_entity(entity_id)


@tool
def get_case_network_summary(case_id: str) -> Dict:
    """Return a structured summary of ALL entities and relationships in a case."""
    with get_session() as db:
        svc = InvestigationService(db)
        return svc.get_case_network_summary(case_id)


@tool
def get_entity_relationships(entity_id: str, case_id: Optional[str] = None) -> Dict:
    """Return immediate relationships for an entity, optionally scoped to a case."""
    with get_session() as db:
        svc = InvestigationService(db)
        return svc.get_entity_relationships(entity_id, case_id)


@tool
def find_cross_case_connections(entity_id: str) -> Dict:
    """Find other cases that share this entity."""
    with get_session() as db:
        svc = InvestigationService(db)
        return svc.find_cross_case_connections(entity_id)


@tool
def explore_graph(case_id: str, entity_id: str, depth: int) -> Dict:
    """Explore the network graph starting from an entity, limited to a max depth of 5."""
    with get_session() as db:
        svc = InvestigationService(db)
        return svc.explore_graph(case_id, entity_id, depth)


@tool
def get_relationship(relationship_id: str) -> Dict:
    """Return relationship details, ensuring only CONFIRMED relationships are exposed."""
    with get_session() as db:
        svc = InvestigationService(db)
        return svc.get_relationship(relationship_id)


@tool
def get_findings(case_id: str) -> List[Dict]:
    """Return the Step 10.9 investigator-facing findings."""
    with get_session() as db:
        svc = InvestigationService(db)
        return svc.get_findings(case_id)


@tool
def get_evidence(evidence_id: str) -> Dict:
    """Return evidence metadata and provenance."""
    with get_session() as db:
        svc = InvestigationService(db)
        return svc.get_evidence(evidence_id)


@tool
def run_network_analysis(case_id: str) -> Dict:
    """Expose existing deterministic analytics for a case (degree, betweenness, etc)."""
    with get_session() as db:
        svc = InvestigationService(db)
        return svc.run_network_analysis(case_id)


class ActionItem(BaseModel):
    label: str = Field(description="Short UI text")
    description: str = Field(description="A short explanation of why to take this action")
    prompt: str = Field(description="The internal natural language question this action will send")
    type: str = Field(description="ENUM of (GRAPH, CROSS_CASE, EVIDENCE, ANALYTICS, ENTITY, RELATIONSHIP)")
    target_id: Optional[str] = Field(description="The ID of the subject entity/relationship", default=None)
    is_recommended: Optional[bool] = Field(description="Set to True for the single best next step", default=False)

class FactItem(BaseModel):
    text: str = Field(description="Text of the fact")
    source: Optional[str] = Field(description="Source of the fact", default=None)

class ObservationItem(BaseModel):
    text: str = Field(description="Text of the observation")
    source: Optional[str] = Field(description="Source of the observation", default=None)

class UncertaintyItem(BaseModel):
    text: str = Field(description="Text of the uncertainty")
    source: Optional[str] = Field(description="Source of the uncertainty", default=None)

class SubmitFinalResponseArgs(BaseModel):
    answer: str = Field(description="The final investigative response")
    facts: List[FactItem] = Field(default_factory=list)
    observations: List[ObservationItem] = Field(default_factory=list)
    uncertainties: List[UncertaintyItem] = Field(default_factory=list)
    actions: List[ActionItem] = Field(default_factory=list)

@tool(args_schema=SubmitFinalResponseArgs)
def submit_final_response(answer: str, facts: list, observations: list, uncertainties: list, actions: list) -> str:
    """Submit your final investigative response using a structured format. YOU MUST CALL THIS TOOL TO FINISH YOUR TURN.
    facts, observations, and uncertainties should be lists of dicts e.g. [{"text": "...", "source": "..."}].
    actions should be a list of suggested next steps. Each action MUST contain:
    - label: Short UI text (e.g., "Find related cases")
    - description: A short explanation of why to take this action (e.g., "Check whether this entity appears in other investigations.")
    - prompt: The internal natural language question this action will send (e.g., "Which other cases are connected to Juhu?")
    - type: ENUM of (GRAPH, CROSS_CASE, EVIDENCE, ANALYTICS, ENTITY, RELATIONSHIP)
    - target_id: The ID of the subject entity/relationship
    - is_recommended: bool, set to True for the single best next step.
    """
    return "Response submitted."

def get_all_tools():
    return [
        search_cases,
        search_entities,
        get_entity,
        get_case_network_summary,
        get_entity_relationships,
        find_cross_case_connections,
        explore_graph,
        get_relationship,
        get_findings,
        get_evidence,
        run_network_analysis,
        submit_final_response
    ]
