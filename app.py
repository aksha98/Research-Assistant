import streamlit as st
from graph import build_graph
from agents import memory

st.set_page_config(page_title="Deep Research Assistant", layout="wide")

st.markdown(
    """
    <style>
    .main {
        background-color: #f9f9f9;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stButton button {
        background-color: #0066cc;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        margin-top: 1rem;
    }
    .stButton button:hover {
        background-color: #005bb5;
        color: #ffffff;
    }
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border: 1px solid #ccc;
        border-radius: 8px;
        padding: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.header("📂 Research History")
    st.markdown("---")
    if st.session_state.chat_history:
        for idx, entry in enumerate(st.session_state.chat_history):
            with st.expander(f"🔎 {entry['query']}"):
                st.markdown(f"**Final Answer:**")
                st.info(entry['answer'])
    else:
        st.info("No previous research queries.")

    if st.button("🗑️ Clear History"):
        st.session_state.chat_history = []
        st.success("Chat history cleared.")

st.title("💬 Deep Research Assistant")
st.caption("An AI-powered system for multi-step research, refinement, and fact-checking.")

st.markdown("### Enter your research query:")
query = st.text_input("", placeholder="Type your research topic here...")

col1, col2 = st.columns([1, 6])
with col1:
    run_clicked = st.button("Run Research")

if run_clicked:
    if not query.strip():
        st.warning("⚠️ Please enter a valid research query.")
    else:
        graph = build_graph()
        with st.spinner("🔄 Processing your research..."):
            result = graph.invoke({"query": query})
            final_answer = result["answer"]

        st.markdown("---")
        st.subheader("📜 Final Answer")
        st.success(final_answer)

        st.session_state.chat_history.append({
            "query": query,
            "answer": final_answer
        })

