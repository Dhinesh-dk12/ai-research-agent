from memory.embeddings import EmbeddingService

from memory.chroma_store import ChromaStore

from utils.logger import logger


class MemoryRetriever:

    def __init__(

        self,

        embedding_service,

        store,

    ):

        self.embedding_service = (
            embedding_service
        )

        self.store = store

    def retrieve(

        self,

        query,

        top_k=5,

    ):

        logger.info(
            "Searching memory..."
        )

        embedding = (
            self.embedding_service.embed_text(
                query
            )
        )

        results = self.store.search(

            embedding,

            top_k,

        )

        logger.success(
            "Memory retrieval completed."
        )

        return results