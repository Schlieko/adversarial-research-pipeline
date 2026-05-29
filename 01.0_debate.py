import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from openai import OpenAI
from docx import Document
from docx.shared import Pt, RGBColor

# ==========================================
# 1. SETUP & AUTHENTICATION
# ==========================================
target_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(target_dir, ".env")) 

# Gemini stays native for deep-research compatibility
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# OpenRouter handles BOTH DeepSeek and Qwen
openrouter_client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"), 
    base_url="https://openrouter.ai/api/v1"
)

# ==========================================
# 2. FILE MANAGEMENT (Models & Prompts)
# ==========================================
print("=== WELCOME TO THE 3-WAY ADVERSARIAL AI DEBATE ===")

# Dynamic models configuration
models_filepath = os.path.join(target_dir, "models.json")
if not os.path.exists(models_filepath):
    default_models = {
        "senior": ["gemini-3.1-pro-preview", "gemini-2.5-pro"],
        "junior": ["deepseek/deepseek-v4-pro", "deepseek/deepseek-chat"],
        "grounding": ["qwen/qwen3.7-max", "qwen/qwen-max"]
    }
    with open(models_filepath, "w", encoding="utf-8") as f:
        json.dump(default_models, f, indent=4)
    print("📁 Created 'models.json'.")

with open(models_filepath, "r", encoding="utf-8") as f:
    available_models = json.load(f)

# Base Prompt setup
seed_filepath = os.path.join(target_dir, "seed_prompt.md")
if not os.path.exists(seed_filepath):
    with open(seed_filepath, "w", encoding="utf-8") as f:
        f.write("Write your starting prompt or question here.")
    print("⚠️ Created 'seed_prompt.md'. Please write your starting prompt and run again.")
    exit()

# Attachments Setup
attachments_dir = os.path.join(target_dir, "prompt_files")
if not os.path.exists(attachments_dir):
    os.makedirs(attachments_dir)

with open(seed_filepath, "r", encoding="utf-8") as f:
    base_prompt = f.read().strip()

if base_prompt == "Write your starting prompt or question here." or not base_prompt:
    print("❌ Please update 'seed_prompt.md' with your actual question before running.")
    exit()

# Extract attachments text
attached_text = ""
for filename in os.listdir(attachments_dir):
    filepath = os.path.join(attachments_dir, filename)
    if filename.endswith((".txt", ".md")):
        with open(filepath, "r", encoding="utf-8") as file:
            attached_text += f"\n\n--- START ATTACHED FILE: {filename} ---\n{file.read()}\n--- END ATTACHED FILE ---\n"
    elif filename.endswith(".docx"):
        try:
            doc = Document(filepath)
            doc_text = "\n".join([para.text for para in doc.paragraphs])
            attached_text += f"\n\n--- START ATTACHED FILE: {filename} ---\n{doc_text}\n--- END ATTACHED FILE ---\n"
        except Exception:
            pass

current_input = base_prompt + attached_text

# ==========================================
# 3. TERMINAL UI (Model Selection)
# ==========================================
def select_model(role, model_list):
    print(f"\n=== SELECT YOUR {role.upper()} ===")
    for idx, model in enumerate(model_list):
        print(f"{idx + 1}. {model}")
    
    if role == "bs detector (optional)":
        print("0. Skip (Run standard 2-way debate)")
        
    choice = input("> ")
    if role == "bs detector (optional)" and (choice == "0" or choice == ""):
        return None
    try:
        return model_list[int(choice) - 1]
    except:
        return model_list[0]

senior_model = select_model("senior ai", available_models["senior"])
junior_model = select_model("junior ai", available_models["junior"])
bs_model = select_model("bs detector (optional)", available_models["grounding"])

rounds_input = input("\nHow many rounds would you like them to debate? (e.g., 5): ")
total_rounds = int(rounds_input) if rounds_input.isdigit() else 5

# ==========================================
# 4. INITIALIZE PERSONAS & MEMORY
# ==========================================
GEMINI_PERSONA = (
    "You are a senior, highly experienced AI. Analyze the user's queries or the "
    "counter-arguments provided. Offer your expert opinion, cut through the fluff, "
    "and provide a definitive, authoritative answer."
)
DEEPSEEK_PERSONA = (
    "You are an inquisitive, highly analytical Junior AI. Analyze the statements provided "
    "from a fresh perspective, point out nuances or alternative viewpoints, and ALWAYS "
    "end your response with a highly introspective, open-ended leading question."
)
BS_PERSONA = (
    "You are a ruthless fact-checker and grounding agent. Review the Senior and Junior AIs' "
    "preceding exchange. Identify any unproven assumptions, logical fallacies, or hypothetical hype. "
    "Ground the conversation back in reality and empirical fact before the next round begins. "
    "Be concise and direct."
)

gemini_chat = gemini_client.chats.create(
    model=senior_model, 
    config=types.GenerateContentConfig(system_instruction=GEMINI_PERSONA)
)

junior_messages = [{"role": "system", "content": DEEPSEEK_PERSONA}]
bs_messages = [{"role": "system", "content": BS_PERSONA}] if bs_model else []

junior_messages.append({"role": "user", "content": f"The starting topic is provided below.\n\n{current_input}"})
if bs_model:
    bs_messages.append({"role": "user", "content": f"The starting topic is provided below.\n\n{current_input}"})

# ==========================================
# 5. THE 3-WAY ADVERSARIAL LOOP
# ==========================================
markdown_log = f"# AI Debate Log\n**Topic:** {base_prompt[:100]}...\n**Rounds:** {total_rounds}\n---\n\n"
with open("debate_log.md", "w", encoding="utf-8") as f:
    f.write(markdown_log)

print("\n[Starting the Debate Loop...]\n")

for i in range(total_rounds):
    print(f"--- Round {i+1} of {total_rounds} ---")
    
    # 1. GEMINI (Senior - Native SDK)
    print("Gemini (Senior) is thinking...")
    gemini_response = gemini_chat.send_message(current_input)
    gemini_text = gemini_response.text
    
    with open("debate_log.md", "a", encoding="utf-8") as f:
        f.write(f"### Senior AI ({senior_model}) - Round {i+1}\n{gemini_text}\n\n---\n\n")
    markdown_log += f"### Senior AI - Round {i+1}\n{gemini_text}\n\n"

    # 2. DEEPSEEK (Junior - Via OpenRouter)
    print("DeepSeek (Junior) is interrogating...")
    junior_messages.append({"role": "user", "content": gemini_text})
    
    ds_response = openrouter_client.chat.completions.create(
        model=junior_model,
        messages=junior_messages
    )
    ds_text = ds_response.choices[0].message.content
    junior_messages.append({"role": "assistant", "content": ds_text})
    
    with open("debate_log.md", "a", encoding="utf-8") as f:
        f.write(f"### Junior AI ({junior_model}) - Round {i+1}\n{ds_text}\n\n---\n\n")
    markdown_log += f"### Junior AI - Round {i+1}\n{ds_text}\n\n"

    current_input = ds_text

    # 3. QWEN (BS Detector - Via OpenRouter)
    if bs_model:
        print("Qwen (BS Detector) is fact-checking...")
        bs_payload = f"SENIOR SAID:\n{gemini_text}\n\nJUNIOR SAID:\n{ds_text}\n\nPlease fact-check and ground this."
        bs_messages.append({"role": "user", "content": bs_payload})
        
        qwen_response = openrouter_client.chat.completions.create(
            model=bs_model,
            messages=bs_messages
        )
        qwen_text = qwen_response.choices[0].message.content
        bs_messages.append({"role": "assistant", "content": qwen_text})
        
        with open("debate_log.md", "a", encoding="utf-8") as f:
            f.write(f"### BS Detector ({bs_model}) - Round {i+1}\n{qwen_text}\n\n---\n\n")
        markdown_log += f"### BS Detector - Round {i+1}\n{qwen_text}\n\n"
        
        # Cross-pollinate critique and leading question back to Gemini
        current_input = f"JUNIOR QUESTION: {ds_text}\n\nBS DETECTOR CRITIQUE: {qwen_text}\n\nAddress both in your next response."

# ==========================================
# 6. EXECUTIVE SUMMARY (Word Doc Generation)
# ==========================================
print("\n[Debate Complete! Generating Executive Summary Word Document...]")

summary_prompt = f"""
You are an executive summarizer. Review the preceding AI debate transcript. 
Identify the core disagreements, the points of consensus, and the most profound 
open questions or hidden vulnerabilities raised. 

Format your response using ONLY clean Markdown headings (## ) and bullet points (* ). 
DO NOT use asterisks for bolding (**). Write in clear, professional plain text.

DEBATE TRANSCRIPT:
{markdown_log}
"""

try:
    summary_response = gemini_client.models.generate_content(
        model=senior_model,
        contents=summary_prompt
    )
    
    doc = Document()
    doc.styles['Normal'].font.name = 'Calibri'
    doc.styles['Normal'].font.size = Pt(11)
    
    title_style = doc.styles['Title']
    title_style.font.name = 'Calibri'
    title_style.font.bold = True
    title_style.font.color.rgb = RGBColor(17, 85, 204)
    
    doc.add_heading('AI Debate: Executive Summary', 0)
    
    for line in summary_response.text.split('\n'):
        clean_line = line.replace('**', '').strip()
        if clean_line.startswith('## '):
            doc.add_heading(clean_line.replace('## ', ''), level=1)
        elif clean_line.startswith('### '):
            doc.add_heading(clean_line.replace('### ', ''), level=2)
        elif clean_line.startswith('* ') or clean_line.startswith('- '):
            doc.add_paragraph(clean_line[2:], style='List Bullet')
        elif clean_line:
            doc.add_paragraph(clean_line)
            
    doc.save("Executive_Summary.docx")
    print("✅ Success! Executive summary saved to 'Executive_Summary.docx'.")

except Exception as e:
    print(f"⚠️ Error generating summary: {e}")

print("\n=== SCRIPT 1 COMPLETE ===")