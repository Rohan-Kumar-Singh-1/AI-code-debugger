import subprocess
import tempfile
import os


def read_code(file_path: str):
    with open(file_path, "r") as f:
        return f.read()


from ddgs import DDGS


def search_docs(query):

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))

        if not results:
            return "No documentation results found."

        docs = "\n".join(
            f"{r.get('title','')} - {r.get('body','')}"
            for r in results
        )

        return docs

    except Exception:
        return "Documentation search failed or returned no results."

def run_python(code: str):
    """
    Runs dynamically generated python tests
    """

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp:
            temp.write(code.encode())
            temp_path = temp.name

        result = subprocess.run(
            ["python", temp_path],
            capture_output=True,
            text=True
        )

        os.remove(temp_path)

        return result.stdout + result.stderr

    except Exception as e:
        return str(e)


def apply_patch(file_path: str, new_code: str):
    with open(file_path, "w") as f:
        f.write(new_code)


    return "Patch applied"
