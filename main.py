# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from graph.workflow_graph import build_workflow

# app = FastAPI(title="Multi-Agent Workflow Engine")


# class TaskRequest(BaseModel):
#     task: str


# class WorkflowResponse(BaseModel):
#     task: str
#     plan: list
#     results: list
#     validation_passed: bool
#     final_report: str


# @app.post("/run-workflow", response_model=WorkflowResponse)
# async def run_workflow(request: TaskRequest):
#     """
#     User ka task lo aur multi-agent workflow se execute karo.
#     """
#     if not request.task.strip():
#         raise HTTPException(status_code=400, detail="Task cannot be empty")

#     # Initial state
#     initial_state = {
#         "task": request.task,
#         "plan": [],
#         "current_step": 0,
#         "results": [],
#         "validation_passed": False,
#         "final_report": None,
#         "error": None
#     }

#     try:
#         # Workflow run karo
#         final_state = build_workflow.invoke(initial_state)

#         return WorkflowResponse(
#             task=final_state["task"],
#             plan=final_state["plan"],
#             results=final_state["results"],
#             validation_passed=final_state["validation_passed"],
#             final_report=final_state["final_report"] or "No report generated"
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @app.get("/health")
# def health_check():
#     return {"status": "running", "message": "Multi-Agent Workflow Engine is active"}

import os
from dotenv import load_dotenv
from graph.workflow_graph import build_workflow  # ← YAHAN FIX KARO

load_dotenv()

def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: OPENAI_API_KEY not found in .env file!")
        return

    workflow = build_workflow()  # ← YAHAN BUILD KARO

    print("\n" + "="*55)
    print("   🤖 AUTONOMOUS MULTI-AGENT WORKFLOW ENGINE")
    print("="*55)
    task = input("\n📌 Enter your task: ").strip()

    if not task:
        print("❌ Task cannot be empty!")
        return

    initial_state = {
        "task":              task,
        "plan":              [],
        "current_step":      0,
        "results":           [],
        "validation_passed": False,
        "final_report":      None,
        "error":             None
    }

    print("\n🚀 Starting workflow...\n")
    result = workflow.invoke(initial_state)

    print("\n" + "="*55)
    print("📊 FINAL REPORT")
    print("="*55)
    print(result["final_report"])
    print("\n" + "="*55)
    print(f"✅ Validation : {'PASSED' if result['validation_passed'] else 'FAILED'}")
    print(f"📋 Steps Done : {len(result['plan'])}")
    print("="*55)
    print("\n🎉 Workflow complete!\n")

if __name__ == "__main__":
    main()