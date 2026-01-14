import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/tasks"

st.title("Task Manager Dashboard")

if "refresh" not in st.session_state:
    st.session_state.refresh = 0

def refresh_page():
    st.session_state.refresh += 1  # triggers Streamlit to rerun

# --- Add Task ---
st.subheader("Add a New Task")
task_name = st.text_input("Task Name")
if st.button("Add Task"):
    if task_name:
        response = requests.post(API_URL, json={"name": task_name})
        if response.status_code == 200:
            st.success(f"Task added: {response.json()}")
        else:
            st.error("Failed to add task")
        refresh_page()  # rerun after adding

# --- List Tasks ---
st.subheader("All Tasks")
tasks = requests.get(API_URL).json()
for task in tasks:
    col1, col2, col3 = st.columns([3,1,1])
    col1.write(f"{task['id']}: {task['name']} - {'✅' if task['completed'] else '❌'}")
    if col2.button("Complete", key=f"complete-{task['id']}"):
        requests.put(f"{API_URL}/{task['id']}/complete")
        refresh_page()  # rerun after completing
    if col3.button("Delete", key=f"delete-{task['id']}"):
        requests.delete(f"{API_URL}/{task['id']}")
        refresh_page()  # rerun after deleting
