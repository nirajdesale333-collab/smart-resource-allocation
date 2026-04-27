import streamlit as st
import pandas as pd

st.set_page_config(page_title="Smart Resource Allocation", layout="wide")

st.title("🌍 Smart Resource Allocation")
st.subheader("Data-driven Volunteer Coordination for Social Impact")

# -------------------------
# Volunteer Input
# -------------------------
st.sidebar.header("Add Volunteer")

name = st.sidebar.text_input("Name")
skill = st.sidebar.selectbox("Skill", ["Education", "Medical", "Logistics", "Technical"])
availability = st.sidebar.selectbox("Availability", ["Full-time", "Part-time"])
location = st.sidebar.text_input("Location")
experience = st.sidebar.selectbox("Experience", ["Beginner", "Intermediate", "Expert"])

if st.sidebar.button("Add Volunteer"):
    if "volunteers" not in st.session_state:
        st.session_state.volunteers = []

    st.session_state.volunteers.append({
        "Name": name,
        "Skill": skill,
        "Availability": availability,
        "Location": location,
        "Experience": experience
    })

# -------------------------
# Task Input
# -------------------------
st.sidebar.header("Add Task")

task_name = st.sidebar.text_input("Task Name")
req_skill = st.sidebar.selectbox("Required Skill", ["Education", "Medical", "Logistics", "Technical"])
priority = st.sidebar.selectbox("Priority", ["High", "Medium", "Low"])
task_location = st.sidebar.text_input("Task Location")

if st.sidebar.button("Add Task"):
    if "tasks" not in st.session_state:
        st.session_state.tasks = []

    st.session_state.tasks.append({
        "Task": task_name,
        "Skill": req_skill,
        "Priority": priority,
        "Location": task_location
    })

# -------------------------
# Display Data
# -------------------------
st.header("📋 Volunteers")
if "volunteers" in st.session_state:
    df_v = pd.DataFrame(st.session_state.volunteers)
    st.dataframe(df_v)

st.header("🛠 Tasks")
if "tasks" in st.session_state:
    df_t = pd.DataFrame(st.session_state.tasks)
    st.dataframe(df_t)

# -------------------------
# Allocation Logic
# -------------------------
st.header("⚡ Smart Allocation")

if st.button("Run Allocation"):
    if "volunteers" in st.session_state and "tasks" in st.session_state:
        allocations = []

        for task in st.session_state.tasks:
            for vol in st.session_state.volunteers:
                if vol["Skill"] == task["Skill"]:
                    allocations.append({
                        "Task": task["Task"],
                        "Volunteer": vol["Name"],
                        "Skill": vol["Skill"]
                    })

        if allocations:
            df_alloc = pd.DataFrame(allocations)
            st.success("✅ Allocation Done")
            st.dataframe(df_alloc)

            # Simple fairness check
            skill_counts = df_alloc["Skill"].value_counts()
            if len(skill_counts) > 1 and skill_counts.max() - skill_counts.min() > 2:
                st.error("⚠ Bias Detected in Allocation")
            else:
                st.success("🎉 Fair Allocation")
        else:
            st.warning("No matching volunteers found")
