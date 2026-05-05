from langgraph.graph import StateGraph, END
from state.workflow_state import WorkflowState
from agents.planner   import planner_agent
from agents.executor  import executor_agent
from agents.validator import validator_agent
from agents.reporter  import reporter_agent


def should_continue(state: WorkflowState) -> str:
    """
    Decide karo — aur steps baaki hain ya validate karo.
    """
    if state["current_step"] < len(state["plan"]):
        return "execute"   # Abhi aur steps hain
    return "validate"      # Saare steps ho gaye


def build_workflow():
    g = StateGraph(WorkflowState)

    # ── Nodes (agents) add karo ──────────────────────────
    g.add_node("planner",   planner_agent)
    g.add_node("executor",  executor_agent)
    g.add_node("validator", validator_agent)
    g.add_node("reporter",  reporter_agent)

    # ── Entry point ──────────────────────────────────────
    g.set_entry_point("planner")

    # ── Edges (flow) ─────────────────────────────────────
    g.add_edge("planner", "executor")

    # Executor ke baad — loop ya validate
    g.add_conditional_edges(
        "executor",
        should_continue,
        {
            "execute":  "executor",   # Loop back
            "validate": "validator"   # Aage jao
        }
    )

    g.add_edge("validator", "reporter")
    g.add_edge("reporter",  END)

    return g.compile()
    workflow = build_workflow()