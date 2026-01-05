# THE BRAIN: Defines, Nodes, Edges and compiles the graph
# Here we call workflow.compile(). It imports functions from nodes.py to keep file clean.
from langgraph.graph import StateGraph, END
from app.schemas import AgentState
from agents.nodes import manager_node, search_node, scraper_node, strategist_node

# Initialize the Graph
workflow = StateGraph(AgentState)

# Add our Nodes
workflow.add_node("manager", manager_node)
workflow.add_node("search", search_node)
workflow.add_node("scraper", scraper_node)
workflow.add_node("strategist", strategist_node)

# Set the Entry Point
workflow.set_entry_point("manager")

# Define the Logic (Edges)
workflow.add_edge("manager", "search")
workflow.add_edge("search", "scraper")
workflow.add_edge("scraper", "strategist")
workflow.add_edge("strategist", END)

# Compile the Graph
agent_app2 = workflow.compile()