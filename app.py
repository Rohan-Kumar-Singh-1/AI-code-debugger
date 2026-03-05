import streamlit as st
from graph import graph

st.title("🤖 AI Debug Agent")
st.write("Upload buggy code and describe the bug.")

# Persist results and filename across reruns
if "result" not in st.session_state:
    st.session_state.result = None

if "filename" not in st.session_state:
    st.session_state.filename = None


bug_report = st.text_area("Bug Report")

uploaded_file = st.file_uploader("Upload Python file", type=["py"])

run_agent = st.button("Run Debug Agent")


# Run agent
if run_agent and uploaded_file:

    code = uploaded_file.read().decode()

    # Save uploaded file locally using its original name
    file_path = uploaded_file.name

    with open(file_path, "w") as f:
        f.write(code)

    # Store filename for later patching
    st.session_state.filename = file_path

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


# Display results
if st.session_state.result:

    result = st.session_state.result

    st.subheader("Generated Fix")
    st.code(result["fix"], language="python")
    # DOWNLOAD BUTTON
    st.download_button(
        label="⬇ Download Debugged File",
        data=result["fix"],
        file_name=f"fixed_{st.session_state.filename}",
        mime="text/x-python"
    )
    
    st.subheader("Test Results")
    st.text(result["test_result"])

    col1, col2 = st.columns(2)

    # approve = col1.button("✅ Approve Patch")
    # reject = col2.button("❌ Reject Patch")

    # if approve:

    #     file_path = st.session_state.filename

    #     with open(file_path, "w") as f:
    #         f.write(result["fix"])

    #     st.success(f"Patch applied successfully to {file_path}")

    # if reject:
    #     st.warning("Fix rejected. You can run the agent again.")

