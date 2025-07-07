# dev_utils/injector.py

import os
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROJECT_MAP_FILE = "dev_utils/project_map.json"
LOG_FILE = "logs/injector_log.json"
os.makedirs("logs", exist_ok=True)

def log_injection(instruction, file_path, summary="Change applied"):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "instruction": instruction,
        "file_modified": file_path,
        "summary": summary
    }

    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                log = json.load(f)
        except json.JSONDecodeError:
            log = []
    else:
        log = []

    log.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)

def choose_file_with_gpt(instruction):
    with open(PROJECT_MAP_FILE, "r") as f:
        project_map = json.load(f)

    prompt = f"""
Instruction:
"{instruction}"

Files and roles:
{json.dumps(project_map, indent=2)}

Return ONLY the best file path to modify.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a smart code assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip().strip('"')

def inject_feature(instruction, model="gpt-4"):
    print("[→] Choosing target file...")
    file_path = choose_file_with_gpt(instruction)

    if not os.path.exists(file_path):
        print(f"[✗] File not found: {file_path}")
        return

    with open(file_path, "r") as f:
        original = f.read()

    prompt = f"""
You are a helpful AI that modifies Python files based on user instructions.

Instruction:
{instruction}

Original code:
{original}
"""

    print("[→] Sending to GPT...")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an autonomous coding agent. Return the updated full file only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=3000
    )

    updated = response.choices[0].message.content.strip()

    backup = file_path + ".bak"
    if os.path.exists(backup):
        os.remove(backup)
    os.rename(file_path, backup)

    with open(file_path, "w") as f:
        f.write(updated)

    print(f"[✓] Updated: {file_path} (backup saved)")
    log_injection(instruction, file_path)

# Optional test run
if __name__ == "__main__":
    test_instruction = "Add a function to clear the memory_log.json file"
    inject_feature(test_instruction)
