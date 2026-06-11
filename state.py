from typing import Optional
from typing_extensions import TypedDict

class CampaignState(TypedDict):
    # The original request
    campaign_request: str

    # Research Agent output
    research_findings: Optional[str]

    # Strategist Agent output
    campaign_angles: Optional[list[str]]

    # Critic Agent output
    critic_feedback: Optional[str]
    selected_angle: Optional[str]

    # Writer Agent output
    final_brief: Optional[str]

    # System tracking
    current_stage: str
    revision_count: int
    status: str
    routing_table: Optional[dict]