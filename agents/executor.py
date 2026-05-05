from dotenv import load_dotenv
load_dotenv()  # ← YEH ADD KARO TOP PE

from langchain_openai import ChatOpenAI
from state.workflow_state import WorkflowState

llm = ChatOpenAI(model="gpt-4o-mini")


def executor_agent(state: WorkflowState) -> WorkflowState:
    """
    Plan ka current step execute karta hai.
    """
    idx  = state["current_step"]
    step = state["plan"][idx]

    print(f"\n⚙️  [EXECUTOR] Running Step {idx + 1}/{len(state['plan'])}")
    print(f"   → {step}")

    response = llm.invoke(f"""
You are an Executor agent. Perform this step and return a detailed, clear result.

Step to execute: {step}
Previous results for context: {state['results']}
""")

    result  = response.content.strip()
    updated = state["results"] + [f"Step {idx + 1}: {result}"]

    print(f"   ✅ Step {idx + 1} completed")

    return {
        **state,
        "results":      updated,
        "current_step": idx + 1
    }