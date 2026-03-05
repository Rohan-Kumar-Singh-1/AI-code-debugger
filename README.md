This repository contains the **AI Debug Agent**, a specialized tool built with **LangGraph** and **Streamlit** that automatically analyzes buggy Python code, researches potential fixes, and runs tests to verify solutions.

---

## 🤖 AI Debug Agent

The AI Debug Agent uses a state-of-the-art agentic workflow to handle the heavy lifting of debugging. By combining Large Language Models (LLMs) with actual code execution, it ensures that proposed fixes aren't just syntactically correct, but functionally sound.

### 🌟 Key Features

* 
**Self-Healing Loop**: If generated tests fail, the agent automatically loops back to refine the fix based on the error output.


* 
**Contextual Research**: Integrated with DuckDuckGo Search to find documentation for specific libraries or error messages.


* 
**Session Persistence**: SQLite integration to save bug reports, original code, fixes, and test results for future reference.


* 
**Secure Authentication**: A built-in user system to manage individual session histories.


* 
**Live Progress**: Real-time status updates in the UI as the agent moves through the debugging stages.



---

### 🛠 Architecture

The application is powered by **LangGraph**, which manages the logic as a state machine:

| Node | Responsibility |
| --- | --- |
| **Analyze** | Reads the code and the user's bug report to identify the root cause.

 |
| **Search Docs** | Performs a web search to gather technical context or documentation.

 |
| **Generate Fix** | Writes a corrected version of the Python script. |
| **Generate Tests** | Creates executable tests (assertions) specifically for the new fix. |
| **Test Fix** | Executes the code in a temporary environment and returns the result.

 |

---

### 🚀 Getting Started

#### 1. Prerequisites

Ensure you have an **OpenRouter API Key** (or modify `nodes.py` to use a direct OpenAI key).

#### 2. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-debug-agent.git
cd ai-debug-agent

# Install dependencies
pip install -r requirements.txt

```

#### 3. Environment Setup

Create a `.env` file in the root directory:

```env
OPENROUTER_API_KEY=your_api_key_here

```

#### 4. Run the App

```bash
streamlit run app.py

```

---

### 📂 File Structure

* 
`app.py`: The Streamlit frontend and main entry point.


* 
`graph.py`: Defines the LangGraph state machine and conditional routing logic.


* `nodes.py`: Contains the LLM logic for each step of the debugging process.
* 
`database.py`: Manages the SQLite schema for users and sessions.


* `tools.py`: Helper functions for reading files, searching the web, and running subprocesses.

---

### 🛡 Example Usage

1. **Login** or **Register** a new account.
2. **Upload** a Python file (e.g., a script throwing a `RuntimeError` while iterating over a dictionary).
3. **Describe** the issue (e.g., "The code crashes when trying to remove items from a dict").
4. 
**Run Agent** and watch as it researches the error and provides a "PASS" verified fix.



Would you like me to help you draft the `LICENSE` file for this repository as well?
