import os 
import asyncio
import certifi
from dotenv import load_dotenv  
from langchain_mcp_adapters.client import MultiServerMCPClient

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUEST_CA_BUNDLE"] = certifi.where()


load_dotenv()


TAVILY_API_KEY = os.getenv("TAVILY_API_KEY") 
AVIATION_API_KEY = os.getenv("AVIATION_API_KEY")


client = MultiServerMCPClient( 
    {
        "tavily-remote": {
        "transport": "streamable_http",
        "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_API_KEY}"
    },

    
    "Aviationstack MCP": {
        "transport": "stdio",
        "command": "uvx",
        "args": [
        "aviationstack-mcp"
      ],
      "env": {
        "AVIATION_STACK_API_KEY": AVIATION_API_KEY
      }
    }
}
    
)


async def get_all_tools():
    tools = await client.get_tools()
    print("Available tools:")

    for tool in tools:
        print(tool.name)
