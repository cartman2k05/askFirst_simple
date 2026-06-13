import requests
import streamlit as st

API = "https://your-app-name.onrender.com"

st.set_page_config(
    page_title="AI Chat"
)

st.title("AI Chat")

if st.sidebar.button("New Thread"):

    requests.post(
        f"{API}/threads"
    )

    st.rerun()

threads = requests.get(
    f"{API}/threads"
).json()

if len(threads) == 0:

    st.info("Create a thread.")

    st.stop()

thread_map = {
    f"Thread {t['id']}": t["id"]
    for t in threads
}

selected = st.sidebar.selectbox(
    "Threads",
    list(thread_map.keys())
)

thread_id = thread_map[selected]

if st.sidebar.button("Delete Thread"):

    requests.delete(
        f"{API}/threads/{thread_id}"
    )

    st.rerun()

history = requests.get(
    f"{API}/threads/{thread_id}"
).json()

for msg in history:

    with st.chat_message(
        msg["role"]
    ):
        st.write(
            msg["content"]
        )

prompt = st.chat_input(
    "Type..."
)

if prompt:

    requests.post(
        f"{API}/chat",
        json={
            "thread_id": thread_id,
            "message": prompt
        }
    )

    st.rerun()