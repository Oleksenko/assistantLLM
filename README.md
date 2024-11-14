# AssistantLLM

AssistantLLM is a GPT-powered tool designed to help developers analyze code, generate tests, execute terminal commands, and answer project-related questions.

---

## **Features**

AssistantLLM provides the following features:

1. **Chat with GPT to assist in development:**
   - Answer programming and technology-related questions.
   - Generate ideas, improvements, and tests for your code.

2. **File analysis:**
   - Read file content.
   - Analyze code and provide explanations and recommendations.

3. **Execute terminal commands:**
   - Recognize and execute commands directly from the chat.
   - Request confirmation before executing commands.

4. **Interactive testing:**
   - Support for testing individual commands and file analysis.

---

## **Installation**

### **Prerequisites**

Before installation, ensure you have the following components installed:

- Python 3.9 or later.
- pip (Python package manager).
- `git` installed on your system.

### **Installation Steps**

1. **Install via pip:**

   Run the following command:
   ```bash
   pip install git+https://github.com/Oleksenko/assistantLLM.git
   ```
### **Set up the API key**

2. Create a file named `assistantLLM_config.json` in the root directory of your project. (This file is created automatically during installation if it doesn't exist.)
3. Add your OpenAI API key to the file:
   ```json
   {
       "OPENAI_API_KEY": "your-openai-api-key"
   }
   ```

