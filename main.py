import os
from dotenv import load_dotenv

load_dotenv()

# Force LangSmith settings before importing anything else
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"] = "campaign-intelligence"



from graph import build_graph

def run_campaign(request: str):
    graph = build_graph()

    initial_state = {
        "campaign_request": request,
        "research_findings": None,
        "campaign_angles": None,
        "critic_feedback": None,
        "selected_angle": None,
        "final_brief": None,
        "current_stage": "start",
        "revision_count": 0,
        "status": "in_progress"
    }

    print("\n=== Campaign Intelligence System Starting ===\n")

    result = graph.invoke(initial_state)

    print("\n=== FINAL CAMPAIGN BRIEF ===\n")
    print(result["final_brief"])
    print("\n=== STATUS:", result["status"], "===")

if __name__ == "__main__":
    run_campaign(
        "Launch a new AI productivity app targeting busy professionals in NYC"
    )