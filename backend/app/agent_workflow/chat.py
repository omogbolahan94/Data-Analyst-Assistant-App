from build_graph import graph
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage



def chat(user_input):
    message = [HumanMessage(content=user_input)]
    result = graph.invoke({"messages": message}) 
    return result["messages"][-1].content  










