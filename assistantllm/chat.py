import os
import json
import subprocess
from openai import OpenAI

# Загружаем API-ключ из конфигурации
def load_api_key():
    config_path = os.path.join(os.getcwd(), "assistantLLM_config.json")
    if not os.path.exists(config_path):
        raise FileNotFoundError("Config file assistantLLM_config.json not found. Please re-install or create the file.")

    with open(config_path, "r") as f:
        config = json.load(f)

    if "OPENAI_API_KEY" not in config or not config["OPENAI_API_KEY"]:
        raise ValueError("OPENAI_API_KEY is not set in assistantLLM_config.json.")

    return config["OPENAI_API_KEY"]

# Инициализируем клиента OpenAI
client = OpenAI(
    api_key=load_api_key()
)

# История диалога
conversation_history = [
    {"role": "system", "content": "You are a helpful assistant for a software project."}
]

def execute_command(command):
    """Выполняет команду в терминале и возвращает результат."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()  # Успешный результат
        else:
            return f"Error: {result.stderr.strip()}"  # Ошибка выполнения
    except Exception as e:
        return f"Failed to execute command: {e}"

def chat():
    print("Starting LLM assistant. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        # Добавляем сообщение пользователя в историю
        conversation_history.append({"role": "user", "content": user_input})
        
        # Проверяем, нужно ли выполнить команду
        if user_input.startswith("run:") or user_input.startswith("exec:"):
            command = user_input.split(":", 1)[1].strip()
            result = execute_command(command)
            print(f"Command Output:\n{result}")
            # Возвращаемся в диалог, добавляя результат выполнения команды
            conversation_history.append({"role": "assistant", "content": f"Command executed:\n{result}"})
            continue
        
        # Отправляем запрос к OpenAI API
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=conversation_history
            )
            reply = response.choices[0].message.content.strip()
            print(f"Assistant: {reply}")
            # Добавляем ответ в историю
            conversation_history.append({"role": "assistant", "content": reply})
        except Exception as e:
            print(f"Error: {e}")

def main():
    chat()