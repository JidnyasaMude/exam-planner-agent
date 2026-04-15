import streamlit as st
from agent.graph import build_agent

st.set_page_config(page_title="Exam Study Planner Agent", page_icon="📚")
st.title("📚 Competitive Exam Study Planner")
st.write("Powered by 4 AI agents working together.")

with st.form("planner_form"):
    exam_name = st.selectbox(
        "Select Your Exam",
        ["GATE CSE", "GATE ECE", "CAT", "UPSC", "JEE", "NEET", "Other"]
    )

    weeks_available = st.number_input(
        "Weeks available for preparation",
        min_value=1,
        max_value=52,
        value=8
    )

    weak_topics_input = st.text_area(
        "Your Weak Topics (one per line)",
        placeholder="Operating Systems\nComputer Networks\nDBMS"
    )

    hours_per_day = st.slider(
        "Study hours available per day",
        min_value=1,
        max_value=12,
        value=4
    )

    submitted = st.form_submit_button("🚀 Generate My Study Plan")

if submitted:
    if not weak_topics_input:
        st.error("Please enter at least one weak topic.")
    else:
        weak_topics = [
            t.strip()
            for t in weak_topics_input.strip().split("\n")
            if t.strip()
        ]

        agent = build_agent()

        initial_state = {
            "exam_name": exam_name,
            "weeks_available": int(weeks_available),
            "weak_topics": weak_topics,
            "hours_per_day": int(hours_per_day),
            "syllabus": "",
            "prioritized_topics": "",
            "study_plan": "",
            "evaluation": "",
            "current_step": "Starting..."
        }

        with st.status("4 Agents are working...", expanded=True) as status:
            st.write("🔍 Agent 1: Researching syllabus...")
            st.write("📊 Agent 2: Prioritizing topics...")
            st.write("📅 Agent 3: Building study plan...")
            st.write("⚖️ Agent 4: Evaluating plan...")

            final_state = agent.invoke(initial_state)
            status.update(label="All agents done!", state="complete")

        # Show syllabus
        with st.expander("📋 Syllabus Found (Agent 1)"):
            st.markdown(final_state["syllabus"])

        # Show prioritized topics
        with st.expander("📊 Topic Priority List (Agent 2)"):
            st.markdown(final_state["prioritized_topics"])

        # Show study plan
        st.subheader("📅 Your Week-by-Week Study Plan (Agent 3)")
        st.markdown(final_state["study_plan"])

        # Show evaluation
        st.subheader("⚖️ Plan Evaluation (Agent 4 — Judge)")
        evaluation = final_state["evaluation"]

        if "Score:" in evaluation:
            for line in evaluation.split("\n"):
                if "Score:" in line:
                    try:
                        score_val = int(line.split(":")[1].strip().split("/")[0])
                        if score_val >= 8:
                            st.success(f"✅ {line}")
                        elif score_val >= 5:
                            st.warning(f"⚠️ {line}")
                        else:
                            st.error(f"❌ {line}")
                    except:
                        st.info(line)
                elif line.strip():
                    st.write(line)