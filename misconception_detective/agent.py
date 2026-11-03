"""Multi-agent teaching workflow for misconception detection."""

from __future__ import annotations

import os
from collections import Counter
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

try:
    from .question_bank import GUIDES, PRACTICE, Question
except ImportError:  # pragma: no cover - fallback for direct script execution
    from question_bank import GUIDES, PRACTICE, Question


load_dotenv(Path(__file__).resolve().parent.parent / ".env")


@tool
def concept_guide(concept: str) -> str:
    """Get the verified teaching note for a named quiz concept."""
    return GUIDES.get(concept, "No guide is available for this concept.")


def _build_model() -> ChatGoogleGenerativeAI | None:
    if not os.getenv("GOOGLE_API_KEY"):
        return None

    return ChatGoogleGenerativeAI(
        model=os.getenv("MISCONCEPTION_MODEL", "gemini-3.6-flash"),
        max_retries=2,
        timeout=45,
    )


def _make_agent(name: str, system_prompt: str):
    model = _build_model()
    if model is None:
        return None

    return create_agent(
        model=model,
        tools=[concept_guide],
        system_prompt=system_prompt,
        name=name,
    )


AGENT_TEAM = {
    "grader": {
        "role": "Deterministic scoring agent",
        "agent": None,
    },
    "concept_coach": {
        "role": "Explains the focus misconception using the concept guide",
        "agent": _make_agent(
            "concept_coach",
            (
                "You are a precise, kind learning coach. Diagnose the learner's reasoning, "
                "not their ability. You MUST call concept_guide for the focus concept before "
                "answering. Use its note as ground truth. Do not invent learner history or "
                "claim certainty about their thoughts. Write in simple English, under 110 words. "
                "Use exactly three short sections: Likely mix-up, Correct mental model, Next step. "
                "The quiz score and correct answers supplied by the app are authoritative."
            ),
        ),
    },
    "practice_planner": {
        "role": "Builds a short, targeted practice question for the learner",
        "agent": _make_agent(
            "practice_planner",
            (
                "You are a supportive tutor. Use the concept_guide tool for the focus concept and "
                "turn it into one concise practice task that checks whether the learner can apply the "
                "concept correctly. Output only a single question prompt with four labeled choices and "
                "the correct answer index. Keep it brief and focused."
            ),
        ),
    },
}

AGENT_COUNT = len(AGENT_TEAM)


def grade(questions: list[Question], answers: dict[str, int]) -> dict:
    """Score answers and identify misconceptions without relying on an LLM."""
    rows = []
    for question in questions:
        selected = answers.get(question.id)
        if selected is None:
            raise ValueError(f"Missing answer for {question.id}")
        correct = selected == question.answer
        rows.append(
            {
                "question": question,
                "selected": selected,
                "correct": correct,
                "reason": None if correct else question.wrong_reasons[selected],
            }
        )

    misses = Counter(row["question"].concept for row in rows if not row["correct"])
    focus = misses.most_common(1)[0][0] if misses else None
    return {
        "rows": rows,
        "score": sum(row["correct"] for row in rows),
        "total": len(rows),
        "misses": dict(misses),
        "focus": focus,
    }


def get_practice_question(focus: str | None) -> Question | None:
    """Prefer the deterministic practice bank, while the multi-agent team can be extended later."""
    return PRACTICE.get(focus) if focus else None


def explain_diagnosis(result: dict, track: str) -> str:
    """Use the concept-coach agent and the verified concept guide for tailored feedback."""
    if not result["focus"]:
        return "Strong work. Every answer was correct. Try another track to test a new skill."

    agent = AGENT_TEAM["concept_coach"]["agent"]
    if agent is None:
        guide = concept_guide.invoke({"concept": result["focus"]})
        return (
            "Likely mix-up: the learner likely merged the concept with a nearby idea.\n"
            f"Correct mental model: {guide}\n"
            "Next step: review the concept with one short practice question before retrying."
        )

    wrong = [
        {
            "question": row["question"].prompt,
            "chosen": row["question"].options[row["selected"]],
            "correct": row["question"].options[row["question"].answer],
            "misconception": row["reason"],
        }
        for row in result["rows"]
        if not row["correct"]
    ]

    response = agent.invoke(
        {
            "messages": [
                (
                    "user",
                    f"Track: {track}\nScore: {result['score']}/{result['total']}\n"
                    f"Focus concept: {result['focus']}\nWrong answers: {wrong}\n"
                    "Explain the main misconception and prepare the learner for one short practice question.",
                )
            ]
        }
    )
    content = response["messages"][-1].content
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(part.get("text", "") for part in content if isinstance(part, dict)).strip()
    return str(content)


def run_agent_team(questions: list[Question], answers: dict[str, int], track: str) -> dict[str, Any]:
    """Return a structured result for the full multi-agent workflow."""
    result = grade(questions, answers)
    return {
        "diagnosis": explain_diagnosis(result, track),
        "practice": get_practice_question(result["focus"]),
        "agents": list(AGENT_TEAM.keys()),
        "result": result,
    }

