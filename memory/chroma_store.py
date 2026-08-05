import chromadb

from utils.logger import logger


class ChromaStore:

    def __init__(self):

        logger.info(
            "Initializing ChromaDB..."
        )

        self.client = chromadb.PersistentClient(
            path="./chroma_db"
        )

        self.collection = (
            self.client.get_or_create_collection(
                name="research_memory"
            )
        )

        logger.success(
            "ChromaDB initialized."
        )

    def add_memory(
        self,
        memory,
        embedding,
    ):

        self.collection.add(

            ids=[
                memory.id
            ],

            documents=[
                memory.content
            ],

            embeddings=[
                embedding
            ],

            metadatas=[
                {
                    "query": memory.query,
                    "source_url": memory.source_url,
                    "source_type": memory.source_type,
                    "credibility_score": memory.credibility_score,
                    "created_at": str(
                        memory.created_at
                    ),
                    **memory.metadata,
                }
            ],
        )

    def exists(
        self,
        memory_hash: str,
    ) -> bool:

        results = self.collection.get(
            where={
                "memory_hash": memory_hash
            }
        )

        return len(
            results["ids"]
        ) > 0

    def search(
        self,
        embedding,
        top_k=5,
    ):

        return self.collection.query(

            query_embeddings=[
                embedding
            ],

            n_results=top_k,

            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

    def count(self):

        return self.collection.count()

    def clear(self):

        self.collection.delete(
            where={}
        )