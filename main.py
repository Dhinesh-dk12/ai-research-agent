import asyncio
import sys

from graph.workflow import (
    graph,
)

from graph.state import (
    ResearchState,
)


async def main():

    initial_state: ResearchState = {

        # -----------------------------
        # User Input
        # -----------------------------

        "query":
        "give me factually correct and accurate research report about NASA's Voyager Spacecraft.",

        # -----------------------------
        # Planner
        # -----------------------------

        "research_plan": None,

        # -----------------------------
        # Executor
        # -----------------------------

        "completed_tasks": [],

        "task_results": {},

        "metadata": {},

        # -----------------------------
        # Extraction
        # -----------------------------

        "urls": [],

        "fresh_evidences": [],

        # -----------------------------
        # Memory
        # -----------------------------

        "evidences": [],

        # -----------------------------
        # Reasoning
        # -----------------------------

        "reasoning_output": "",

        # -----------------------------
        # Report
        # -----------------------------

        "report": "",

        # -----------------------------
        # PDF
        # -----------------------------

        "pdf_path": "",

    }

    final_state = await graph.ainvoke(
        initial_state
    )

    print(
        "\n\nFINAL REPORT\n"
    )

    print(
        final_state[
            "report"
        ]
    )

    print(
        "\nPDF Saved To:\n"
    )

    print(
        final_state[
            "pdf_path"
        ]
    )


if __name__ == "__main__":

    def _is_known_proactor_shutdown_noise(
        exc_type,
        exc_value,
        exc_traceback,
    ) -> bool:
        """
        On Windows, asyncio's ProactorEventLoop can leave an SSL
        connection's finalizer (__del__) running after the event
        loop and its proactor are already closed and gone. That
        produces a "RuntimeError: Event loop is closed" or an
        "AttributeError: 'NoneType' object has no attribute 'send'"
        raised from inside Python's own asyncio module — not from
        this project's code — after the program's real work is
        already finished. Nothing is lost when this happens.

        Only these two specific, recognized error types are
        treated as safe to hide, and only when they originate from
        asyncio's own sslproto.py / proactor_events.py. Anything
        else is still reported normally, so a real bug is never
        silently swallowed.
        """

        if exc_type is RuntimeError and str(
            exc_value
        ) == "Event loop is closed":

            frame_matches = True

        elif (
            exc_type is AttributeError

            and "NoneType" in str(exc_value)

            and "send" in str(exc_value)
        ):

            frame_matches = True

        else:

            return False

        tb = exc_traceback

        while tb is not None:

            filename = (
                tb.tb_frame.f_code.co_filename
            )

            if "asyncio" in filename and (
                "sslproto.py" in filename
                or "proactor_events.py" in filename
            ):

                return frame_matches

            tb = tb.tb_next

        return False

    def _silence_proactor_shutdown_noise(
        unraisable,
    ):
        """
        Hook for exceptions raised inside __del__ / garbage
        collection (Python calls this instead of printing
        "Exception ignored in: ..." directly). This is where the
        leftover SSL transport cleanup actually surfaces.
        """

        if _is_known_proactor_shutdown_noise(
            unraisable.exc_type,
            unraisable.exc_value,
            unraisable.exc_traceback,
        ):

            return

        sys.__unraisablehook__(
            unraisable
        )

    sys.unraisablehook = (
        _silence_proactor_shutdown_noise
    )

    def _silence_closed_loop_error(loop, context):

        exc = context.get(
            "exception"
        )

        # Same known-harmless case, but for when it surfaces as a
        # regular event-loop callback error instead of a __del__
        # finalizer error.
        if (
            isinstance(
                exc,
                RuntimeError,
            )

            and str(exc) == "Event loop is closed"
        ):

            return

        loop.default_exception_handler(
            context
        )

    async def run():

        loop = (
            asyncio.get_running_loop()
        )

        loop.set_exception_handler(
            _silence_closed_loop_error
        )

        await main()

        # Give background SSL/HTTP connections more time to
        # finish closing before the event loop shuts down. This
        # reduces how often the __del__ finalizer above even has
        # to run.
        await asyncio.sleep(
            1.0
        )

    asyncio.run(
        run()
    )