import os
import streamlit as st
from dotenv import load_dotenv
from graph.workflow_graph import build_workflow

load_dotenv()

# ── Page Config ─────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Workflow Engine",
    page_icon="🤖",
    layout="centered"
)

# ── Custom CSS ───────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');
    
    * { font-family: 'Space Grotesk', sans-serif; }
    
    .main { background-color: #0f0f0f; }
    
    .stApp {
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 100%);
        color: #ffffff;
    }

    .title-box {
        background: linear-gradient(135deg, #1e1e3f, #16213e);
        border: 1px solid #4f46e5;
        border-radius: 16px;
        padding: 30px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 0 40px rgba(79,70,229,0.2);
    }

    .title-box h1 {
        font-size: 2rem;
        font-weight: 700;
        color: #a5b4fc;
        margin: 0;
    }

    .title-box p {
        color: #6b7280;
        margin-top: 8px;
        font-size: 0.95rem;
    }

    .agent-card {
        background: #1e1e2e;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 10px 0;
        border-left: 4px solid;
        animation: fadeIn 0.4s ease;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    .agent-planner   { border-color: #6366f1; }
    .agent-executor  { border-color: #f59e0b; }
    .agent-validator { border-color: #10b981; }
    .agent-reporter  { border-color: #3b82f6; }

    .agent-title {
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 6px;
    }

    .agent-content {
        color: #9ca3af;
        font-size: 0.88rem;
        line-height: 1.6;
    }

    .report-box {
        background: linear-gradient(135deg, #1e3a5f, #1e1e3f);
        border: 1px solid #3b82f6;
        border-radius: 16px;
        padding: 28px;
        margin-top: 20px;
        box-shadow: 0 0 30px rgba(59,130,246,0.15);
    }

    .report-box h3 {
        color: #60a5fa;
        font-size: 1.2rem;
        margin-bottom: 16px;
    }

    .report-box p {
        color: #d1d5db;
        line-height: 1.8;
        font-size: 0.95rem;
    }

    .stat-row {
        display: flex;
        gap: 16px;
        margin-top: 20px;
    }

    .stat-card {
        flex: 1;
        background: #1e1e2e;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        border: 1px solid #374151;
    }

    .stat-number {
        font-size: 1.8rem;
        font-weight: 700;
        color: #a5b4fc;
    }

    .stat-label {
        font-size: 0.8rem;
        color: #6b7280;
        margin-top: 4px;
    }

    .stTextArea textarea {
        background: #1e1e2e !important;
        color: #ffffff !important;
        border: 1px solid #374151 !important;
        border-radius: 12px !important;
        font-size: 0.95rem !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 32px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        cursor: pointer !important;
        transition: all 0.2s !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(79,70,229,0.4) !important;
    }

    div[data-testid="stStatusWidget"] { display: none; }
</style>
""", unsafe_allow_html=True)


# ── Header ───────────────────────────────────────────────
st.markdown("""
<div class="title-box">
    <h1>🤖 Multi-Agent Workflow Engine</h1>
    <p>Planner → Executor → Validator → Reporter &nbsp;|&nbsp; Powered by GPT-4o-mini</p>
</div>
""", unsafe_allow_html=True)


# ── API Key Check ────────────────────────────────────────
if not os.getenv("OPENAI_API_KEY"):
    st.error("❌ OPENAI_API_KEY not found! Please add it to your .env file.")
    st.stop()


# ── Task Input ───────────────────────────────────────────
st.markdown("### 📌 Enter Your Task")
task = st.text_area(
    label="",
    placeholder="Example: Research top 3 AI tools for data analysis in 2025...",
    height=100
)

run_btn = st.button("🚀 Run Workflow")


# ── Run Workflow ─────────────────────────────────────────
if run_btn:
    if not task.strip():
        st.warning("⚠️ Please enter a task first!")
        st.stop()

    # Placeholders for live updates
    status_placeholder  = st.empty()
    agents_placeholder  = st.empty()
    report_placeholder  = st.empty()

    agent_logs = []

    def add_log(agent, icon, color_class, content):
        agent_logs.append({
            "agent":       agent,
            "icon":        icon,
            "color_class": color_class,
            "content":     content
        })
        # Render all logs so far
        html = ""
        for log in agent_logs:
            html += f"""
            <div class="agent-card {log['color_class']}">
                <div class="agent-title">{log['icon']} {log['agent']}</div>
                <div class="agent-content">{log['content']}</div>
            </div>
            """
        agents_placeholder.markdown(html, unsafe_allow_html=True)

    # ── Build workflow with callbacks ─────────────────────
    try:
        status_placeholder.info("⏳ Building workflow...")
        workflow = build_workflow()

        initial_state = {
            "task":              task.strip(),
            "plan":              [],
            "current_step":      0,
            "results":           [],
            "validation_passed": False,
            "final_report":      None,
            "error":             None
        }

        status_placeholder.info("🧠 Planner is breaking down your task...")

        # ── Stream node by node ───────────────────────────
        final_state = None

        for step in workflow.stream(initial_state):
            node_name = list(step.keys())[0]
            node_state = step[node_name]

            if node_name == "planner":
                plan = node_state.get("plan", [])
                plan_html = "<br>".join([f"&nbsp;&nbsp;→ {s}" for s in plan])
                add_log(
                    "PLANNER", "🧠", "agent-planner",
                    f"Created <b>{len(plan)} steps:</b><br>{plan_html}"
                )
                status_placeholder.info("⚙️ Executor is working on each step...")

            elif node_name == "executor":
                results  = node_state.get("results", [])
                step_num = len(results)
                last     = results[-1] if results else ""
                short    = last[:120] + "..." if len(last) > 120 else last
                add_log(
                    f"EXECUTOR — Step {step_num}", "⚙️", "agent-executor",
                    short
                )

            elif node_name == "validator":
                passed = node_state.get("validation_passed", False)
                add_log(
                    "VALIDATOR", "🔍", "agent-validator",
                    "✅ All results validated — <b>PASSED</b>" if passed
                    else "❌ Validation <b>FAILED</b>"
                )
                status_placeholder.info("📝 Reporter is writing the final report...")

            elif node_name == "reporter":
                add_log(
                    "REPORTER", "📝", "agent-reporter",
                    "✅ Final report has been generated successfully!"
                )
                final_state = node_state

        # ── Final Report ──────────────────────────────────
        status_placeholder.success("🎉 Workflow Complete!")

        if final_state:
            report      = final_state.get("final_report", "")
            steps_done  = len(final_state.get("plan", []))
            validated   = final_state.get("validation_passed", False)

            report_placeholder.markdown(f"""
<div class="report-box">
    <h3>📊 Final Report</h3>
    <p>{report.replace(chr(10), '<br>')}</p>
</div>

<div class="stat-row">
    <div class="stat-card">
        <div class="stat-number">{steps_done}</div>
        <div class="stat-label">Steps Executed</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">4</div>
        <div class="stat-label">Agents Used</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">{'✅' if validated else '❌'}</div>
        <div class="stat-label">Validation</div>
    </div>
</div>
""", unsafe_allow_html=True)

    except Exception as e:
        status_placeholder.error(f"❌ Error: {str(e)}")
        st.exception(e)