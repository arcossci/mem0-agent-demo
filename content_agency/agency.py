from agency_swarm import Agency
from key_account_manager.key_account_manager import KeyAccountManager
from content_writer.content_writer import ContentWriter
from researcher.researcher import Researcher

# Set API keys directly
OPENAI_API_KEY = "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"
MEM0_API_KEY = "m0-WSQJiEuFlgHRBKZmjBLou2BgptgqdjPqfo8t71bC"

# Initialize agents
kam = KeyAccountManager(openai_api_key=OPENAI_API_KEY)
writer = ContentWriter(openai_api_key=OPENAI_API_KEY)
researcher = Researcher(openai_api_key=OPENAI_API_KEY)

# Create agency with communication flows
agency = Agency(
    [
        kam,  # Key Account Manager is the entry point
        [kam, writer],  # KAM can communicate with Content Writer
        [kam, researcher],  # KAM can communicate with Researcher
        [researcher, writer],  # Researcher can communicate with Content Writer
    ],
    shared_instructions="agency_manifesto.md",
    temperature=0.7,
    max_prompt_tokens=4000
)

if __name__ == "__main__":
    agency.run_demo()  # Start the agency in terminal mode 