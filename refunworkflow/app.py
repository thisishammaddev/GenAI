import os
from dotenv import load_dotenv
from typing import TypedDict
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END

load_dotenv()

if os.getenv("GROQ_API_KEY"):
    llm = ChatGroq(model="openai/gpt-oss-120b")
elif os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"):
    llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash")
else:
    raise ValueError("No API key found. Please set GROQ_API_KEY or GEMINI_API_KEY in .env")

class QAState(TypedDict):
    question: str
    answer: str


def llm_qa(state: QAState) -> dict:
    question = state["question"]
    prompt = (
        "Answer the following question directly and concisely. "
        "Keep the answer short (1-2 sentences only, not too long):\n\n"
        f"Question: {question}"
    )
    response = llm.invoke(prompt)
    answer = getattr(response, "text", None) or response.content
    if isinstance(answer, list):
        answer = "".join(
            b.get("text", "") if isinstance(b, dict) else getattr(b, "text", str(b))
            for b in answer
        )
    return {"answer": str(answer).strip()}

graph = StateGraph(QAState)  # type: ignore[type-var]
graph.add_node("llm_qa", llm_qa)
graph.add_edge(START, "llm_qa")
graph.add_edge("llm_qa", END)
workflow = graph.compile()

initial_state: QAState = {
    "question": input("Enter your question: "),
    "answer": ""
}
final_state = workflow.invoke(initial_state)
print("\n--- Result ---")
print(final_state)
print(f"\n--- Answer ---\n{final_state.get('answer', '')}\n")

with open("qa_graph.png", "wb") as f:
    f.write(workflow.get_graph().draw_mermaid_png())