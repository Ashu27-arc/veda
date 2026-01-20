"""
VEDA AI - Semantic Similarity Search
Uses embeddings for intelligent response matching
"""

import json
import os
import numpy as np
from typing import List, Dict, Tuple, Optional
from python_backend.logger import log_info, log_error, log_warning
from python_backend.ml_config import SIMILARITY_THRESHOLD, EMBEDDING_MODEL

# ========================================
# SEMANTIC SEARCH ENGINE
# ========================================

class SemanticSearchEngine:
    """
    Semantic search using sentence embeddings
    Finds similar responses based on meaning, not just keywords
    """
    
    def __init__(self):
        self.model = None
        self.knowledge_base: List[Dict] = []
        self.embeddings: Optional[np.ndarray] = None
        self.storage_path = "data/semantic_knowledge.json"
        self.embeddings_path = "data/semantic_embeddings.npy"
        
        self._load_model()
        self._load_knowledge_base()
    
    def _load_model(self):
        """Load sentence transformer model"""
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(EMBEDDING_MODEL)
            log_info(f"Semantic search model loaded: {EMBEDDING_MODEL}")
        except ImportError:
            log_warning("sentence-transformers not installed. Run: pip install sentence-transformers")
        except Exception as e:
            log_error(f"Failed to load semantic model: {e}")
    
    def _load_knowledge_base(self):
        """Load existing knowledge base"""
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    self.knowledge_base = json.load(f)
                log_info(f"Loaded {len(self.knowledge_base)} knowledge entries")
            
            if os.path.exists(self.embeddings_path):
                self.embeddings = np.load(self.embeddings_path)
                log_info(f"Loaded {len(self.embeddings)} embeddings")
                
        except Exception as e:
            log_error(f"Failed to load knowledge base: {e}")
    
    def add_knowledge(self, question: str, answer: str, category: str = "general"):
        """Add new knowledge to the base"""
        if not self.model:
            log_warning("Model not loaded, cannot add knowledge")
            return False
        
        try:
            # Create entry
            entry = {
                "question": question,
                "answer": answer,
                "category": category,
                "added_at": str(np.datetime64('now'))
            }
            
            # Generate embedding
            embedding = self.model.encode([question])[0]
            
            # Add to knowledge base
            self.knowledge_base.append(entry)
            
            # Update embeddings array
            if self.embeddings is None:
                self.embeddings = embedding.reshape(1, -1)
            else:
                self.embeddings = np.vstack([self.embeddings, embedding])
            
            # Save
            self._save_knowledge_base()
            log_info(f"Added knowledge: {question[:50]}...")
            return True
            
        except Exception as e:
            log_error(f"Failed to add knowledge: {e}")
            return False
    
    def search(
        self,
        query: str,
        top_k: int = 3,
        threshold: float = SIMILARITY_THRESHOLD
    ) -> List[Dict]:
        """
        Search for similar entries
        
        Returns:
            List of {question, answer, similarity} dicts
        """
        if not self.model or self.embeddings is None or len(self.knowledge_base) == 0:
            return []
        
        try:
            # Encode query
            query_embedding = self.model.encode([query])[0]
            
            # Calculate cosine similarity
            similarities = self._cosine_similarity(query_embedding, self.embeddings)
            
            # Get top-k indices
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            results = []
            for idx in top_indices:
                sim = similarities[idx]
                if sim >= threshold:
                    entry = self.knowledge_base[idx].copy()
                    entry["similarity"] = float(sim)
                    results.append(entry)
            
            if results:
                log_info(f"Found {len(results)} similar entries (best: {results[0]['similarity']:.2f})")
            
            return results
            
        except Exception as e:
            log_error(f"Search error: {e}")
            return []
    
    def get_best_response(
        self,
        query: str,
        threshold: float = SIMILARITY_THRESHOLD
    ) -> Optional[str]:
        """Get the best matching response for a query"""
        results = self.search(query, top_k=1, threshold=threshold)
        
        if results:
            return results[0]["answer"]
        return None
    
    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """Calculate cosine similarity between vector and matrix"""
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b, axis=1)
        
        # Avoid division by zero
        norm_b = np.where(norm_b == 0, 1, norm_b)
        
        return np.dot(b, a) / (norm_b * norm_a)
    
    def _save_knowledge_base(self):
        """Save knowledge base to files"""
        try:
            os.makedirs("data", exist_ok=True)
            
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_base, f, indent=2, ensure_ascii=False)
            
            if self.embeddings is not None:
                np.save(self.embeddings_path, self.embeddings)
                
        except Exception as e:
            log_error(f"Failed to save knowledge base: {e}")
    
    def rebuild_embeddings(self):
        """Rebuild all embeddings (use after model change)"""
        if not self.model or not self.knowledge_base:
            return False
        
        try:
            questions = [entry["question"] for entry in self.knowledge_base]
            self.embeddings = self.model.encode(questions)
            self._save_knowledge_base()
            log_info(f"Rebuilt {len(self.embeddings)} embeddings")
            return True
        except Exception as e:
            log_error(f"Failed to rebuild embeddings: {e}")
            return False
    
    def get_stats(self) -> Dict:
        """Get knowledge base statistics"""
        return {
            "total_entries": len(self.knowledge_base),
            "model_loaded": self.model is not None,
            "embeddings_loaded": self.embeddings is not None,
            "model_name": EMBEDDING_MODEL
        }


# ========================================
# ENHANCED SELF-LEARNING WITH SEMANTICS
# ========================================

class SemanticSelfLearning:
    """
    Enhanced self-learning that uses semantic similarity
    instead of exact string matching
    """
    
    def __init__(self):
        self.search_engine = SemanticSearchEngine()
    
    def learn(self, question: str, answer: str, category: str = "learned"):
        """Learn from a new Q&A pair"""
        return self.search_engine.add_knowledge(question, answer, category)
    
    def get_response(self, query: str) -> Optional[str]:
        """Get learned response using semantic similarity"""
        return self.search_engine.get_best_response(query)
    
    def find_similar(self, query: str, top_k: int = 3) -> List[Dict]:
        """Find similar questions and their answers"""
        return self.search_engine.search(query, top_k)
    
    def get_stats(self) -> Dict:
        """Get learning statistics"""
        return self.search_engine.get_stats()


# ========================================
# GLOBAL INSTANCES
# ========================================

_search_engine = None
_self_learning = None

def get_semantic_search() -> SemanticSearchEngine:
    """Get or create global semantic search instance"""
    global _search_engine
    if _search_engine is None:
        _search_engine = SemanticSearchEngine()
    return _search_engine


def get_semantic_learning() -> SemanticSelfLearning:
    """Get or create global semantic learning instance"""
    global _self_learning
    if _self_learning is None:
        _self_learning = SemanticSelfLearning()
    return _self_learning


def semantic_search(query: str, top_k: int = 3) -> List[Dict]:
    """Convenience function for semantic search"""
    return get_semantic_search().search(query, top_k)


def get_semantic_response(query: str) -> Optional[str]:
    """Convenience function to get semantic response"""
    return get_semantic_learning().get_response(query)


def learn_response(question: str, answer: str):
    """Convenience function to learn a response"""
    return get_semantic_learning().learn(question, answer)
