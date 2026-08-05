from planner.schemas import (
    ResearchPlan,
)

from executor.dispatcher import (
    TaskDispatcher,
)

from utils.logger import (
    logger,
)


class ExecutorService:

    def __init__(self):

        self.dispatcher = (
            TaskDispatcher()
        )

    async def execute(

        self,

        research_plan: ResearchPlan,

    ):

        logger.info(
            "Starting task execution"
        )

        completed_tasks = []

        task_results = {}

        for task in research_plan.tasks:

            logger.info(
                f"Executing Task {task.task_id}: {task.title}"
            )

            try:

                result = await self.dispatcher.dispatch(
                    task
                )

                completed_tasks.append(
                    task.task_id
                )

                task_results[
                    task.task_id
                ] = result

                logger.success(
                    f"Task {task.task_id} completed successfully"
                )

            except Exception as e:

                logger.exception(
                    f"Task {task.task_id} failed: {e}"
                )

        logger.success(
            "Executor finished all tasks"
        )

        return (

            completed_tasks,

            task_results,

        )