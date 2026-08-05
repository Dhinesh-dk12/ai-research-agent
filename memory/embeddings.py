from sentence_transformers import SentenceTransformer

from utils.logger import logger


class EmbeddingService:
    """
    Generates vector embeddings for text.
    """

    def __init__(self):

        logger.info(
            "Loading embedding model..."
        )

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        logger.success(
            "Embedding model loaded."
        )

    def embed_text(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding for a single text.
        """

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_documents(
        self,
        documents: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple documents.
        """

        embeddings = self.model.encode(
            documents,
            normalize_embeddings=True,
        )

        return embeddings.tolist()