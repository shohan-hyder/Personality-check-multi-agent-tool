# 🧠 AI Multi-Agent System: Personality & Skill Coach

A modular, FastAPI-powered AI system that assesses personality and recommends personalized skill development plans using **LangGraph**, **LLMs**, and **adaptive logic**.

🎯 **Use Cases**:
- Personality assessment with dynamic, culturally-aware questions
- Personalized learning path generation
- General knowledge Q&A with real-time web search
- Coaching, HR, EdTech, and self-development tools

> 🚀 Deployable as a web API or CLI tool — built for developers, coaches, and AI enthusiasts.

---

## 🔥 Features

| Feature | Description |
|--------|-------------|
| 🧑‍💼 **Smart Personality Checker** | Asks 8 adaptive questions based on user's country, skills, and goals |
| 🛠️ **Skill Planner** | Generates a step-by-step learning plan with real resources from the web |
| ❓ **General Q&A** | Answers any question using live web search (Tavily) |
| 📊 **Scored Feedback** | Returns personality score out of 100 + 5-line summary + 2 improvement tips |
| 💾 **JSON Export** | Saves full results to a timestamped JSON file |
| 🌐 **FastAPI Backend** | REST API with Swagger UI at `/api/docs` |
| 🧩 **Modular Design** | Clean separation: agents, tools, graph, services, schema |

---

## 🛠️ Tech Stack

| Layer | Technology |
|------|------------|
| Framework | `FastAPI`, `LangGraph`, `LangChain` |
| LLM | `Groq` (Llama3-70b) |
| Search | `TavilySearch` (real-time web search) |
| State | `TypedDict` + LangGraph |
| Env | `Miniconda3` / `pip` |
| Frontend | Swagger UI (`/api/docs`) |

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/your-username/multi-agents-demo.git
cd multi-agents-demo