import os
from dotenv import load_dotenv
import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI

from tools import read_code, search_docs, run_python
from state import AgentState

load_dotenv()

# -------- LLM --------

llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    google_api_key=st.secrets["GEMINI_API_KEY"],
    temperature=0,
)

# -------- Helpers --------

def clean_code(text):
    """
    Gemini sometimes returns lists or dict blocks.
    Convert everything safely to a clean string.
    """

    if isinstance(text, list):
        text = " ".join(
            item.get("text", str(item)) if isinstance(item, dict) else str(item)
            for item in text
        )

    text = str(text)

    text = text.replace("```python", "")
    text = text.replace("```", "")

    return text.strip()


# -------- Nodes --------

def analyze_code(state: AgentState):

    code = read_code(state["file_path"])

    prompt = f"""
You are a senior software engineer.

Bug Report:
{state['bug_report']}

Code:
{code}

Explain what might be causing the bug.
Keep the explanation short and technical.
"""

    response = llm.invoke(prompt)

    analysis = clean_code(response.content)

    return {
        "code": code,
        "analysis": analysis
    }


def search_documentation(state: AgentState):

    docs = search_docs(state["bug_report"])

    return {"docs": docs}


def generate_fix(state: AgentState):

    prompt = f"""
You are an expert Python debugger.

Bug Report:
{state['bug_report']}

Bug Analysis:
{state['analysis']}

Code:
{state['code']}

Docs:
{state['docs']}

Generate a corrected version of the code.

Rules:
- Return ONLY Python code
- No markdown
- No explanations
"""

    response = llm.invoke(prompt)

    fix = clean_code(response.content)

    return {"fix": fix}


def generate_tests(state: AgentState):

    prompt = f"""
Write a Python script to test this code.

Rules:
- Return ONLY executable Python code
- No markdown
- No explanations
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
