import os

from dotenv import load_dotenv

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()


class MCPClient:

    def __init__(self):

        self.server_params = StdioServerParameters(
            command="npx",
            args=[
                "-y",
                "tavily-mcp",
            ],
            env={
                "TAVILY_API_KEY": os.getenv("TAVILY_API_KEY"),
            },
        )

    async def call_tool(
        self,
        tool_name: str,
        arguments: dict,
    ):

        async with stdio_client(self.server_params) as (
            read_stream,
            write_stream,
        ):

            async with ClientSession(
                read_stream,
                write_stream,
            ) as session:

                await session.initialize()

                result = await session.call_tool(
                    tool_name,
                    arguments,
                )

                return result

    async def search(
        self,
        query: str,
        max_results: int = 5,
    ):

        return await self.call_tool(
            tool_name="tavily_search",
            arguments={
                "query": query,
                "max_results": max_results,
            },
        )