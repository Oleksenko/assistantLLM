import os
import json
import subprocess
from openai import OpenAI
from rich.console import Console
from rich.text import Text
from rich.syntax import Syntax

console = Console()

def load_api_key():
    config_path = os.path.join(os.getcwd(), "assistantLLM_config.json")
    if not os.path.exists(config_path):
        raise FileNotFoundError("Config file assistantLLM_config.json not found.")

    with open(config_path, "r") as f:
        config = json.load(f)

    if "OPENAI_API_KEY" not in config or not config["OPENAI_API_KEY"]:
        raise ValueError("OPENAI_API_KEY is not set in assistantLLM_config.json.")

    return config["OPENAI_API_KEY"]

client = OpenAI(
    api_key=load_api_key()
)

conversation_history = [
    {"role": "system", "content": "You are a helpful assistant for analyzing code and answering software-related questions."}
]

def read_file_content(file_path):
    if not os.path.exists(file_path):
        return None, f"File {file_path} not found."
    try:
        with open(file_path, "r") as file:
            content = file.read()
        return content, None
    except Exception as e:
        return None, f"Error reading file {file_path}: {e}"

def analyze_file(file_path):
    content, error = read_file_content(file_path)
    if error:
        return error

    max_lines = 100
    lines = content.split("\n")
    if len(lines) > max_lines:
        content = "\n".join(lines[:max_lines]) + "\n... [Truncated: File too large]"

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=conversation_history + [{"role": "user", "content": f"Analyze the following code:\n\n{content}"}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error interacting with LLM: {e}"

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"[red]Error:[/red] {result.stderr.strip()}"
    except Exception as e:
        return f"[red]Failed to execute command:[/red] {e}"

def detect_and_confirm_command(reply):
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

def chat():
    console.print("[bold green]Starting LLM assistant. Type 'exit' to quit.[/bold green]")
    project_dir = os.getcwd()
    while True:
        user_input = console.input("[bold blue]You:[/bold blue] ")

        if user_input.lower() == "exit":
            console.print("[bold red]Goodbye![/bold red]")
            break
        
        possible_path = os.path.join(project_dir, user_input)
        if os.path.isfile(possible_path):
            console.print(f"[bold yellow]File detected:[/bold yellow] {user_input}")
            result = analyze_file(possible_path)
            console.print(f"[bold yellow]Analysis Result:[/bold yellow]\n{result}")
            continue

        conversation_history.append({"role": "user", "content": user_input})
        
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
