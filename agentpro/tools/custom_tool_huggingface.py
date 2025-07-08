# HuggingFace_MostFamousModelsSearch.py

# Imports
import os
from agentpro import ReactAgent
from agentpro.tools import Tool
from huggingface_hub import list_models
from typing import Any
from agentpro import create_model

class MostModelTool(Tool):
    name: str = "Most Downloaded Model Finder" # Human-readable tool name
    description: str = "Finds the most downloaded model for a given task on Hugging Face." # Brief explanation of tool for agent
    action_type: str = "find_top_model" # Use lowercase letters with underscores for agent; avoid spaces, digits and special characters
    input_format: str = "Task name as a string. Example: 'text-classification'" # Expected input dtype with example

    def run(self, input_text: Any) -> str:
        task_name = input_text.strip()
        models = list_models(filter=task_name, sort="downloads", direction=-1)
        top_model = next(models)
        return top_model.id