from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from state import AgentState
from nodes import (
    analyze_code,
    search_documentation,
    generate_fix,
    generate_tests,
    test_fix
)


def test_router(state: AgentState):

    # If tests fail → generate another fix
    if "fail" in state["test_result"].lower():
        return "generate_fix"

    # If tests pass → stop graph
    return END


builder = StateGraph(AgentState)

builder.add_node("analyze_code", analyze_code)
builder.add_node("search_docs", search_documentation)
builder.add_node("generate_fix", generate_fix)
builder.add_node("generate_tests", generate_tests)
builder.add_node("test_fix", test_fix)


# Graph flow
builder.add_edge(START, "analyze_code")
builder.add_edge("analyze_code", "search_docs")
builder.add_edge("search_docs", "generate_fix")
builder.add_edge("generate_fix", "generate_tests")
builder.add_edge("generate_tests", "test_fix")


# Conditional loop
builder.add_conditional_edges(
    "test_fix",
    test_router,
    {
        "generate_fix": "generate_fix",
        END: END
    }
)


memory = MemorySaver()

graph = builder.compile(checkpointer=memory)