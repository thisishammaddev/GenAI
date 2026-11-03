import sys
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END


# Define State
class EmailState(TypedDict):
    topic: str
    email: str
    evaluation: str
    feedback: str
    iteration: int
    max_iteration: int
    email_history: list[str]
    feedback_history: list[str]


# Node 1: Generate Email
def generate(state: EmailState) -> dict:
    topic = state["topic"]

    email = (
        f"Subject: Regarding {topic}\n\n"
        f"Dear Sir/Madam,\n\n"
        f"I am writing to discuss {topic}. "
        f"Please let me know if further information is needed.\n\n"
        f"Best regards"
    )

    return {
        "email": email,
        "email_history": state["email_history"] + [email]
    }


# Node 2: Evaluate Email
def evaluate(state: EmailState) -> dict:
    email = state["email"]

    # Simple evaluation for demonstration
    if len(email) > 100 and "Dear" in email:
        evaluation = "approved"
        feedback = "The email is clear and professional."
    else:
        evaluation = "needs_improvement"
        feedback = (
            "Make the email longer and use a professional greeting."
        )

    return {
        "evaluation": evaluation,
        "feedback": feedback,
        "feedback_history": (
            state["feedback_history"] + [feedback]
        )
    }


# Node 3: Optimize Email
def optimize(state: EmailState) -> dict:
    email = state["email"]
    feedback = state["feedback"]

    improved_email = (
        email
        + "\n\nAdditional note: "
        + feedback
        + " Please feel free to contact me."
    )

    return {
        "email": improved_email,
        "iteration": state["iteration"] + 1,
        "email_history": (
            state["email_history"] + [improved_email]
        )
    }


# Decide whether to approve or improve
def check_email(
    state: EmailState
) -> Literal["approved", "needs_improvement", "max_reached"]:

    if state["evaluation"] == "approved":
        return "approved"

    if state["iteration"] >= state["max_iteration"]:
        return "max_reached"

    return "needs_improvement"


# Build Graph
graph = StateGraph(EmailState)

graph.add_node("generate", generate)
graph.add_node("evaluate", evaluate)
graph.add_node("optimize", optimize)

graph.add_edge(START, "generate")
graph.add_edge("generate", "evaluate")

graph.add_conditional_edges(
    "evaluate",
    check_email,
    {
        "approved": END,
        "needs_improvement": "optimize",
        "max_reached": END
    }
)

graph.add_edge("optimize", "evaluate")


# Compile
workflow = graph.compile()


def main() -> None:
    default_topic = "college events"
    topic = ""

    if len(sys.argv) > 1:
        topic = sys.argv[1].strip()
    elif sys.stdin.isatty():
        try:
            topic = input("Enter email topic: ").strip()
        except EOFError:
            topic = default_topic
    else:
        topic = default_topic

    if not topic:
        topic = default_topic

    initial_state = {
        "topic": topic,
        "email": "",
        "evaluation": "",
        "feedback": "",
        "iteration": 0,
        "max_iteration": 3,
        "email_history": [],
        "feedback_history": []
    }

    final_state = workflow.invoke(initial_state)

    # Display Results
    print("\n--- FINAL EMAIL ---")
    print(final_state["email"])

    print("\n--- EVALUATION ---")
    print(final_state["evaluation"])

    print("\n--- FEEDBACK ---")
    print(final_state["feedback"])

    print("\n--- ITERATIONS ---")
    print(final_state["iteration"])

    print("\n--- EMAIL HISTORY ---")
    for i, email in enumerate(final_state["email_history"], start=1):
        print(f"\nVersion {i}:\n{email}")

    print("\n--- FEEDBACK HISTORY ---")
    for i, feedback in enumerate(
        final_state["feedback_history"], start=1
    ):
        print(f"{i}. {feedback}")

    # Save Graph Image
    try:
        png_data = workflow.get_graph().draw_mermaid_png()

        with open("email_workflow.png", "wb") as file:
            file.write(png_data)

        print("\nGraph saved as email_workflow.png")

    except Exception as error:
        print("\nCould not save graph image:", error)


if __name__ == "__main__":
    main()