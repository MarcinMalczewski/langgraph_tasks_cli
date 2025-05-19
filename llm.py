from dotenv import load_dotenv

from langchain_core.messages import SystemMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, MessagesState
from langchain.chat_models import init_chat_model

from retrieve_service import get_tasks, get_tasks_for_team, get_tasks_for_person, create_graph


load_dotenv()


# declare global variables
llm = None
graph = None


# Step 1: Generate an AIMessage that may include a tool-call to be sent.
def query_or_respond(state: MessagesState):
    """Generate tool call for retrieval or respond."""
    llm_with_tools = llm.bind_tools([get_tasks, get_tasks_for_team, get_tasks_for_person, create_graph])
    response = llm_with_tools.invoke(state["messages"])
    # MessagesState appends messages to state instead of overwriting
    return {"messages": [response]}


# Step 2: Execute the retrieval.
tools = ToolNode([get_tasks, get_tasks_for_team, get_tasks_for_person, create_graph])


# Step 3: Generate a response using the retrieved content.
def generate(state: MessagesState):
    """Generate answer."""
    # Get generated ToolMessages
    recent_tool_messages = []
    for message in reversed(state["messages"]):
        if message.type == "tool":
            recent_tool_messages.append(message)
        else:
            break
    tool_messages = recent_tool_messages[::-1]

    # Format into prompt
    docs_content = "\n\n".join(doc.content for doc in tool_messages if doc.content != [])
    system_message_content = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise. "
        "If a tool for drawing chart was called, do not answer that you don't have drawing capabilities. "
        "\n\n"
        f"{docs_content}"
    )
    conversation_messages = [
        message
        for message in state["messages"]
        if (message.type in ("human", "system")) or (message.type == "ai" and not message.tool_calls)
    ]
    prompt = [SystemMessage(system_message_content)] + conversation_messages

    # Run
    response = llm.invoke(prompt)
    return {"messages": [response]}


def build_graph():
    graph_builder = StateGraph(MessagesState)
    graph_builder.add_node(query_or_respond)
    graph_builder.add_node(tools)
    graph_builder.add_node(generate)

    graph_builder.set_entry_point("query_or_respond")
    graph_builder.add_conditional_edges(
        "query_or_respond",
        tools_condition,
        {END: END, "tools": "tools"}
    )
    graph_builder.add_edge("tools", "generate")
    graph_builder.add_edge("generate", END)

    # print(graph.get_graph().draw_ascii())
    memory = MemorySaver()
    return graph_builder.compile(checkpointer=memory)


def setup_llm():
    print("setup the llm")
    global llm
    # select an llm model of your choice
    llm = init_chat_model("gpt-4o-mini", model_provider="openai")
    # llm = init_chat_model(model="gemini-2.0-flash-001", model_provider="google_vertexai")
    global graph
    graph = build_graph()


def ask(query):
    answer = []
    for step in graph.stream(
            {"messages": [{"role": "user", "content": query}]},
            {"configurable": {"thread_id": "1"}},
            stream_mode="values"
    ):
        message = step["messages"][-1]
        # message.pretty_print()
        if isinstance(message, AIMessage) and message.tool_calls == []:
            answer.append(message.content)

    return "\n\n".join(ans for ans in answer)
