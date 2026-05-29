# 🧠 Adversarial Multi-Agent AI Debate & Deep Research Pipeline

An enterprise-grade, autonomous multi-agent research pipeline that orchestrates a 3-way structured debate to uncover cognitive blind spots, followed by an autonomous deep web-research execution phase.

## 🚀 The Architecture

1. **The Senior AI (Gemini 3.1 Pro):** Establishes authoritative, structural arguments and deep domain insights.
2. **The Junior AI (DeepSeek V4 Pro via OpenRouter):** Uses advanced reasoning to relentlessly interrogate assumptions and propose sharp, leading questions.
3. **The BS Detector (Qwen 3.7 Max via OpenRouter):** Acts as a ruthless grounding agent, slicing through hypothetical hype and enforcing empirical reality.
4. **The Researcher (Gemini Deep Research):** Takes the unresolved, high-tension conflicts from the debate and autonomously browses the web to generate a comprehensive 20-page `.docx` executive brief.

## 🛠️ Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name```

2. **Install dependencies:**
```bash
pip install -r requirements.txt```


3. **Configure your environment:**
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY="your_native_google_key"
OPENROUTER_API_KEY="your_openrouter_key"

```



## 🎯 How to Run

1. **Phase 1 (The Debate):** Write your starting thesis in `seed_prompt.md`, drop any background reading into `prompt_files/`, and execute:
```bash
python debate.py

```


*Select your model configuration using the interactive terminal menu.*
2. **Phase 2 (The Deep Research):** Review the debate log, then trigger the autonomous web agent to settle the score:
```bash
python step2_deep_research.py
