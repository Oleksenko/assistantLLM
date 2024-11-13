import os
import json
import subprocess
from openai import OpenAI
from rich.console import Console
from rich.text import Text
from rich.syntax import Syntax
from file_reader import read_file_content, file_exists, is_project_file

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
    """Выполняет команду в терминале с обработкой вывода."""
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in process.stdout:
            console.print(line.strip())
        process.wait()
        if process.returncode == 0:
            return "[bold green]Command executed successfully![/bold green]"
        else:
            return f"[red]Error:[/red] Command failed with exit code {process.returncode}"
    except Exception as e:
        return f"[red]Failed to execute command:[/red] {e}"

def detect_and_confirm_command(reply):
    """Определяет, содержит ли ответ команду, и спрашивает, нужно ли её выполнить."""
    if "```" in reply:
        command = reply.split("```")[1].strip()
        console.print(f"[bold yellow]Detected Command:[/bold yellow] {command}")

        user_input = console.input("[bold cyan]Execute this command? (Yes/No):[/bold cyan] ").strip().lower()
        if user_input == "yes":
            result = execute_command(command)
            console.print(f"[bold yellow]Command Output:[/bold yellow]")
            console.print(result)
            return f"Command executed:\n{result}"
        elif user_input == "no":
            console.print("[bold green]Command not executed. Returning to chat.[/bold green]")
            return "Command detected but not executed."
    return reply

def analyze_file(file_path, project_dir):
    """Читает и анализирует содержимое файла."""
    if not is_project_file(project_dir, file_path):
        return f"[red]Error:[/red] File {file_path} is outside the project directory."

    content, error = read_file_content(file_path)
    if error:
        return error

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=conversation_history + [{"role": "user", "content": f"Analyze the following code:\n\n{content}"}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[red]Error interacting with LLM:[/red] {e}"

def chat():
    console.print("[bold green]Starting LLM assistant. Type 'exit' to quit.[/bold green]")
    project_dir = os.getcwd()
    while True:
        user_input = console.input("[bold blue]You:[/bold blue] ")

        if user_input.lower() == "exit":
            console.print("[bold red]Goodbye![/bold red]")
            break
        
        # Проверяем, является ли ввод путём к файлу
        if file_exists(user_input):
            console.print(f"[bold yellow]File detected:[/bold yellow] {user_input}")
            result = analyze_file(user_input, project_dir)
            console.print(f"[bold yellow]Analysis Result:[/bold yellow]\n{result}")
            continue

        # Добавляем сообщение пользователя в историю
        conversation_history.append({"role": "user", "content": user_input})
        
        # Отправляем запрос к OpenAI API
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=conversation_history
            )
            reply = response.choices[0].message.content.strip()

            modified_reply = detect_and_confirm_command(reply)

            if not modified_reply.startswith("Command executed") and not modified_reply.startswith("Command detected"):
                console.print(f"[bold green]Assistant:[/bold green] {modified_reply}")

            conversation_history.append({"role": "assistant", "content": reply})
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")

def main():
    chat()