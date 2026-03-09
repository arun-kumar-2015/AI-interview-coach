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
import math
from collections import Counter

class EmbeddingService:
    """
    Zero-dependency Service for generating text vectors using manual TF-IDF.
    
    Replaces scikit-learn to avoid heavy builds and memory usage on Render.
    """
    
    def __init__(self, model_name: str = "manual-tfidf"):
        self.model_name = model_name
        self.vocabulary = {}
        self.idf = {}
        self.fitted = False
        print("✅ Zero-Dependency Embedding Service (Manual TF-IDF) initialized!")
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenizer: lowercase and split by non-alphanumeric."""
        import re
        text = text.lower()
        tokens = re.findall(r'\w+', text)
        return [t for t in tokens if len(t) > 2] # Skip very short words
    
    def embed_texts(self, texts: Union[str, List[str]], fit: bool = False) -> np.ndarray:
        """
        Convert text(s) to TF-IDF vectors using manual calculations.
        """
        if isinstance(texts, str):
            texts = [texts]
        
        tokenized_docs = [self._tokenize(doc) for doc in texts]
        
        if fit:
            # Build vocabulary from top 1000 terms
            all_words = []
            for doc in tokenized_docs:
                all_words.extend(doc)
            
            word_counts = Counter(all_words)
            # Take top 1000 most frequent words
            most_common = word_counts.most_common(1000)
            self.vocabulary = {word: i for i, (word, _) in enumerate(most_common)}
            
            # Calculate IDF
            num_docs = len(tokenized_docs)
            for word in self.vocabulary:
                containing_docs = sum(1 for doc in tokenized_docs if word in doc)
                self.idf[word] = math.log(num_docs / (1 + containing_docs))
            
            self.fitted = True
        
        # Vectorize
        dim = len(self.vocabulary) if self.vocabulary else 1000
        vectors = np.zeros((len(texts), dim))
        
        if not self.fitted:
            return vectors
            
        for i, tokens in enumerate(tokenized_docs):
            counts = Counter(tokens)
            doc_len = len(tokens) if tokens else 1
            for word, idx in self.vocabulary.items():
                if word in counts:
                    tf = counts[word] / doc_len
                    vectors[i, idx] = tf * self.idf[word]
        
        return vectors
    
    def get_embedding_dimension(self) -> int:
        return len(self.vocabulary) if self.vocabulary else 1000


# For backward compatibility
EmbeddingService = EmbeddingService
