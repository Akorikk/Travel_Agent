import os 
import asyncio
import certifi
from dotenv import load_dotenv  
from langchain_mcp_adapters.client import MultiServerMCPClient

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUEST_CA_BUNDLE"] = certifi.where()


load_dotenv()


TAVILY_API_KEY = os.getenv("TAVILY_API_KEY") 


client = MultiServerMCPClient( 
    {
        "tavily-remote": {
        "transport": "streamable_http",
        "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_API_KEY}"
      
    },
}
    
)




async def get_all_tools():
    tools = await client.get_tools()
    print("Available tools:")

    for tool in tools:
        print(tool.name)






tavily_search_tool = None


async def get_tavily_search_tool():
    global tavily_search_tool

    # Reuse the tool if already retrieved
    if tavily_search_tool is not None:
        return tavily_search_tool

    # Retrieve available MCP tools
    tools = await client.get_tools()

    print("\nAvailable MCP Tools:")
    for tool in tools:
        print(tool.name)

    # Select the Tavily search tool
    tavily_search_tool = next(
        (tool for tool in tools if tool.name == "tavily_search"),
        None
    )

    if tavily_search_tool is None:
        raise ValueError(
            "tavily_search tool not found in MCP server"
        )

    return tavily_search_tool


async def tavily_mcp_search(query: str):
    search_tool = await get_tavily_search_tool()

    result = await search_tool.ainvoke(
        {"query": query}
    )

    return result

