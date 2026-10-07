from langgraph.graph import StateGraph, START, END

from graph.state import ConstructionState

from graph.nodes import (
    requirement_agent,
    cost_agent,
    material_agent,
    timeline_agent,
    planning_agent,
    visualization_agent,
    budget_agent,
    report_agent
)


# Create LangGraph
builder = StateGraph(ConstructionState)


# Add agents as nodes
builder.add_node("requirement_agent", requirement_agent)
builder.add_node("cost_agent", cost_agent)
builder.add_node("material_agent", material_agent)
builder.add_node("timeline_agent", timeline_agent)
builder.add_node("planning_agent", planning_agent)
builder.add_node("visualization_agent", visualization_agent)
builder.add_node("budget_agent", budget_agent)
builder.add_node("report_agent", report_agent)


# Define workflow
builder.add_edge(START, "requirement_agent")

builder.add_edge(
    "requirement_agent",
    "cost_agent"
)

builder.add_edge(
    "cost_agent",
    "material_agent"
)

builder.add_edge(
    "material_agent",
    "timeline_agent"
)

builder.add_edge(
    "timeline_agent",
    "planning_agent"
)

builder.add_edge(
    "planning_agent",
    "visualization_agent"
)

builder.add_edge(
    "visualization_agent",
    "budget_agent"
)

builder.add_edge(
    "budget_agent",
    "report_agent"
)

builder.add_edge(
    "report_agent",
    END
)


# Compile workflow
construction_workflow = builder.compile()