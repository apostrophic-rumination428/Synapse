"""Abstract embedding backend interface."""

from abc import ABC, abstractmethod
from typing import List


class EmbeddingBackend(ABC):
    """Abstract interface for embedding generation backends."""

    def __init__(self, model_name: str) -> None:
        """Initialize embedding backend."""
        self.model_name = model_name
        self.dimension = self._get_dimension()

    @abstractmethod
    def _get_dimension(self) -> int:
        """Get embedding dimension for the model."""
        pass

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        pass

    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        pass
