import os
from typing import Optional, Dict, Any

# Global services (will be initialized lazily)
_embedding_service: Optional[Any] = None
_vector_store: Optional[Any] = None
_llm_service: Optional[Any] = None

# Store resumes in memory (in production, use a database)
resumes_db: Dict[str, Dict[str, Any]] = {}

def get_embedding_service():
    global _embedding_service
    if _embedding_service is None:
        from services.embedding_service import EmbeddingService
        print("📥 Lazy LOADING Embedding Service...")
        _embedding_service = EmbeddingService()
    return _embedding_service

def get_vector_store():
    global _vector_store
    if _vector_store is None:
        from services.vector_store import VectorStore
        print("📥 Lazy LOADING Vector Store...")
        _vector_store = VectorStore(get_embedding_service())
    return _vector_store

def get_llm_service():
    global _llm_service
    if _llm_service is None:
        from services.llm_service import LLMService
        print("📥 Lazy LOADING LLM Service...")
        _llm_service = LLMService()
    return _llm_service
