import asyncio

from mcp_client.client import MCPClient


async def main():

    client = MCPClient()

    result = await client.search(
        query="Latest AI Agent frameworks",
        max_results=3,
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())