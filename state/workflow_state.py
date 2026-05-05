from typing import TypedDict, List, Optional


class WorkflowState(TypedDict):
    task:               str        # User ka original task
    plan:               List[str]  # Planner ke banaye steps
    current_step:       int        # Abhi kaunsa step chal raha hai
    results:            List[str]  # Har step ka result
    validation_passed:  bool       # Validator ne approve kiya?
    final_report:       Optional[str]  # Reporter ka final output
    error:              Optional[str]  # Koi error aayi toh yahan