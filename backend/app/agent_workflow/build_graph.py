from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition 

from .state import State
from .assistant import assistant, decides_if_tool


graph_builder = StateGraph(State)
graph_builder.add_node('agent', assistant)
graph_builder.add_node("tools", ToolNode(tools=tools))

graph_builder.add_edge(START, "agent")
graph_builder.add_conditional_edges("agent", decides_if_tool, {"tools":"tools", "end": END})
graph_builder.add_edge("tools", "agent")

graph = graph_builder.compile() 
