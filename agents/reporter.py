from dotenv import load_dotenv
load_dotenv()  # ← YEH ADD KARO TOP PE

from langchain_openai import ChatOpenAI
from state.workflow_state import WorkflowState

llm = ChatOpenAI(model="gpt-4o-mini")


def reporter_agent(state: WorkflowState) -> WorkflowState:
    """
    Poore workflow ka professional summary report banata hai.
    """
    print("\n📝 [REPORTER] Generating final report...")

    response = llm.invoke(f"""
You are a Reporter agent. Write a professional 2-paragraph executive summary report.

Task: {state['task']}
Plan executed: {state['plan']}
Results: {state['results']}
Validation status: {'Passed ✅' if state['validation_passed'] else 'Failed ❌'}
""")

    print("   ✅ Report generated!")

    return {
        **state,
        "final_report": response.content.strip()
    }