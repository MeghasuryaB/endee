from langgraph.graph import StateGraph, END
from graph.state import ResearchState
from agents.planner import planner_agent
from agents.searcher import searcher_agent
from agents.analyzer import analyzer_agent
from agents.reporter import reporter_agent

def build_workflow():
    workflow = StateGraph(ResearchState)

    # Register all 4 agents as nodes
    workflow.add_node("planner", planner_agent)
    workflow.add_node("searcher", searcher_agent)
    workflow.add_node("analyzer", analyzer_agent)
    workflow.add_node("reporter", reporter_agent)

    # Define the flow
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "searcher")
    workflow.add_edge("searcher", "analyzer")
    workflow.add_edge("analyzer", "reporter")
    workflow.add_edge("reporter", END)

    return workflow.compile()