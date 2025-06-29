import os
import json
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EMBED_MODEL = "all-MiniLM-L6-v2"
VECTOR_DB_PATH = "code_memory"
PROJECT_MAP_FILE = "project_map.json"
LOG_FILE = os.path.join("logs", "injector_log.json")
os.makedirs("logs", exist_ok=True)

def log_injection(instruction, file_path, summary=None):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "instruction": instruction,
        "file_modified": file_path,
        "summary": summary or "Change applied"
    }
    # Read existing log or start a new list
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            try:
                log = json.load(f)
                if isinstance(log, dict):
                    log = [log]
            except json.JSONDecodeError:
                log = []
    else:
        log = []
    log.append(entry)
    # Write the updated log as a JSON array
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)

def choose_file_with_gpt(instruction):
    with open(PROJECT_MAP_FILE, "r") as f:
        project_map = json.load(f)

    file_prompt = f"""
You are part of an AI assistant that modifies code files.

Given this instruction:
"{instruction}"

And this list of files and their purposes:
{json.dumps(project_map, indent=2)}

Return ONLY the filename that should be modified. No explanation.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an intelligent file selector."},
            {"role": "user", "content": file_prompt}
        ],
        temperature=0
    )

    selected_file = response.choices[0].message.content.strip().strip('"')
    print(f"[🧠] GPT chose to modify: {selected_file}")
    return selected_file


def inject_feature(instruction, model="gpt-4"):
    print("[→] Using project map to determine best file...")

    file_path = choose_file_with_gpt(instruction)
    if not os.path.exists(file_path):
        print(f"[✗] Selected file not found: {file_path}")
        return

    with open(file_path, "r") as f:
        original_code = f.read()

    system_prompt = (
        "You are an autonomous coding agent. You will receive an instruction "
        "and the full content of a target code file. Apply the instruction intelligently. "
        "Output ONLY the updated full file content."
    )

    user_prompt = f"""
INSTRUCTION:
{instruction}

FILE: {file_path}

CURRENT FILE CONTENT:
{original_code}
"""

    print("[→] Asking GPT to modify the file...")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
        max_tokens=3000
    )

    updated_code = response.choices[0].message.content.strip()

    # Backup and write
    backup_path = file_path + ".bak"
    os.rename(file_path, backup_path)
    with open(file_path, "w") as f:
        f.write(updated_code)

    print(f"[✓] File updated: {file_path}")
    print(f"[📦] Backup created: {backup_path}")

    log_injection(instruction, file_path)


# Optional test run
if __name__ == "__main__":
    test_instruction = "Add a function to list all previous instructions logged in injector_log.json"
    inject_feature(test_instruction)