# 🧠 Collaborative Multi-Agent AI Think-Tank & Deep Research Pipeline

An enterprise-grade, autonomous multi-agent research pipeline that orchestrates a 3-way collaborative discussion to explore ideas laterally, followed by an autonomous deep web-research execution phase.

## 🚀 The Architecture

1. **First Voice AI (e.g., Gemini 3.1 Pro):** Establishes foundational arguments, thinks outside the box, and asks thought-provoking questions.
2. **Second Voice AI (e.g., DeepSeek V4 / Llama 3.3 via OpenRouter):** Responds directly to the first voice, expands the conversation in new directions, and adds lateral insights.
3. **Anchor AI (e.g., Qwen 3.7 Max / Moonshot Kimi via OpenRouter):** Acts as the group's synthesis engine. It reviews the discussion, anchors the AI back to the user's original seed prompt and attached files, and guides the next round to ensure alignment with the human's core intent.
4. **The Researcher (Gemini Deep Research):** Takes the profound open questions and strategic directions from the think-tank and autonomously browses the web to generate a comprehensive 20-page `.docx` executive brief.

## ⚙️ Customization & Configuration Files

This pipeline is designed to be highly modular. When you run the script for the first time, it will automatically generate two configuration files:

* **`models.json`:** Dynamically select and swap your preferred models for each role from a curated list of frontier models (including DeepSeek, Qwen, Meta Llama, NVIDIA Nemotron, and Moonshot Kimi).
* **`personas.json`:** Easily adjust the psychology, role-play, and system instructions for the First Voice, Second Voice, and Anchor AIs without ever touching the Python code.

## 🛠️ Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your environment:**
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY="your_native_google_key"
   OPENROUTER_API_KEY="your_openrouter_key"
   ```

## 🎯 How to Run

1. **Phase 1 (The Collaborative Think-Tank):** Write your starting thesis in `seed_prompt.md`, drop any background reading or context files into the `prompt_files/` directory, and execute:
   ```bash
   python 01.0_debate.py
   ```
   *Select your model configuration using the interactive terminal menu.*

2. **Phase 2 (The Deep Research):** Review the generated discussion log and executive summary, then trigger the autonomous web agent to explore the findings:
   ```bash
   python 02.0_deep_research.py
   ```
