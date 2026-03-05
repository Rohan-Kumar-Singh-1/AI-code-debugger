import streamlit as st
from graph import graph
from database import init_db, save_session, get_sessions, get_session_by_id
from auth import login_page

init_db()

# -------------------------
# Initialize session variables
# -------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "user_id" not in st.session_state:
    st.session_state.user_id = None

# -------------------------
# LOGIN CHECK
# -------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_page()
    st.stop()

# -------------------------
# App Header
# -------------------------

st.title("🤖 AI Debug Agent")
st.write("Upload buggy code and describe the bug.")

# -------------------------
# Session State
# -------------------------

if "result" not in st.session_state:
    st.session_state.result = None

if "filename" not in st.session_state:
    st.session_state.filename = None

if "code" not in st.session_state:
    st.session_state.code = None

if "saved" not in st.session_state:
    st.session_state.saved = False


# -------------------------
# Sidebar
# -------------------------

st.sidebar.write(f"👤 Logged in as: {st.session_state.user}")

# Logout button
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.user_id = None
    st.rerun()

st.sidebar.divider()

st.sidebar.title("🗂 Session History")

# ➕ NEW CHAT BUTTON
if st.sidebar.button("➕ New Chat"):

    st.session_state.result = None
    st.session_state.code = None
    st.session_state.filename = None
    st.session_state.saved = False

    st.rerun()

st.sidebar.divider()

# Load sessions for current user
sessions = get_sessions(st.session_state.user_id)

session_options = {
    f"{s['title']}": s["id"]
    for s in sessions
}

selected_session = st.sidebar.selectbox(
    "View Previous Session",
    ["None"] + list(session_options.keys())
)


# -------------------------
# Main UI
# -------------------------

bug_report = st.text_area("Bug Report")
uploaded_file = st.file_uploader("Upload Python file", type=["py"])

run_agent = st.button("Run Debug Agent")


# -------------------------
# Run Agent
# -------------------------

if run_agent and uploaded_file:

    code = uploaded_file.read().decode()
    st.session_state.code = code

    file_path = uploaded_file.name

    with open(file_path, "w") as f:
        f.write(code)

    st.session_state.filename = file_path
    st.session_state.saved = False

    initial_state = {
        "bug_report": bug_report,
        "file_path": file_path,
        "code": "",
        "docs": "",
        "fix": "",
        "tests": "",
        "test_result": "",
        "approved": False
    }

    config = {"configurable": {"thread_id": "1"}}

    status_box = st.empty()

    steps = {
        "analyze_code": "🔍 Analyzing code...",
        "search_docs": "📚 Searching documentation...",
        "generate_fix": "🛠 Generating fix...",
        "generate_tests": "🧪 Generating tests...",
        "test_fix": "⚙ Running tests..."
    }

    final_result = {}

    for event in graph.stream(initial_state, config):

        for node, output in event.items():

            if node in steps:
                status_box.info(steps[node])

            if output:
                final_result.update(output)

    st.session_state.result = final_result


# -------------------------
# Display Agent Result
# -------------------------

if st.session_state.result:

    result = st.session_state.result

    st.subheader("Generated Fix")
    st.code(result["fix"], language="python")

    st.download_button(
        label="⬇ Download Debugged File",
        data=result["fix"],
        file_name=f"fixed_{st.session_state.filename}",
        mime="text/x-python"
    )

    st.subheader("Test Results")
    st.text(result["test_result"])

    # Save session only once
    if not st.session_state.saved:

        save_session(
            st.session_state.user_id,
            bug_report,
            st.session_state.code,
            result["fix"],
            result["tests"],
            result["test_result"]
        )

        st.session_state.saved = True


# -------------------------
# Show Selected Session
# -------------------------

if selected_session != "None":

    session_id = session_options[selected_session]

    session = get_session_by_id(session_id)

    st.subheader(session["title"])

    st.write("Bug Report")
    st.write(session["bug_report"])

    st.subheader("Original Code")
    st.code(session["original_code"], language="python")

    st.subheader("Generated Fix")
    st.code(session["generated_fix"], language="python")

    st.subheader("Generated Tests")
    st.code(session["tests"], language="python")

    st.subheader("Test Result")
    st.text(session["test_result"])
