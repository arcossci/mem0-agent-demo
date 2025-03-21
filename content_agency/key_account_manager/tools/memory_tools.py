from agency_swarm.tools import BaseTool
from pydantic import Field
from mem0 import MemoryClient

# Initialize the MemoryClient with API key
client = MemoryClient(api_key="m0-WSQJiEuFlgHRBKZmjBLou2BgptgqdjPqfo8t71bC")

# Define a default app_id for our content agency
APP_ID = "content_agency_v1"

# Define default user ID for persistence
DEFAULT_USER_ID = "jeff001"

class MemoryTools:
    """
    A collection of memory-related tools for the Key Account Manager.
    """
    @staticmethod
    def get_tools():
        return [SeachMemory, UpdateMemory, DeleteMemory]

class SeachMemory(BaseTool):
    """
    Retrieves relevant memories based on a the complete user's message query.
    """

    customer_id: str = Field(
        default=DEFAULT_USER_ID, 
        description="Unique identifier for the user whose memories are being searched."
    )
    query: str = Field(
        ..., 
        description="the complete message query to search for relevant stored memories."
    )

    def run(self):
        """
        Searches for stored memories that match the user's query and return it.
        """

        try:
            # Perform a memory search using the specified query and filters.
            # The system will return a list of matching memory entries.
            memories = client.search(
                query=self.query,
                user_id=self.customer_id,  # Ensure the correct customer ID is used
                version="v2",
                keyword_search=True
            )
            
            # Check if relevant memories were found
            if isinstance(memories, list) and memories:
                # Format retrieved memories into a readable list
                formatted_memories = "\n".join(f"- {entry['memory']}" for entry in memories)
                return f"Relevant memories found for '{self.query}':\n{formatted_memories}"
            
            return f"No relevant memories found for '{self.query}'."

        except Exception as e:
            return f"Error retrieving memories: {str(e)}"

class UpdateMemory(BaseTool):
    """
    Store a message into long-term memory
    """
    customer_id: str = Field(
        default=DEFAULT_USER_ID, description="The unique identifier for the customer"
    )
    message: str = Field(
        ..., description="Message string to store in memory.",
    )

    def run(self):
        """
        Store the message in memory and return a confirmation.
        """
        try:
            # Format the memory as a message
            memory = {
                "role": "assistant",
                "content": self.message,
            }
            # Add the memory using the documented format
            client.add([memory], user_id=self.customer_id)
            return f"Successfully updated message for customer {self.customer_id}"
        except Exception as e:
            return f"Error updating memory: {str(e)}"


class DeleteMemory(BaseTool):
    """
    Handles memory deletion requests naturally during a chat with the AI agent.
    It first searches for the most relevant memory before attempting deletion.
    """
    query: str = Field(
        ..., description="The search query to find the most relevant memory before deletion."
    )
    customer_id: str = Field(
        default="jeff", description="The unique identifier for the customer making the request."
    )

    def run(self):
        """
        Searches for the most relevant memory, retrieves its ID, and then deletes it.
        """

        try:
            # Search for the most relevant memory before deletion
            search_results = client.search(query=self.query, user_id=self.customer_id)
            
            if not search_results or "results" not in search_results or not search_results["results"]:
                return f"I couldn't find any memory related to '{self.query}'. Are you sure it exists?"
            
            # Select the most relevant memory (first result)
            most_relevant_memory = search_results["results"][0]
            memory_id = most_relevant_memory["id"]
            
            client.delete(memory_id=memory_id)
            
            return f"Got it! I’ve deleted the most relevant memory related to '{self.query}'."
        except Exception as e:
            return f"Hmm, I ran into an issue deleting that memory: {str(e)}"



