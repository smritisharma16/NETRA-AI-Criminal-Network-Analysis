with open(r"d:\NETRA\SIH2026\ai-service\app\agent\tools.py", "r", encoding="utf-8") as f:
    content = f.read()

import_pydantic = "from pydantic import BaseModel, Field\nfrom langchain_core.tools import tool"
content = content.replace("from langchain_core.tools import tool", import_pydantic)

pydantic_schema = """
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
"""

old_func_def = "@tool\ndef submit_final_response(answer: str, facts: list, observations: list, uncertainties: list, actions: list) -> str:"

if old_func_def in content:
    content = content.replace(old_func_def, pydantic_schema.strip())
    with open(r"d:\NETRA\SIH2026\ai-service\app\agent\tools.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed tools.py")
else:
    print("Could not find definition.")
