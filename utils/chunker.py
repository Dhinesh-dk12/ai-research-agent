class TextChunker:
    """
    Splits large text into overlapping chunks
    for storage in ChromaDB.
    """

    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 100,
    ):

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(
        self,
        text: str,
    ) -> list[str]:

        words = text.split()

        if not words:
            return []

        chunks = []

        start = 0

        while start < len(words):

            end = start + self.chunk_size

            chunk = " ".join(
                words[start:end]
            )

            chunks.append(
                chunk
            )

            start += (
                self.chunk_size
                - self.overlap
            )

        return chunks