# 🎤 AI Interview Simulator

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-000000?style=flat&logo=chainlink&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-grey?style=flat)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat)

> A locally-running AI-powered interview simulator — practice technical interviews, get scored in real time, and receive detailed feedback to improve your answers.

---

## 🎯 Why I Built This

Technical interviews are stressful — especially without practice. Most interview prep tools are expensive or require internet access. This simulator runs **100% locally** using Ollama, gives **real-time scoring and feedback** on every answer, and generates a **final performance report** — completely free.

---

## ✨ Features

- 🎭 **Multiple Roles** — Data Scientist, ML Engineer, AI Engineer, Data Analyst
- 📊 **Difficulty Levels** — Easy, Medium, Hard
- 💬 **Real-time Scoring** — Each answer scored 1-10 with detailed feedback
- 📋 **Final Report** — Overall score, strengths, weak areas, improvement tips
- 🖥️ **100% Local** — Runs on your machine via Ollama (no API costs)
- 🔄 **Session History** — Full Q&A transcript with scores

---

## 📸 Demo

```
🎤 AI Interview Simulator
━━━━━━━━━━━━━━━━━━━━━━━━

Role: ML Engineer | Difficulty: Medium | Question 3/7

Q: "Explain the difference between bagging and boosting.
    Give an example of each."

Your Answer: [user types here]

━━━━━━━━━━━━━━━━━━━━━━━━
Score: 8/10 ⭐⭐⭐⭐

✅ Strengths:
   - Correctly identified Random Forest as bagging example
   - Good explanation of parallel vs sequential training

💡 Improve:
   - Mention that boosting focuses on misclassified samples
   - Add XGBoost/AdaBoost as boosting examples
━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🏗️ Architecture

```
User selects Role + Difficulty
        ↓
Question Generator (LangChain + Ollama)
        ↓
User types answer
        ↓
Answer Evaluator (LangChain + Ollama)
        ↓
Score (1-10) + Feedback
        ↓
Next question... (repeat 5-10 times)
        ↓
Final Report Generator
        ↓
Overall score + Strengths + Weak areas + Tips
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com) installed

### Installation

```bash
# Clone the repo
git clone https://github.com/adheethii/ai-interview-simulator.git
cd ai-interview-simulator

# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Pull Ollama model
ollama pull llama3.2:1b

# Run the app
streamlit run app.py
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | Ollama (llama3.2:1b) — runs locally |
| Framework | LangChain |
| Frontend | Streamlit |
| Language | Python 3.10+ |

---

## 📁 Project Structure

```
ai-interview-simulator/
├── app.py                  ← Main Streamlit app
├── interviewer.py          ← Question generation + answer evaluation
├── prompts.py              ← All prompt templates
├── question_bank.py        ← Role-specific question topics
├── requirements.txt
└── README.md
```

---

## 🙏 Acknowledgements

- [LangChain](https://langchain.com)
- [Ollama](https://ollama.com)
- [Streamlit](https://streamlit.io)
