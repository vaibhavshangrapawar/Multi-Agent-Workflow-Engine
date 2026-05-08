# Multi-Agent Workflow Engine 
# 🤖 Autonomous Multi-Agent Workflow Engine

An AI-powered workflow automation system using LangGraph and GPT-4o-mini.
Four specialized agents collaborate to complete complex tasks autonomously.

## 🏗️ Architecture

User Task → [PLANNER] → [EXECUTOR] → [VALIDATOR] → [REPORTER] → Output

## 🤖 Agents

| Agent | Role |
|---|---|
| 🧠 Planner | Breaks task into steps |
| ⚙️ Executor | Executes each step |
| 🔍 Validator | Validates results |
| 📝 Reporter | Generates final report |

## 🛠️ Tech Stack

- **LangGraph** — Multi-agent orchestration
- **GPT-4o-mini** — AI backbone
- **Streamlit** — Interactive UI
- **Python** — Core language

## 🚀 Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/multi-agent-workflow.git
cd multi-agent-workflow
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your API key
Create a `.env` file:
```env
OPENAI_API_KEY=your_key_here
```

### 4. Run the app
```bash
streamlit run app.py

##📁 Project Structure

multi_agent/
├── agents/          # All 4 AI agents
├── graph/           # LangGraph workflow
├── state/           # Shared state
├── app.py           # Streamlit UI
└── main.py          # CLI version
```


