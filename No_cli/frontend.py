import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/tasks"

# Page config
st.set_page_config(page_title="Task Manager", page_icon="📋", layout="wide")
st.title("📋 Task Manager Dashboard")

# -----------------------------
# Session state trigger for refresh
# -----------------------------
if "refresh" not in st.session_state:
    st.session_state.refresh = 0

def trigger_refresh():
    st.session_state.refresh += 1

# -----------------------------
# Add Task Form
# -----------------------------
with st.expander("➕ Add a New Task", expanded=True):
    with st.form("add_task_form"):
        task_name = st.text_input("Task Name")
        submitted = st.form_submit_button("Add Task")
        if submitted and task_name.strip():
            try:
                requests.post(API_URL, json={"name": task_name.strip()})
                st.success(f"Task added: {task_name.strip()}")
                trigger_refresh()  # refresh UI
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to backend.")

# -----------------------------
# Fetch tasks from backend
# -----------------------------
try:
    tasks = requests.get(API_URL).json()
except requests.exceptions.ConnectionError:
    st.error("Cannot connect to backend.")
    st.stop()

pending_tasks = [t for t in tasks if not t["completed"]]
completed_tasks = [t for t in tasks if t["completed"]]

# -----------------------------
# Display Pending Tasks (Dark Theme)
# -----------------------------
st.subheader("🕒 Pending Tasks")
if pending_tasks:
    for task in pending_tasks:
        with st.container():
            st.markdown(
                f"""
                <div style="padding:10px; border:2px solid #444; border-radius:10px; 
                            background-color:#1E1E1E; color:#FFFFFF">
                    <b>{task['id']}: {task['name']}</b>
                </div>
                """,
                unsafe_allow_html=True,
            )
        col1, col2 = st.columns([1, 1])
        if col1.button("✅ Complete", key=f"complete-{task['id']}"):
            requests.put(f"{API_URL}/{task['id']}/complete")
            trigger_refresh()
        if col2.button("🗑 Delete", key=f"delete-{task['id']}"):
            requests.delete(f"{API_URL}/{task['id']}")
            trigger_refresh()
else:
    st.info("No pending tasks!")

# -----------------------------
# Display Completed Tasks (Dark Theme)
# -----------------------------
st.subheader("✅ Completed Tasks")
if completed_tasks:
    for task in completed_tasks:
        with st.container():
            st.markdown(
                f"""
                <div style="padding:10px; border:2px solid #444; border-radius:10px; 
                            background-color:#2E2E2E; color:#FFFFFF">
                    <b>{task['id']}: {task['name']}</b>
                </div>
                """,
                unsafe_allow_html=True,
            )
        if st.button("🗑 Delete", key=f"delete-completed-{task['id']}"):
            requests.delete(f"{API_URL}/{task['id']}")
            trigger_refresh()
else:
    st.info("No completed tasks!")

