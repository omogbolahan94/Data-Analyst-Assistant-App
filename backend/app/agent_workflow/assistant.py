from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from typing import Annotated, List, Dict, Any, Optional
from typing_extensions import TypedDict   

from .state import State
from .tools import tools
from .llms import groq_llm


groq_llm_with_tools = groq_llm.bind_tools(tools)


def assistant(state: State):
    return {"messages": [groq_llm_with_tools.invoke(state["messages"])]}


def decides_if_tool(state: State):
    """
    The agent's output is an AIMessage that contains a tool_call object
    """
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tools"
    return "end"







