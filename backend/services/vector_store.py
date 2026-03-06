"""
Vector Store Service
====================
This service manages FAISS (Facebook AI Similarity Search) vector database
for storing and retrieving resume embeddings.

FAISS is a library for efficient similarity search and clustering of 
dense vectors. It contains algorithms that search in sets of vectors 
of any size, up to ones that possibly do not fit in RAM.

Key Concepts:
- Index: Data structure for efficient similarity search
- Embeddings: Dense vector representations of text
- Cosine Similarity: Measures semantic similarity between vectors

Author: AI Interview Coach Team
"""

from typing import List, Tuple, Optional, Dict, Any
import numpy as np
import numpy as np
import pickle
from pathlib import Path


class VectorStore:
    """
    FAISS-based vector store for semantic similarity search.
    
    Manages multiple resume indexes, each identified by a unique session ID.
    Supports adding text with embeddings and searching for similar text.
    """
    
    def __init__(self, embedding_service):
        """
        Initialize the vector store.
        
        Args:
            embedding_service: Service for generating text embeddings
        """
        # Local import to prevent heavy loading during application startup
        print("📥 Importing faiss...")
        import faiss
        self.faiss = faiss
        
        self.embedding_service = embedding_service
        self.dimension = embedding_service.get_embedding_dimension()
        
        # Dictionary to store multiple indexes (one per resume/session)
        # Key: session_id, Value: dict with 'index' and 'texts'
        self.indexes: Dict[str, Dict[str, Any]] = {}
        
        print(f"📦 Vector store initialized with dimension: {self.dimension}")
    
    def create_index(self, session_id: str) -> None:
        """
        Create a new FAISS index for a session.
        
        Args:
            session_id: Unique identifier for the resume/session
        """
        # Use IndexFlatIP for inner product (cosine similarity with normalized vectors)
        # For cosine similarity, we use Inner Product with L2 normalized vectors
        index = self.faiss.IndexFlatIP(self.dimension)
        
        self.indexes[session_id] = {
            'index': index,
            'texts': [],  # Store original texts for retrieval
            'metadatas': []  # Store metadata if needed
        }
        
        print(f"✅ Created new index for session: {session_id}")
    
    def add_texts(
        self, 
        session_id: str, 
        texts: List[str],
        metadatas: Optional[List[Dict]] = None
    ) -> None:
        """
        Add texts to the vector store.
        
        This method:
        1. Generates embeddings for the texts
        2. Normalizes embeddings for cosine similarity
        3. Adds to the FAISS index
        
        Args:
            session_id: Session identifier
            texts: List of text strings to add
            metadatas: Optional metadata for each text
        """
        if session_id not in self.indexes:
            self.create_index(session_id)
        
        # Generate embeddings
        embeddings = self.embedding_service.embed_texts(texts)
        
        # Normalize embeddings for cosine similarity
        # This converts inner product to cosine similarity
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1, norms)  # Avoid division by zero
        normalized_embeddings = embeddings / norms
        
        # Add to FAISS index
        index = self.indexes[session_id]['index']
        index.add(normalized_embeddings.astype('float32'))
        
        # Store original texts
        self.indexes[session_id]['texts'].extend(texts)
        
        # Store metadata if provided
        if metadatas:
            self.indexes[session_id]['metadatas'].extend(metadatas)
        else:
            self.indexes[session_id]['metadatas'].extend([{}] * len(texts))
        
        print(f"📝 Added {len(texts)} texts to index for session: {session_id}")
    
    def search(
        self, 
        session_id: str, 
        query: str, 
        k: int = 5
    ) -> List[Tuple[str, float]]:
        """
        Search for similar texts in the vector store.
        
        Uses cosine similarity (via normalized inner product) to find
        the most semantically similar texts to the query.
        
        Args:
            session_id: Session identifier
            query: Query text
            k: Number of results to return (default: 5)
            
        Returns:
            List of tuples (text, similarity_score) sorted by relevance
        """
        if session_id not in self.indexes:
            return []
        
        # Generate query embedding
        query_embedding = self.embedding_service.embed_texts([query])
        
        # Normalize query embedding
        norms = np.linalg.norm(query_embedding, axis=1, keepdims=True)
        normalized_query = query_embedding / norms
        
        # Search the index
        index = self.indexes[session_id]['index']
        scores, indices = index.search(normalized_query.astype('float32'), k)
        
        # Get texts and scores
        texts = self.indexes[session_id]['texts']
        results = []
        
        for idx, score in zip(indices[0], scores[0]):
            if idx >= 0 and idx < len(texts):
                results.append((texts[idx], float(score)))
        
        return results
    
    def get_relevant_context(
        self, 
        session_id: str, 
        topic: str, 
        max_length: int = 2000
    ) -> str:
        """
        Get relevant context from resume for a specific topic.
        
        This is used in the RAG pipeline to retrieve relevant resume
        sections before generating questions.
        
        Args:
            session_id: Session identifier
            topic: Topic or skill to search for
            max_length: Maximum length of combined context
            
        Returns:
            Combined relevant text from the resume
        """
        results = self.search(session_id, topic, k=10)
        
        context_parts = []
        current_length = 0
        
        for text, score in results:
            if current_length + len(text) > max_length:
                break
            context_parts.append(text)
            current_length += len(text)
        
        return "\n\n".join(context_parts)
    
    def delete_index(self, session_id: str) -> None:
        """
        Delete an index and its associated data.
        
        Args:
            session_id: Session identifier to delete
        """
        if session_id in self.indexes:
            del self.indexes[session_id]
            print(f"🗑️ Deleted index for session: {session_id}")
    
    def get_index_stats(self, session_id: str) -> Dict[str, Any]:
        """
        Get statistics about an index.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Dictionary with index statistics
        """
        if session_id not in self.indexes:
            return {"error": "Index not found"}
        
        index = self.indexes[session_id]['index']
        
        return {
            "session_id": session_id,
            "num_vectors": index.ntotal,
            "dimension": self.dimension,
            "num_texts": len(self.indexes[session_id]['texts'])
        }
