from memory.instance import (
    memory_service,
)

from research.evidence import (
    Evidence,
)

from utils.logger import (
    logger,
)


class MemoryRetrievalService:

    def __init__(self):

        self.memory = (
            memory_service
        )

    def retrieve(

        self,

        query: str,

        top_k: int = 5,

        min_similarity: float = 0.45,

    ) -> list[Evidence]:

        logger.info(
            "Retrieving related memories..."
        )

        evidences = []

        try:

            results = self.memory.retrieve(

                query=query,

                top_k=top_k,

            )

            documents = results.get(
                "documents",
                []
            )

            metadatas = results.get(
                "metadatas",
                []
            )

            if (

                documents

                and len(documents) > 0

                and len(documents[0]) > 0

            ):

                logger.info(
                    f"Checking {len(documents[0])} candidate memories"
                )

                for document, metadata, distance in zip(

                    documents[0],

                    metadatas[0],

                    results.get(
                        "distances",
                        [[]],
                    )[0],

                ):

                    # Chroma's default metric is squared L2. With
                    # normalized embeddings: cosine = 1 - distance / 2
                    similarity = 1 - (
                        distance / 2
                    )

                    if similarity < min_similarity:

                        logger.info(
                            f"Skipping unrelated memory "
                            f"(similarity {similarity:.2f})"
                        )

                        continue

                    logger.info(
                        f"Using related memory "
                        f"(similarity {similarity:.2f})"
                    )

                    evidences.append(

                        Evidence(

                            source_url=metadata.get(

                                "source_url",

                                "memory",

                            ),

                            content=document,

                        )

                    )

            else:

                logger.info(
                    "No related memories found."
                )

        except Exception as e:

            logger.warning(
                f"Memory retrieval failed: {e}"
            )

        return evidences