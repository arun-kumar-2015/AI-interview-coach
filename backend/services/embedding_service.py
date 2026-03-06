"""
Embedding Service
=================
This service handles the creation of text embeddings using sentence-transformers.
Embeddings are used for semantic similarity search in the RAG pipeline.

RAG (Retrieval-Augmented Generation) Concept:
- We convert resume text into vector embeddings
- These embeddings capture semantic meaning, not just keywords
- FAISS stores these vectors for efficient similarity search
- When generating questions, we retrieve relevant resume sections first
- This ensures questions are based on actual resume content

Author: AI Interview Coach Team
"""

from typing import List, Union
import numpy as np
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedding service.
        
        Args:
            model_name: Name of the sentence-transformer model to use
                       'all-MiniLM-L6-v2' is a good balance of speed and quality
        """
        # Local import to prevent heavy loading during application startup
        print("📥 Importing sentence_transformers (this may take a minute)...")
        from sentence_transformers import SentenceTransformer
        
        self.model_name = model_name
        print(f"📥 Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        print("✅ Embedding model loaded successfully!")
    
    def embed_texts(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Convert text(s) to embeddings.
        
        Args:
            texts: Single text string or list of text strings
            
        Returns:
            Numpy array of embeddings with shape (n_texts, embedding_dim)
        """
        if isinstance(texts, str):
            texts = [texts]
        
        # Generate embeddings using the sentence-transformer model
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        
        return embeddings
    
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of the embeddings produced by this model.
        
        Returns:
            Embedding dimension (384 for all-MiniLM-L6-v2)
        """
        return self.model.get_sentence_embedding_dimension()


# For backward compatibility
EmbeddingService = EmbeddingService
