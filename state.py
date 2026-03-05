from typing import TypedDict

class AgentState(TypedDict):
    bug_report: str
    file_path: str
    code: str
    docs: str
    fix: str
    tests: str
    test_result: str
    approved: bool