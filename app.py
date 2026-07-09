"""
AI Interview Simulator — Main Streamlit App
"""

import streamlit as st
from interviewer import generate_question, evaluate_answer, generate_final_report
from question_bank import ROLES, DIFFICULTY_LEVELS

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Interview Simulator",
    page_icon="🎤",
    layout="centered"
)

# ─────────────────────────────────────────────
# Session State Initialisation
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "stage": "setup",           # setup / interview / results
        "role": None,
        "difficulty": None,
        "total_questions": 7,
        "current_question_num": 1,
        "current_question": None,
        "questions": [],
        "answers": [],
        "evaluations": [],
        "scores": [],
        "covered_topics": [],
        "final_report": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

# ─────────────────────────────────────────────
# STAGE 1: Setup
# ─────────────────────────────────────────────
if st.session_state.stage == "setup":
    st.title("🎤 AI Interview Simulator")
    st.markdown("*Practice technical interviews with AI — get scored in real time*")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        role = st.selectbox("🎯 Select Role", ROLES)
        difficulty = st.selectbox("📊 Difficulty", DIFFICULTY_LEVELS)

    with col2:
        total_questions = st.slider("❓ Number of Questions", 3, 10, 7)
        st.markdown("<br>", unsafe_allow_html=True)
        st.info(f"⏱️ Estimated time: **{total_questions * 3}-{total_questions * 5} minutes**")

    st.divider()
    st.markdown("### 📋 How it works")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**1️⃣ Answer**\nType your answer to each question")
    with col2:
        st.markdown("**2️⃣ Get Scored**\nAI scores 1-10 with feedback")
    with col3:
        st.markdown("**3️⃣ Final Report**\nGet overall assessment + tips")

    st.divider()

    if st.button("🚀 Start Interview", type="primary", use_container_width=True):
        st.session_state.role = role
        st.session_state.difficulty = difficulty
        st.session_state.total_questions = total_questions
        st.session_state.stage = "interview"

        with st.spinner("Generating your first question..."):
            question = generate_question(
                role, difficulty, [],
                1, total_questions
            )
            st.session_state.current_question = question

        st.rerun()

# ─────────────────────────────────────────────
# STAGE 2: Interview
# ─────────────────────────────────────────────
elif st.session_state.stage == "interview":
    # Header
    st.title("🎤 AI Interview Simulator")

    # Progress
    q_num = st.session_state.current_question_num
    total = st.session_state.total_questions
    progress = (q_num - 1) / total

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.progress(progress, text=f"Question {q_num} of {total}")
    with col2:
        st.metric("Role", st.session_state.role)
    with col3:
        st.metric("Difficulty", st.session_state.difficulty)

    st.divider()

    # Current Question
    st.markdown(f"### ❓ Question {q_num}")
    st.info(st.session_state.current_question)

    # Answer Input
    answer = st.text_area(
        "💬 Your Answer",
        placeholder="Type your answer here... Be as detailed as possible.",
        height=200,
        key=f"answer_{q_num}"
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        submit = st.button("✅ Submit Answer", type="primary", use_container_width=True, disabled=not answer)
    with col2:
        skip = st.button("⏭️ Skip", use_container_width=True)

    # Process submission
    if submit and answer:
        with st.spinner("🤔 Evaluating your answer..."):
            evaluation = evaluate_answer(
                st.session_state.role,
                st.session_state.current_question,
                answer
            )

        # Store results
        st.session_state.questions.append(st.session_state.current_question)
        st.session_state.answers.append(answer)
        st.session_state.evaluations.append(evaluation)
        st.session_state.scores.append(evaluation.get("score", 5))

        # Show evaluation
        score = evaluation.get("score", 5)
        verdict = evaluation.get("verdict", "Average")

        # Score display
        if score >= 8:
            st.success(f"### ⭐ Score: {score}/10 — {verdict}")
        elif score >= 6:
            st.warning(f"### 📊 Score: {score}/10 — {verdict}")
        else:
            st.error(f"### 📉 Score: {score}/10 — {verdict}")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**✅ Strengths:**")
            for s in evaluation.get("strengths", []):
                st.markdown(f"- {s}")
        with col2:
            st.markdown("**💡 Improve:**")
            for i in evaluation.get("improvements", []):
                st.markdown(f"- {i}")

        hint = evaluation.get("ideal_answer_hint", "")
        if hint:
            st.markdown(f"**🎯 Ideal answer hint:** *{hint}*")

        st.divider()

        # Next question or finish
        if q_num >= total:
            if st.button("📊 See Final Report", type="primary", use_container_width=True):
                with st.spinner("Generating your performance report..."):
                    report = generate_final_report(
                        st.session_state.role,
                        st.session_state.difficulty,
                        st.session_state.questions,
                        st.session_state.answers,
                        st.session_state.scores
                    )
                    st.session_state.final_report = report
                st.session_state.stage = "results"
                st.rerun()
        else:
            if st.button("➡️ Next Question", type="primary", use_container_width=True):
                st.session_state.current_question_num += 1
                with st.spinner("Generating next question..."):
                    next_q = generate_question(
                        st.session_state.role,
                        st.session_state.difficulty,
                        st.session_state.covered_topics,
                        st.session_state.current_question_num,
                        total
                    )
                    st.session_state.current_question = next_q
                st.rerun()

    if skip:
        st.session_state.questions.append(st.session_state.current_question)
        st.session_state.answers.append("(Skipped)")
        st.session_state.evaluations.append({"score": 0, "strengths": [], "improvements": ["Practice this topic"]})
        st.session_state.scores.append(0)

        if q_num >= total:
            st.session_state.stage = "results"
        else:
            st.session_state.current_question_num += 1
            with st.spinner("Generating next question..."):
                next_q = generate_question(
                    st.session_state.role,
                    st.session_state.difficulty,
                    st.session_state.covered_topics,
                    st.session_state.current_question_num,
                    total
                )
                st.session_state.current_question = next_q
        st.rerun()

    # Previous Q&A
    if st.session_state.questions:
        with st.expander(f"📝 Previous Questions ({len(st.session_state.questions)})"):
            for i, (q, a, s) in enumerate(zip(
                st.session_state.questions,
                st.session_state.answers,
                st.session_state.scores
            )):
                st.markdown(f"**Q{i+1}:** {q}")
                st.markdown(f"**Score:** {s}/10")
                st.divider()

# ─────────────────────────────────────────────
# STAGE 3: Results
# ─────────────────────────────────────────────
elif st.session_state.stage == "results":
    report = st.session_state.final_report
    scores = st.session_state.scores
    avg_score = sum(scores) / len(scores) if scores else 0

    st.title("📊 Interview Performance Report")
    st.markdown(f"**Role:** {st.session_state.role} | **Difficulty:** {st.session_state.difficulty}")
    st.divider()

    # Overall Score
    grade = report.get("overall_grade", "B")
    readiness = report.get("interview_readiness", "Almost Ready")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Score", f"{round(avg_score, 1)}/10")
    with col2:
        st.metric("Overall Grade", grade)
    with col3:
        st.metric("Readiness", readiness)

    st.divider()

    # Summary
    st.markdown("### 📝 Performance Summary")
    st.info(report.get("performance_summary", ""))

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### ✅ Top Strengths")
        for s in report.get("top_strengths", []):
            st.markdown(f"- {s}")

    with col2:
        st.markdown("### 💡 Areas to Improve")
        for a in report.get("areas_to_improve", []):
            st.markdown(f"- {a}")

    st.divider()

    st.markdown("### 📚 Study Recommendations")
    for rec in report.get("study_recommendations", []):
        st.markdown(f"- 📖 {rec}")

    st.divider()
    st.success(f"💪 {report.get('encouragement', 'Keep practising!')}")

    # Score breakdown
    with st.expander("📋 Full Q&A Transcript"):
        for i, (q, a, s) in enumerate(zip(
            st.session_state.questions,
            st.session_state.answers,
            st.session_state.scores
        )):
            st.markdown(f"**Q{i+1} (Score: {s}/10):** {q}")
            st.markdown(f"**Your answer:** {a}")
            st.divider()

    st.divider()
    if st.button("🔄 Start New Interview", type="primary", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
