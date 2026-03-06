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
    Pure Numpy vector store for semantic similarity search.
    
    Uses cosine similarity for retrieval without needing heavy FAISS.
    """
    
    def __init__(self, embedding_service):
        """
        Initialize the vector store.
        """
        self.embedding_service = embedding_service
        # Dictionary to store multiple indexes (one per resume/session)
        # Key: session_id, Value: dict with 'vectors' and 'texts'
        self.indexes: Dict[str, Dict[str, Any]] = {}
        
        print(f"📦 Lightweight Vector store initialized!")
    
    def create_index(self, session_id: str) -> None:
        """
        Create a new entry for a session.
        """
        self.indexes[session_id] = {
            'vectors': None,
            'texts': [],
            'metadatas': []
        }
        print(f"✅ Created new storage for session: {session_id}")
    
    def add_texts(
        self, 
        session_id: str, 
        texts: List[str],
        metadatas: Optional[List[Dict]] = None
    ) -> None:
        """
        Add texts and generate TF-IDF embeddings.
        """
        if session_id not in self.indexes:
            self.create_index(session_id)
        
        # Generate and store embeddings (with fit=True for initial resume processing)
        embeddings = self.embedding_service.embed_texts(texts, fit=True)
        
        # Normalize for easier cosine similarity later
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1, norms)
        normalized_embeddings = embeddings / norms
        
        self.indexes[session_id]['vectors'] = normalized_embeddings
        self.indexes[session_id]['texts'].extend(texts)
        
        if metadatas:
            self.indexes[session_id]['metadatas'].extend(metadatas)
        else:
            self.indexes[session_id]['metadatas'].extend([{}] * len(texts))
        
        print(f"📝 Added {len(texts)} texts to lightweight store for session: {session_id}")
    
    def search(
        self, 
        session_id: str, 
        query: str, 
        k: int = 5
    ) -> List[Tuple[str, float]]:
        """
        Search for similar texts using manual cosine similarity.
        """
        if session_id not in self.indexes or self.indexes[session_id]['vectors'] is None:
            return []
        
        # Generate query embedding
        query_embedding = self.embedding_service.embed_texts([query])
        
        # Normalize query
        norm = np.linalg.norm(query_embedding)
        normalized_query = query_embedding / (norm if norm > 0 else 1)
        
        # Calculate cosine similarity: dot product since both are normalized
        stored_vectors = self.indexes[session_id]['vectors']
        similarities = np.dot(stored_vectors, normalized_query.T).flatten()
        
        # Get top K indices
        top_k_indices = np.argsort(similarities)[::-1][:k]
        
        # Get texts and scores
        texts = self.indexes[session_id]['texts']
        results = []
        
        for idx in top_k_indices:
            results.append((texts[idx], float(similarities[idx])))
        
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
        Get statistics about a session storage.
        """
        if session_id not in self.indexes:
            return {"error": "Index not found"}
        
        stored_vectors = self.indexes[session_id]['vectors']
        
        return {
            "session_id": session_id,
            "num_vectors": len(stored_vectors) if stored_vectors is not None else 0,
            "num_texts": len(self.indexes[session_id]['texts'])
        }
