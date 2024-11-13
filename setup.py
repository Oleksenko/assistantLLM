import os
import json

def create_config():
    config_path = os.path.join(os.getcwd(), "assistantLLM_config.json")
    if not os.path.exists(config_path):
        config_data = {
            "OPENAI_API_KEY": "your-api-key-here"  # Заглушка для ключа
        }
        with open(config_path, "w") as f:
            json.dump(config_data, f, indent=4)
        print(f"Config file created at {config_path}. Please update the OPENAI_API_KEY.")

def add_to_gitignore():
    gitignore_path = os.path.join(os.getcwd(), ".gitignore")
    entries = ["assistantLLM/", "assistantLLM_config.json"]
    if not os.path.exists(gitignore_path):
        with open(gitignore_path, "w") as f:
            f.write("\n".join(entries) + "\n")
    else:
        with open(gitignore_path, "r") as f:
            lines = f.readlines()
        with open(gitignore_path, "a") as f:
            for entry in entries:
                if entry not in lines:
                    f.write(f"{entry}\n")

# Добавляем оба действия в процесс установки
create_config()
add_to_gitignore()