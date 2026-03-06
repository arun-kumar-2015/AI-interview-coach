import os
from typing import Optional, Dict, Any
from services.embedding_service import EmbeddingService
from services.vector_store import VectorStore
from services.llm_service import LLMService

# Global services (will be initialized lazily)
_embedding_service: Optional[EmbeddingService] = None
_vector_store: Optional[VectorStore] = None
_llm_service: Optional[LLMService] = None

# Store resumes in memory (in production, use a database)
resumes_db: Dict[str, Dict[str, Any]] = {}

def get_embedding_service() -> EmbeddingService:
    global _embedding_service
    if _embedding_service is None:
        print("📥 Lazy LOADING Embedding Service...")
        _embedding_service = EmbeddingService()
    return _embedding_service

def get_vector_store() -> VectorStore:
    global _vector_store
    if _vector_store is None:
        print("📥 Lazy LOADING Vector Store...")
        _vector_store = VectorStore(get_embedding_service())
    return _vector_store

def get_llm_service() -> LLMService:
    global _llm_service
    if _llm_service is None:
        print("📥 Lazy LOADING LLM Service...")
        _llm_service = LLMService()
    return _llm_service
