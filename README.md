📚 Competitive Exam Study Planner Agent
An AI-powered multi-agent system that creates personalized week-by-week study plans for competitive exams like GATE, CAT, and UPSC.
🔗 Live Demo
[Click here to open the app](https://exam-planner-agent-production.up.railway.app)

📌 Project Info

Course: Introduction to Agentic AI Systems
University: Ramdeobaba University, Nagpur
Project Number: 14
Team:Mahek Mishra(09) & Jidnyasa Mude(12)

📄 Documents
-Problem Statement
-Task Decomposition & Specs
-Architecture Diagram


🧠 What This Project Does
Students preparing for competitive exams like GATE, CAT, or UPSC struggle with three problems:

1.They don't know which topics to prioritize
2.They don't know where to find good resources
3.They can't make a realistic plan on their own

This AI agent system solves all three problems automatically. The student just enters their exam name, weak topics, weeks available, and hours per day — and 4 independent AI agents work together to produce a complete personalized study plan.

🤖 The 4 Agents
Agent 1 — Syllabus Researcher

Has its own independent ReAct loop
Uses Tavily Search tool to find the complete syllabus
Searches multiple times with different queries
Produces a clean structured syllabus

Agent 2 — Topic Prioritizer

Has its own independent ReAct loop
Uses Tavily Search to find high weightage topics
Searches for previous year question patterns
Ranks all topics as HIGH / MEDIUM / LOW priority
Specially marks student's weak topics

Agent 3 — Study Plan Builder

Has its own independent ReAct loop
Uses Tavily Search to find real study resources
Builds a week-by-week plan with daily targets
Includes actual resource links found from internet
Revises the plan if Judge gives low score

Agent 4 — Judge (LLM-as-Judge)

Has its own independent ReAct loop
Critically evaluates the study plan
Scores it out of 10 using a fixed rubric
Gives specific feedback on what to improve
If score is below 6 — sends plan back to Agent 3 for revision


🔄 How The Agents Work Together
User Input
↓
Agent 1: Researches syllabus using Tavily
↓
Agent 2: Prioritizes topics using Tavily
↓
Agent 3: Builds week-by-week plan using Tavily
↓
Agent 4: Judges and scores the plan
↓
Score below 6? → Back to Agent 3 (max 2 revisions)
Score 6 or above? → Show final output
Each agent has its own:

Independent LLM instance
Own system prompt and personality
Own tools
Own ReAct reasoning loop (Think → Act → Observe → Repeat)


📊 LLM-as-Judge Evaluation Rubric (Agent 4)

Criteria                                  Max Score
All weak topics covered?                     3
Plan realistic for weeks available?          3
Good resources included?                     2
Revision week at the end?                    2
Total                                       10

🛠️ Tech Stack
Tool                               Purpose
Python                             Main language
LangGraph                          Multi-agent framework
Groq llama-3.3-70b-versatile       LLM for all 4 agents
Tavily Search                      Internet search toolS
treamlit                           Web UI
Railway                            Deployment

📁 Project Structure
exam-planner-agent/
├── app.py
├── requirements.txt
├── railway.json
├── README.md
├── agent/
│   ├── init.py
│   ├── state.py
│   ├── tools.py
│   ├── agent1_syllabus_researcher.py
│   ├── agent2_topic_prioritizer.py
│   ├── agent3_plan_builder.py
│   ├── agent4_judge.py
│   └── graph.py
├── Problem_Statement.pdf
├── Task_Decomposition.pdf
└── Architecture_Diagram.pdf

⚙️ Run Locally
Step 1 — Clone the repo:
git clone https://github.com/JidnyasaMude/exam-planner-agent.git
cd exam-planner-agent
Step 2 — Create virtual environment:
python -m venv venv
venv\Scripts\activate
Step 3 — Install dependencies:
pip install -r requirements.txt
Step 4 — Create .env file:
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here
Step 5 — Run the app:
streamlit run app.py
Open browser at http://localhost:8501

🚀 Deployment
This app is deployed on Railway.
Every push to main branch automatically redeploys.
Live URL: https://exam-planner-agent-production.up.railway.app