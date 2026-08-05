from utils.logger import logger


class MemoryDecision:

    """
    Decides whether existing memory is
    sufficient or if new research is needed.
    """

    def __init__(
        self,
        similarity_threshold: float = 0.80,
    ):

        self.similarity_threshold = (
            similarity_threshold
        )

    def should_research(

        self,

        memory_results,

    ) -> bool:

        """
        Returns True if new research is required.
        """

        if not memory_results:

            logger.info(
                "No memory found."
            )

            return True

        distances = memory_results.get(
            "distances",
            [],
        )

        if not distances:

            logger.info(
                "No similarity scores found."
            )

            return True

        if not distances[0]:

            logger.info(
                "Empty similarity results."
            )

            return True

        distance = distances[0][0]

        similarity = (
            1 - distance
        )

        logger.info(
            f"Memory similarity: {similarity:.3f}"
        )

        if similarity >= self.similarity_threshold:

            logger.success(
                "Relevant memory found."
            )

            return False

        logger.info(
            "Memory not sufficient."
        )

        return True