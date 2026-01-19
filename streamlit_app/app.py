import streamlit as st
import tempfile
import os
from src.rag_setup import setup_retriever
from src.graph_builder import build_graph
import asyncio
import uuid

def run_async(coro):
    """
    Safe async runner for Streamlit.
    Creates and destroys its own event loop.
    """
    try:
        return asyncio.run(coro)
    except RuntimeError:
        # Fallback for environments with existing loops
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)

st.set_page_config(page_title="Seminar Report Generator")

st.title("📄 Seminar Report Generator")

uploaded_files = st.file_uploader(
    "Upload PDF papers for RAG",
    type=["pdf"],
    accept_multiple_files=True
)

topic = st.text_input("Enter Seminar Topic")

if st.button("Generate Report"):
    if not uploaded_files or not topic:
        st.warning("Please upload PDFs and enter a topic")
        st.stop()

    with tempfile.TemporaryDirectory() as tmpdir:
        for pdf in uploaded_files:
            with open(os.path.join(tmpdir, pdf.name), "wb") as f:
                f.write(pdf.read())

        retriever = setup_retriever(tmpdir)
        app = build_graph(retriever)

        initial_state = {
            "topic": topic,
            "outline": [],
            "current_section_index": 0,
            "current_section": "",
            "key_points": [],
            "rag_context": "",
            "web_context": "",
            "draft": "",
            "section_drafts": [],
            "final_paper": "",
            "is_valid": False,
            "feedback": "",
            "revision_count": 0
        }

        thread_id = st.session_state.get("thread_id")

        if not thread_id:
            thread_id = st.session_state["thread_id"] = str(uuid.uuid4())

        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

        with st.spinner("Generating report..."):
            final_state = run_async(
                app.ainvoke(initial_state, config=config)
            )

        st.success("Report Generated!")

        st.download_button(
            "Download Markdown",
            final_state["final_report"],
            file_name="seminar_report.md"
        )
