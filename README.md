# AgentPro_saadlahori
AgentPro is a lightweight ReAct-style agentic framework built in Python, designed for structured reasoning step-by-step using available tools, while maintaining a complete history of Thought → Action → Observation → PAUSE → Final Answer steps.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-Apache%202.0-blue" alt="License: Apache 2.0">
</p>

## 📚 Features

- 🔥 ReAct (Reasoning + Acting) agent pattern
- 🛠️ Modular tool system (easy to add your own tools)
- 📜 Clean Thought/Action/Observation/PAUSE parsing
- 📦 Local package structure for easy extension
- 🧠 Powered by any LLM! (Anthropic, Open AI or any other Open source LLMs)

## Quick Start
- Goto: https://github.com/saadlahori/AgentPro_saadlahori_final
- Run Streamlit Interface from app_final_saadlahori.py

### Installation

Install agentpro repository using pip:

```bash
pip install git+https://github.com/traversaal-ai/AgentPro.git -q
```
<!--
### Configuration

Create a `.env` file in the root directory with your API keys:

```
OPENAI_API_KEY=your_openai_api_key
TRAVERSAAL_ARES_API_KEY=your_traversaal_ares_api_key
UNSPLASH_ACCESS_KEY = Your Unplash Key
ELEVENLABS_API_KEY"] = Your Eleven Labs Key
OPENWEATHER_API_KEY = Your Open Weather Key
```
Ares internet tool: Searches the internet for real-time information using the Traversaal Ares API. To get `TRAVERSAAL_ARES_API_KEY`. Follow these steps:

1. Go to the [Traversaal API platform](https://api.traversaal.ai/)
2. Log in or create an account
3. Click **"Create new secret key"**
4. Copy the generated key and paste in `.env` file :
5. Similarly do it for all Tools to fetch API Keys

### Running the Agent

From the command line:

```bash
python main.py
```

This starts an interactive session with the agent where you can enter queries. -->

### Basic Usage
```python
import os
from agentpro import ReactAgent
from agentpro.tools import AresInternetTool
from agentpro import create_model

# Create a model with OpenAI
model = create_model(provider="openai", model_name="gpt-4o", api_key=os.getenv("OPENAI_API_KEY", None))

# Initialize tools
tools = [AresInternetTool(os.getenv("ARES_API_KEY", None))]

# Initialize agent
agent = ReactAgent(model=model, tools=tools)

# Run a query
query = "What is the height of the Eiffel Tower?"
response = agent.run(query)

print(f"\nFinal Answer: {response.final_answer}")
```

For more details, contact or email me

📩 Questions? Reach us at [saadlahori@gmail.com)

## 🛠️ Creating Custom Tools

You can create your own tools by extending the `Tool` base class provided in `agentpro`.

Here’s a basic example:

```python
from agentpro.tools import Tool
from typing import Any

class MyCustomTool(Tool):
    name: str = "My Custom Tool"  # Human-readable name for the tool (used in documentation and debugging)
    description: str = "Description"  # Brief summary explaining the tool's functionality for agent
    action_type: str = "my_custom_action"  # Unique identifier for the tool; lowercase with underscores for agent; avoid spaces, digits, special characters
    input_format: str = "Description of expected input format, e.g., a string query."  # Instruction on what kind of input the tool expects with example

    def run(self, input_text: Any) -> str:
        # your tool logic
        return "Result of your custom tool."

```

After creating your custom tool, you can initialize it and pass it to AgentPro like this:

```python
import os
from agentpro import ReactAgent
from agentpro import create_model

# Create a model with OpenAI
model = create_model(provider="openai", model_name="gpt-4o", api_key=os.getenv("OPENAI_API_KEY", None))

# Instantiate your custom tools
tools = [MyCustomTool()]

# Create AgentPro React agent
myagent = ReactAgent(model=model,tools=tools)

# Run a query
query = "Use the custom tool to perform a task."
response = myagent.run(query)

print(response.final_answer)
```

## Project Structure

```
AgentPro/
├── agentpro/
│   ├── __init__.py
│   ├── react_agent.py                  # Core AgentPro class implementing react-style agent framework
│   ├── agent.py                        # Action, Observation, ThoughtStep, AgentResponse classes
│   ├── model.py                        # Model classes 
│   ├── tools/ (                          # folder for all tool classes (Base by Traversal AI)
│       ├── __init__.py
│       ├── base_tool.py
│       ├── duckduckgo_tool.py
│       ├── calculator_tool.py
│       ├── userinput_tool.py
│       ├── ares_tool.py
│       ├── traversaalpro_rag_tool.py
│       ├── slide_generation_tool.py
│       └── yfinance_tool.py
│   ├── tools/                      # folder for all tool classes (Custom by Saad Saleem, Radiant Technologies )
│       ├── custom_tool_weather_map.py
│       ├── custom_tool_texttospeech_Elevenlabs.py
│       ├── custom_tool_unsplash_Image.py
│       ├── custom_tool_text_to_image.py
│       ├── custom_tool_huggingface.py
├── cookbook/
│   ├── Traversaal x Optimized AI Hackathon 2025
│   ├── quick_start.ipynb
│   └── custool_tool.ipynb   
├── app_final_saadlahori.py     # Main Streamlit GUI Integrated Interface
├── main.py                             # Entrypoint to run the agent
├── requirements.txt                    # Dependencies
├── README.md                           # Project overview, usage instructions, and documentation
├── setup.py       
├── pyproject.toml     
└── LICENSE.txt                         # Open-source license information (Apache License 2.0)
```

## Requirements
- All listed in requirement.txt
- Python 3.8+
- OpenAI API key
- Traversaal Ares API key for internet search (Optional)
- Eleven Labs TTS
- Open Weather
- Unsplash

## License & Link
Goto: https://github.com/saadlahori/AgentPro_saadlahori_final
This project is licensed under the Apache 2.0 License and build in Visual Studio Code - see the LICENSE file for more details.
