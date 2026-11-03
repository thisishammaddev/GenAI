"""Streamlit interface for Misconception Detective."""

from __future__ import annotations

import streamlit as st

try:
    from .agent import explain_diagnosis, get_practice_question, grade
    from .question_bank import GUIDES, TRACKS
except ImportError:  # pragma: no cover - fallback for direct script execution
    from agent import explain_diagnosis, get_practice_question, grade
    from question_bank import GUIDES, TRACKS


st.set_page_config(
    page_title="Misconception Detective",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root { color-scheme: dark; }
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp {
    color: #eef1fa;
    background:
      radial-gradient(900px 480px at 12% -12%, rgba(116, 89, 238, .19), transparent 70%),
      radial-gradient(680px 420px at 91% 9%, rgba(36, 198, 177, .11), transparent 72%),
      #0b0d17;
}
.block-container { max-width: 1110px; padding-top: 2.2rem; padding-bottom: 5rem; }
#MainMenu, footer, header { visibility: hidden; }
h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -.035em; }
h1 { font-size: clamp(2.6rem, 6vw, 4.8rem) !important; line-height: 1.04 !important; margin-bottom: .5rem !important; }
h2 { font-size: 1.75rem !important; }
p { color: #b9bed0; }
.brand { display:flex; align-items:center; gap:.72rem; color:#f8f8ff; font-family:'Space Grotesk',sans-serif; font-size:1.03rem; font-weight:700; letter-spacing:-.02em; }
.brand-mark { display:grid; place-items:center; width:33px; height:33px; border-radius:10px; color:#11131f; background:#b5a3ff; font-size:1.18rem; }
.topline { display:flex; justify-content:space-between; align-items:center; padding: .1rem 0 1.3rem; border-bottom: 1px solid #24283b; }
.top-tag { font-size:.72rem; letter-spacing:.14em; text-transform:uppercase; color:#9da4ba; }
.eyebrow { display:inline-block; font-size:.72rem; font-weight:700; letter-spacing:.17em; text-transform:uppercase; color:#b2a0ff; margin: 2.9rem 0 .9rem; }
.hero-title span { color:#b4a0ff; }
.hero-sub { max-width:680px; color:#aeb5ca; font-size:1.08rem; line-height:1.72; margin:.7rem 0 1.7rem; }
.section-label { color:#aeb5ca; font-size:.76rem; font-weight:700; letter-spacing:.14em; text-transform:uppercase; margin: 1.8rem 0 .75rem; }
.panel { padding: 1.4rem 1.5rem; border:1px solid #292e42; border-radius:20px; background:linear-gradient(145deg, #191d30, #141827); min-height:160px; }
.panel-number { color:#aa96ff; font-family:'Space Grotesk',sans-serif; font-size:.75rem; font-weight:700; margin-bottom:1.05rem; }
.panel-title { color:#f3f4fc; font-family:'Space Grotesk',sans-serif; font-size:1.23rem; font-weight:700; margin-bottom:.4rem; }
.panel-text { color:#a5acc0; font-size:.9rem; line-height:1.5; }
.stepper { display:flex; align-items:center; gap:.6rem; margin:1.2rem 0 1.7rem; flex-wrap:wrap; }
.step { color:#858da5; background:#151928; border:1px solid #2a2e41; border-radius:99px; padding:.48rem .78rem; font-size:.76rem; font-weight:700; }
.step.active { color:#e7ddff; border-color:#816fba; background:#302849; }
.step-sep { color:#5a6278; }
.question-meta { color:#ae9bff; font-size:.75rem; font-weight:700; letter-spacing:.13em; text-transform:uppercase; margin:1.2rem 0 .3rem; }
.question-prompt { color:#eef0fa; font-family:'Space Grotesk',sans-serif; font-size:1.21rem; font-weight:600; line-height:1.4; margin:.2rem 0 .7rem; }
.metric-box { padding:1.3rem 1.4rem; background:#181d2f; border:1px solid #2b3148; border-radius:17px; }
.metric-label { color:#9da6bc; font-size:.74rem; font-weight:700; text-transform:uppercase; letter-spacing:.11em; }
.metric-value { color:#f1f3ff; font-family:'Space Grotesk',sans-serif; font-size:2rem; font-weight:700; line-height:1.25; margin-top:.5rem; }
.metric-value.accent { color:#b6a2ff; }
.insight-label { color:#b6a2ff; font-size:.75rem; font-weight:700; text-transform:uppercase; letter-spacing:.14em; margin-bottom:.6rem; }
.answer-row { border-left:3px solid #7d85a4; background:#171b2b; padding:.75rem 1rem; border-radius:0 10px 10px 0; margin:.6rem 0; }
.answer-row.good { border-color:#48c7ad; }
.answer-row.bad { border-color:#ef9a93; }
.tiny { color:#858da5; font-size:.76rem; }
div[data-testid="stRadio"] { padding: .2rem .1rem .6rem; }
div[data-testid="stRadio"] label { border:1px solid #30364a; background:#171b2b; border-radius:12px; padding:.45rem .7rem; margin:.25rem 0; transition:.18s ease; }
div[data-testid="stRadio"] label:hover { border-color:#8e7bc9; background:#211d36; }
div[data-testid="stButton"] button[kind="primary"], div[data-testid="stFormSubmitButton"] button[kind="primary"] {
    background:#b6a2ff; color:#10111b; border:0; border-radius:11px; font-weight:700; padding:.7rem 1.2rem; box-shadow:0 7px 22px rgba(162,137,255,.18);
}
div[data-testid="stButton"] button[kind="primary"]:hover, div[data-testid="stFormSubmitButton"] button[kind="primary"]:hover { background:#c7b7ff; color:#10111b; }
div[data-testid="stButton"] button[kind="secondary"] { background:#202538; border:1px solid #3a4057; color:#e4e5f3; border-radius:11px; }
div[data-testid="stSelectbox"] > div { background:#171b2b; }
.stAlert { border-radius:13px; }
@media (max-width: 700px) { .block-container { padding:1.2rem 1rem 3rem; } .top-tag { display:none; } .eyebrow { margin-top:2rem; } }
</style>
""",
    unsafe_allow_html=True,
)


def reset() -> None:
    for key in ("stage", "result", "coach_text", "coach_error", "practice_answer", "track"):
        st.session_state.pop(key, None)
    st.session_state.stage = "intro"


if "stage" not in st.session_state:
    st.session_state.stage = "intro"

st.markdown(
    '<div class="topline"><div class="brand"><div class="brand-mark">◈</div> Misconception Detective</div><div class="top-tag">Learn the reason behind the mistake</div></div>',
    unsafe_allow_html=True,
)


def stepper(stage: str) -> None:
    steps = [("01  Choose", "intro"), ("02  Diagnose", "quiz"), ("03  Practice", "result")]
    active = "result" if stage == "practice" else stage
    pieces = []
    for index, (label, name) in enumerate(steps):
        if index:
            pieces.append('<span class="step-sep">/</span>')
        pieces.append(f'<span class="step {"active" if name == active else ""}">{label}</span>')
    st.markdown('<div class="stepper">' + "".join(pieces) + "</div>", unsafe_allow_html=True)


if st.session_state.stage == "intro":
    st.markdown('<div class="eyebrow">Adaptive learning lab · v1</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">Find the <span>why</span> behind<br>every wrong answer.</h1>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">A short quiz reveals the concept you may be mixing up. Get a clear explanation, then prove you understand it with one focused question.</div>', unsafe_allow_html=True)
    stepper("intro")

    st.markdown('<div class="section-label">Choose a learning track</div>', unsafe_allow_html=True)
    track = st.selectbox(
        "Learning track",
        options=list(TRACKS),
        format_func=lambda name: f"{name}  ·  {TRACKS[name]['subtitle']}",
        label_visibility="collapsed",
    )
    st.caption(f"{len(TRACKS[track]['questions'])} questions · about 5 minutes · instant feedback")
    if st.button("Start diagnosis  ↗", type="primary", use_container_width=False):
        st.session_state.track = track
        st.session_state.stage = "quiz"
        st.rerun()

    st.markdown('<div class="section-label">How it works</div>', unsafe_allow_html=True)
    cols = st.columns(3, gap="medium")
    cards = [
        ("01 / ANSWER", "Quick check", "Answer a short quiz designed to reveal common mix-ups."),
        ("02 / UNDERSTAND", "Pattern found", "See the likely misconception and the correct mental model."),
        ("03 / IMPROVE", "Targeted retest", "Try one new question on the exact concept you missed."),
    ]
    for col, (number, title, body) in zip(cols, cards):
        with col:
            st.markdown(f'<div class="panel"><div class="panel-number">{number}</div><div class="panel-title">{title}</div><div class="panel-text">{body}</div></div>', unsafe_allow_html=True)

elif st.session_state.stage == "quiz":
    track = st.session_state.track
    questions = TRACKS[track]["questions"]
    st.markdown('<div class="eyebrow">Knowledge check</div>', unsafe_allow_html=True)
    st.title(track)
    st.caption("Pick one answer for each question. Your result stays in this browser session.")
    stepper("quiz")

    with st.form("quiz_form"):
        answers = {}
        for index, question in enumerate(questions, 1):
            st.markdown(f'<div class="question-meta">Question {index:02d} / {len(questions):02d}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="question-prompt">{question.prompt}</div>', unsafe_allow_html=True)
            answer = st.radio(
                question.prompt,
                options=list(range(4)),
                format_func=lambda option, q=question: q.options[option],
                index=None,
                key=f"answer_{question.id}",
                label_visibility="collapsed",
            )
            answers[question.id] = answer
            st.divider()
        submitted = st.form_submit_button("Reveal my learning pattern  ↗", type="primary")

    if submitted:
        if any(answer is None for answer in answers.values()):
            st.warning("Answer every question before continuing.")
        else:
            result = grade(questions, answers)
            st.session_state.result = result
            st.session_state.coach_text = None
            st.session_state.coach_error = None
            if result["focus"]:
                with st.spinner("Detecting your learning pattern..."):
                    try:
                        st.session_state.coach_text = explain_diagnosis(result, track)
                    except Exception as exc:
                        st.session_state.coach_error = str(exc)
            st.session_state.stage = "result"
            st.rerun()

    if st.button("← Change track", type="secondary"):
        reset()
        st.rerun()

else:
    result = st.session_state.result
    focus = result["focus"]
    st.markdown('<div class="eyebrow">Your learning report</div>', unsafe_allow_html=True)
    st.title("Pattern detected." if focus else "Clean sweep.")
    st.caption(f"{st.session_state.track} · personal result")
    stepper("result")

    metric_cols = st.columns(3, gap="medium")
    metrics = [
        ("Quiz score", f"{result['score']} / {result['total']}", False),
        ("Concepts to review", str(len(result["misses"])), True),
        ("Next step", "Focused retest" if focus else "New track", False),
    ]
    for col, (label, value, accent) in zip(metric_cols, metrics):
        with col:
            st.markdown(f'<div class="metric-box"><div class="metric-label">{label}</div><div class="metric-value {"accent" if accent else ""}">{value}</div></div>', unsafe_allow_html=True)

    if focus:
        st.markdown('<div class="section-label">Your focus concept</div>', unsafe_allow_html=True)
        st.subheader(focus)
        st.markdown('<div class="insight-label">AI coach</div>', unsafe_allow_html=True)
        if st.session_state.coach_text:
            st.markdown(st.session_state.coach_text)
        else:
            st.info(GUIDES[focus])
            st.caption("AI coaching was unavailable. Verified concept guide shown instead.")
        if st.session_state.coach_error:
            with st.expander("AI connection detail"):
                st.code(st.session_state.coach_error)

        st.markdown('<div class="section-label">Your answers</div>', unsafe_allow_html=True)
        for row in result["rows"]:
            question = row["question"]
            status = "good" if row["correct"] else "bad"
            label = "Correct" if row["correct"] else "Review"
            st.markdown(f'<div class="answer-row {status}"><strong>{label} · {question.concept}</strong></div>', unsafe_allow_html=True)
            st.write(question.prompt)
            if not row["correct"]:
                st.caption(f"Your answer: {question.options[row['selected']]}")
                st.caption(f"Correct answer: {question.options[question.answer]}")
                st.caption(f"Likely mix-up: {row['reason']}")

        st.markdown('<div class="section-label">One question to lock it in</div>', unsafe_allow_html=True)
        practice = get_practice_question(focus)
        st.markdown(f'<div class="question-prompt">{practice.prompt}</div>', unsafe_allow_html=True)
        if "practice_answer" not in st.session_state:
            with st.form("practice_form"):
                choice = st.radio(
                    "Choose an answer",
                    options=list(range(4)),
                    format_func=lambda option: practice.options[option],
                    index=None,
                    key="practice_choice",
                    label_visibility="collapsed",
                )
                checked = st.form_submit_button("Check understanding  ↗", type="primary")
            if checked:
                if choice is None:
                    st.warning("Choose an answer first.")
                else:
                    st.session_state.practice_answer = choice
                    st.rerun()
        else:
            choice = st.session_state.practice_answer
            if choice == practice.answer:
                st.success("You got it. This concept is now clearer.")
            else:
                st.warning("Not quite yet. Read the model below, then retry the track.")
                st.caption(f"Correct answer: {practice.options[practice.answer]}")
            st.info(GUIDES[focus])
    else:
        st.success(f"All {result['total']} answers were correct. Pick another track for a fresh challenge.")

    st.write("")
    if st.button("Try another track  ↗", type="secondary"):
        reset()
        st.rerun()
