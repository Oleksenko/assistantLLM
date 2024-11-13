from setuptools import setup, find_packages
import os
import json

# Функция для создания файла конфигурации
def create_config():
    config_path = os.path.join(os.getcwd(), "assistantLLM_config.json")
    if not os.path.exists(config_path):
        config_data = {
            "OPENAI_API_KEY": "your-api-key-here"  # Заглушка для ключа
        }
        with open(config_path, "w") as f:
            json.dump(config_data, f, indent=4)
        print(f"Config file created at {config_path}. Please update the OPENAI_API_KEY.")

# Функция для добавления в .gitignore
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

# Вызов функций при установке
create_config()
add_to_gitignore()

# Основной setup
setup(
    name="assistantLLM",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai",  # Для взаимодействия с OpenAI API
    ],
    entry_points={
        "console_scripts": [
            "assistantLLM=assistantllm.chat:main",  # Команда для запуска проекта
        ],
    },
    description="LLM assistant for project development",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/Oleksenko/assistantLLM",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)