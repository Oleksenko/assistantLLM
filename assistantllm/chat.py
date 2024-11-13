import os
import json
import subprocess
from openai import OpenAI
from rich.console import Console
from rich.text import Text
from rich.syntax import Syntax

# Инициализация консоли rich
console = Console()

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
    {"role": "system", "content": "You are a helpful assistant for a software project. If a user asks for a terminal command, provide the command clearly."}
]

def execute_command(command):
    """Выполняет команду в терминале и возвращает результат."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()  # Успешный результат
        else:
            return f"[red]Error:[/red] {result.stderr.strip()}"  # Ошибка выполнения
    except Exception as e:
        return f"[red]Failed to execute command:[/red] {e}"

def detect_and_execute_command(reply):
    """Определяет, содержит ли ответ команду, и выполняет её."""
    if "```" in reply:
        # Извлекаем содержимое команды между ``` и ```
        command = reply.split("```")[1].strip()
        console.print(f"[bold yellow]Detected Command:[/bold yellow] {command}")
        result = execute_command(command)
        console.print(f"[bold yellow]Command Output:[/bold yellow]")
        console.print(result)

def chat():
    console.print("[bold green]Starting LLM assistant. Type 'exit' to quit.[/bold green]")
    while True:
        user_input = console.input("[bold blue]You:[/bold blue] ")

        if user_input.lower() == "exit":
            console.print("[bold red]Goodbye![/bold red]")
            break
        
        # Добавляем сообщение пользователя в историю
        conversation_history.append({"role": "user", "content": user_input})
        
        # Отправляем запрос к OpenAI API
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=conversation_history
            )
            reply = response.choices[0].message.content.strip()

            # Проверяем, если ответ содержит команду
            detect_and_execute_command(reply)

            # Проверяем, если ответ это просто текст
            if not "```" in reply:
                console.print(f"[bold green]Assistant:[/bold green] {reply}")

            # Добавляем ответ в историю
            conversation_history.append({"role": "assistant", "content": reply})
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")

def main():
    chat()
