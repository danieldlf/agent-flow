from typing import Literal

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode

from core.services import LLMService
from core.tools.asana import (
    get_user,
    # get_users_for_workspace
)

tools = [get_user]

tool_node = ToolNode(tools)

model = LLMService().get_model("ollama", model="llama3.1").bind_tools(tools)

def should_continue(state: MessagesState) -> Literal["tools", END]: # type: ignore
    messages = state["messages"]
    last_message = messages[-1]

    if last_message.tool_calls:
        return "tools"
    
    return END

def call_model(state: MessagesState):
    messages = state['messages']
    response = model.invoke(messages)

    return {"messages": [response]}

workflow = StateGraph(MessagesState)

workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
)

workflow.add_edge("tools", "agent")

checkpointer = MemorySaver()

app = workflow.compile(checkpointer=checkpointer)