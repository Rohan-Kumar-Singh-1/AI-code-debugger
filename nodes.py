import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from tools import read_code, search_docs, run_python, apply_patch
from state import AgentState

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def clean_code(text):
    text = text.replace("```python", "")
    text = text.replace("```", "")
    return text.strip()

def analyze_code(state: AgentState):

    code = read_code(state["file_path"])

    prompt = f"""
Bug Report:
{state['bug_report']}

Code:
{code}

Explain what might be causing the bug.
"""

    response = llm.invoke(prompt)

    return {"code": code}


def search_documentation(state: AgentState):

    docs = search_docs(state["bug_report"])

    return {"docs": docs}


def generate_fix(state: AgentState):

    prompt = f"""
Bug Report:
{state['bug_report']}

Code:
{state['code']}

Docs:
{state['docs']}

Generate a corrected version of the code.
Return ONLY python code.
"""

    response = llm.invoke(prompt)

    fix = clean_code(response.content)
    return {"fix": fix}


def generate_tests(state: AgentState):

    prompt = f"""
    Write a Python script to test this code.

    Rules:
    - Return ONLY executable Python code
    - Do NOT include explanations
    - Do NOT include markdown
    - Print PASS if all tests succeed
    - Print FAIL if any test fails

Code:
{state['fix']}
"""

    response = llm.invoke(prompt)

    tests = clean_code(response.content)
    return {"tests": tests}


def test_fix(state: AgentState):

    test_script = f"""
{state['fix']}

{state['tests']}
"""

    result = run_python(test_script)

    return {"test_result": result}