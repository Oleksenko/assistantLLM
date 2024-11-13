import os
import json
import openai

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

# Устанавливаем ключ OpenAI API
openai.api_key = load_api_key()

def chat():
    print("Starting LLM assistant. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        # Отправляем запрос к OpenAI API
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for a software project."},
                    {"role": "user", "content": user_input}
                ]
            )
            reply = response['choices'][0]['message']['content']
            print(f"Assistant: {reply}")
        except Exception as e:
            print(f"Error: {e}")

def main():
    chat()