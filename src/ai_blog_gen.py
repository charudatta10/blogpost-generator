from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
import chainlit as cl
from ollama import generate as Client

# Initialize FastAPI & MCP Server
app = FastAPI()
mcp = FastMCP("BlogTools")

# Markdown Reader Tool
@mcp.tool()
def read_markdown(file_path: str) -> str:
    """Reads a Markdown file and returns its content."""
    with open(file_path, "r") as f:
        return f.read()

# Initialize LangChain LLM with Phi-3
# Initialize Ollama client with the Phi-3 model
ollama_client = Client()
MODEL_NAME = "llama3.2:1b"

def llm(prompt: str) -> str:
    """Send prompt to Ollama and return the response."""
    response = ollama_client.generate(model=MODEL_NAME, prompt=prompt)
    return response['response']

# Define tools available to the agent
tools = [
    Tool(name="ReadMarkdown", func=read_markdown, description="Reads a Markdown file."),
]

# Initialize LangChain Agent
agent = initialize_agent(tools, llm, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION)

# Chainlit for UI
@cl.on_message
async def handle_message(message):
    """Handles incoming user messages and generates AI responses."""
    response = agent.run(message.content)
    await cl.Message(content=response).send()

# Start MCP Server
if __name__ == "__main__":
    mcp.run(transport="stdio")
    print("MCP Server is running...")
# To run the server, use the command:
# uvicorn ai_blog_gen:app --reload