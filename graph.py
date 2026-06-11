from langgraph.graph import StateGraph, END
from state import CampaignState
from agents import research_agent, strategist_agent, critic_agent, writer_agent

DEFAULT_ROUTING_TABLE = {
    "research_complete": "strategist",
    "strategy_complete": "critic",
    "critique_approved": "writer",
    "critique_rejected": "strategist",
    "complete": END
}

def should_continue(state: CampaignState) -> str:
    stage = state["current_stage"]
    routing_table = state.get("routing_table") or DEFAULT_ROUTING_TABLE
    next_step = routing_table.get(stage, END)
    print(f"--- Routing: {stage} -> {next_step} ---")
    return next_step

def build_graph():
    graph = StateGraph(CampaignState)

    graph.add_node("research", research_agent)
    graph.add_node("strategist", strategist_agent)
    graph.add_node("critic", critic_agent)
    graph.add_node("writer", writer_agent)

    graph.set_entry_point("research")

    graph.add_conditional_edges("research", should_continue)
    graph.add_conditional_edges("strategist", should_continue)
    graph.add_conditional_edges("critic", should_continue)

    graph.add_edge("writer", END)

    return graph.compile()