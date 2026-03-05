from graph import graph

initial_state = {
    "bug_report": """
Several functions in the ecommerce utility module produce incorrect results.
Price calculations, averages, cart totals, and user filtering are incorrect.
Fix the bugs.
""",
    "code": "",
    "docs": "",
    "fix": "",
    "tests": "",
    "test_result": "",
    "approved": False
}

config = {"configurable": {"thread_id": "1"}}

result = graph.invoke(initial_state, config)

print("\nFinal State:\n")
print(result)