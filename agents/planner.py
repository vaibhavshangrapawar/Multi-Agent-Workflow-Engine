from dotenv import load_dotenv
load_dotenv()  # ← YEH ADD KARO TOP PE

from langchain_openai import ChatOpenAI
from state.workflow_state import WorkflowState

llm = ChatOpenAI(model="gpt-4o-mini")


def planner_agent(state: WorkflowState) -> WorkflowState:
    """
    User ka task leke usse 3 clear steps mein todta hai.
    """
    print("\n🧠 [PLANNER] Breaking task into steps...")

    response = llm.invoke(f"""
You are a Planner agent. Break this task into exactly 3 clear numbered steps.
Return ONLY a numbered list. Nothing else. No explanation.

Task: {state['task']}
""")

    lines = response.content.strip().split("\n")
    steps = [
        l.strip()
        for l in lines
        if l.strip() and l.strip()[0].isdigit()
    ]

    print(f"   ✅ {len(steps)} steps created:")
    for s in steps:
        print(f"      → {s}")

    return {
        **state,
        "plan":         steps,
        "current_step": 0,
        "results":      []
    }