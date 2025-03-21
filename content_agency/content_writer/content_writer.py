from agency_swarm import Agent
import os
from dotenv import load_dotenv

load_dotenv()

class ContentWriter(Agent):
    def __init__(self, openai_api_key=None):
        super().__init__(
            name="Content Writer",
            description="Generates high-quality written content based on research and customer requirements.",
            instructions="./instructions.md",
            tools_folder="./tools",
            temperature=0.8,
            max_prompt_tokens=4000
        )
        if openai_api_key:
            self.client.api_key = openai_api_key 