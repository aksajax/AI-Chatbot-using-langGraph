import os
from typing import Annotated, TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

# 1. Load Environment Variables
load_dotenv()

# 2. Define the Application State
# `add_messages` ensures new messages are appended to the history list rather than replacing it
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# 3. Initialize the LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# 4. Define the Chatbot Node
def chatbot_node(state: ChatState):
    """Executes the LLM with current conversation history."""
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# 5. Build the Graph
workflow = StateGraph(ChatState)

# Add Node
workflow.add_node("chatbot", chatbot_node)

# Add Edges
workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)

# 6. Add Checkpointing (Memory Persistence)
# MemorySaver stores conversation state in-memory across multiple user inputs
checkpointer = MemorySaver()
app = workflow.compile(checkpointer=checkpointer)

# ---------------------------------------------------------------------------
# 7. Interactive Terminal Chat Loop
# ---------------------------------------------------------------------------
def start_chat():
    session_id = "session_user_1"
    config = {"configurable": {"thread_id": session_id}}

    print("=" * 60)
    print("  Basic AI Chatbot (LangGraph + MemorySaver)")
    print("  Type 'exit' or 'quit' to stop.")
    print("=" * 60 + "\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # Pass input to the graph
        input_messages = [HumanMessage(content=user_input)]
        
        # Stream response events
        print("AI: ", end="", flush=True)
        for event in app.stream({"messages": input_messages}, config=config):
            for value in event.values():
                print(value["messages"][-1].content)

if __name__ == "__main__":
    start_chat()