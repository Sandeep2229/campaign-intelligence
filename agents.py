from langchain_openai import ChatOpenAI
from state import CampaignState

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

def research_agent(state: CampaignState) -> dict:
    print("--- Research Agent Running ---")

    request = state["campaign_request"]

    response = llm.invoke(
        f"""You are a market research expert.
        
Given this campaign request: {request}

Research and provide:
1. Target audience profile
2. Key market trends
3. Competitor positioning
4. Main audience pain points

Be specific and concise."""
    )

    return {
        "research_findings": response.content,
        "current_stage": "research_complete",
        "status": "in_progress"
    }

def strategist_agent(state: CampaignState) -> dict:
    print("--- Strategist Agent Running ---")

    research = state["research_findings"]

    response = llm.invoke(
        f"""You are a marketing strategist.

Based on this research: {research}

Generate exactly 3 distinct campaign angles.
Format each angle as:
ANGLE 1: [title] - [description]
ANGLE 2: [title] - [description]
ANGLE 3: [title] - [description]"""
    )

    angles = response.content.split("\n")
    angles = [a.strip() for a in angles if a.strip().startswith("ANGLE")]

    return {
        "campaign_angles": angles,
        "current_stage": "strategy_complete",
        "status": "in_progress"
    }


def critic_agent(state: CampaignState) -> dict:
    print("--- Critic Agent Running ---")

    angles = state["campaign_angles"]
    angles_text = "\n".join(angles)
    revision_count = state["revision_count"]

    response = llm.invoke(
        f"""You are a harsh but fair campaign critic.

Review these campaign angles:
{angles_text}

Are these angles strong enough for a real campaign? Be strict.

Format your response exactly as:
VERDICT: APPROVE or REVISE
SELECTED: [paste the winning angle here]
REASON: [why]
WEAKNESSES: [two things to improve]"""
    )

    content = response.content
    selected = ""
    verdict = "APPROVE"

    for line in content.split("\n"):
        if line.startswith("VERDICT:"):
            verdict = line.replace("VERDICT:", "").strip()
        if line.startswith("SELECTED:"):
            selected = line.replace("SELECTED:", "").strip()

    # Force approve after 3 revisions
    if revision_count >= 3:
        verdict = "APPROVE"

    next_stage = "critique_approved" if verdict == "APPROVE" else "critique_rejected"

    return {
        "critic_feedback": content,
        "selected_angle": selected,
        "current_stage": next_stage,
        "revision_count": revision_count + 1
    }


def writer_agent(state: CampaignState) -> dict:
    print("--- Writer Agent Running ---")

    angle = state["selected_angle"]
    research = state["research_findings"]
    feedback = state["critic_feedback"]

    response = llm.invoke(
        f"""You are a senior copywriter.

Campaign angle: {angle}
Research context: {research}
Critic notes: {feedback}

Write a complete campaign brief including:
1. Campaign headline
2. Core message (2 sentences)
3. Target audience
4. Three key messages
5. Call to action"""
    )

    return {
        "final_brief": response.content,
        "current_stage": "complete",
        "status": "done"
    }