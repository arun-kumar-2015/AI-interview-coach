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
class EmbeddingService:
    """
    Lightweight Service for generating text embeddings using TF-IDF.
    
    This replaces sentence-transformers to stay within Render's 512MB RAM limit.
    """
    
    def __init__(self, model_name: str = "tfidf-light"):
        """
        Initialize the lightweight embedding service.
        """
        # Local import to prevent loading during app startup
        from sklearn.feature_extraction.text import TfidfVectorizer
        
        self.model_name = model_name
        # Simple TF-IDF vectorizer - very low memory
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=1000,
            ngram_range=(1, 2)
        )
        self.fitted = False
        print("✅ Lightweight Embedding Service (TF-IDF) initialized!")
    
    def embed_texts(self, texts: Union[str, List[str]], fit: bool = False) -> np.ndarray:
        """
        Convert text(s) to TF-IDF vectors.
        """
        if isinstance(texts, str):
            texts = [texts]
        
        if fit:
            # First time (during upload), we fit the vectorizer to the resume content
            embeddings = self.vectorizer.fit_transform(texts).toarray()
            self.fitted = True
        elif not self.fitted:
            # Fallback if search happens before fit
            return np.zeros((len(texts), 1000))
        else:
            # Subsequent searches
            embeddings = self.vectorizer.transform(texts).toarray()
        
        return embeddings
    
    def get_embedding_dimension(self) -> int:
        return 1000  # Fixed based on max_features


# For backward compatibility
EmbeddingService = EmbeddingService
