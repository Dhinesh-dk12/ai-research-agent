from planner.schemas import ResearchTask

from mcp_client.client import MCPClient


class TaskDispatcher:

    def __init__(self):

        self.client = MCPClient()

    async def dispatch(
        self,
        task: ResearchTask,
    ):

        return await self.client.call_tool(

            tool_name=task.tool_name,

            arguments=task.tool_arguments,

        )