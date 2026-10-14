import asyncio
import os

from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

load_dotenv()

MCP_URL = os.getenv("MCP_URL", "http://localhost:8001/mcp")

async def main():
    async with streamable_http_client(MCP_URL) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.list_tools()
            print("Tools:", [tool.name for tool in result.tools])

if __name__ == "__main__":
    asyncio.run(main())