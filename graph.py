from langgraph.graph import StateGraph, END
from state import CampaignState
from agents import research_agent, strategist_agent, critic_agent, writer_agent

def should_continue(state: CampaignState) -> str:
    stage = state["current_stage"]

    if stage == "research_complete":
        return "strategist"
    elif stage == "strategy_complete":
        return "critic"
    elif stage == "critique_complete":
        return "writer"
    else:
        return END

def build_graph():
    graph = StateGraph(CampaignState)

    # Add all four agents as nodes
    graph.add_node("research", research_agent)
    graph.add_node("strategist", strategist_agent)
    graph.add_node("critic", critic_agent)
    graph.add_node("writer", writer_agent)

    # Entry point
    graph.set_entry_point("research")

    # Conditional routing based on blackboard state
    graph.add_conditional_edges("research", should_continue)
    graph.add_conditional_edges("strategist", should_continue)
    graph.add_conditional_edges("critic", should_continue)

    # Writer is the final node
    graph.add_edge("writer", END)

    return graph.compile()