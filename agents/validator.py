from dotenv import load_dotenv
load_dotenv()  # ← YEH ADD KARO TOP PE

from langchain_openai import ChatOpenAI
from state.workflow_state import WorkflowState

llm = ChatOpenAI(model="gpt-4o-mini")


def validator_agent(state: WorkflowState) -> WorkflowState:
    """
    Saare results check karta hai — task complete hua ya nahi.
    """
    print("\n🔍 [VALIDATOR] Validating all results...")

    response = llm.invoke(f"""
You are a Validator agent. Check if the results successfully complete the original task.
Reply with ONLY one word: PASS or FAIL.

Original Task: {state['task']}
Results achieved: {state['results']}
""")

    content = response.content.strip().upper()
    passed  = content.startswith("PASS")

    print(f"   {'✅ PASSED' if passed else '❌ FAILED'}")

    return {
        **state,
        "validation_passed": passed,
        "error": None if passed else "Validation failed — results incomplete"
    }