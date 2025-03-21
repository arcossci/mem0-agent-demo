from agency_swarm import Agent
from .tools.memory_tools import MemoryTools
import os
from dotenv import load_dotenv

load_dotenv()

class KeyAccountManager(Agent):
    def __init__(self, openai_api_key=None):
        super().__init__(
            name="Key Account Manager",
            description="Main interface between customer and agency, managing coordination and memory.",
            instructions="./instructions.md",
            tools=MemoryTools.get_tools(),
            temperature=0.7,
            max_prompt_tokens=4000
        )
        if openai_api_key:
            self.client.api_key = openai_api_key 