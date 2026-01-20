"""
VEDA AI - Intent Classification System
Classifies user commands into categories for better understanding
"""

import re
from typing import Dict, List, Tuple, Optional
from python_backend.logger import log_info, log_error
from python_backend.ml_config import INTENT_CATEGORIES

# ========================================
# KEYWORD-BASED INTENT CLASSIFIER
# ========================================

class KeywordIntentClassifier:
    """Fast keyword-based intent classification"""
    
    def __init__(self):
        self.categories = INTENT_CATEGORIES
        self._build_pattern_cache()
    
    def _build_pattern_cache(self):
        """Pre-compile regex patterns for faster matching"""
        self.patterns = {}
        for intent, keywords in self.categories.items():
            # Create pattern that matches any keyword
            pattern = r'\b(' + '|'.join(re.escape(k) for k in keywords) + r')\b'
            self.patterns[intent] = re.compile(pattern, re.IGNORECASE)
    
    def classify(self, text: str) -> Tuple[str, float]:
        """
        Classify text into intent category
        
        Returns:
            Tuple of (intent_name, confidence_score)
        """
        text_lower = text.lower()
        scores = {}
        
        for intent, pattern in self.patterns.items():
            matches = pattern.findall(text_lower)
            if matches:
                # Score based on number of keyword matches and their position
                score = len(matches) / len(text_lower.split())
                scores[intent] = min(score * 2, 1.0)  # Normalize to 0-1
        
        if not scores:
            return ("unknown", 0.0)
        
        # Return highest scoring intent
        best_intent = max(scores.items(), key=lambda x: x[1])
        log_info(f"Intent classified: {best_intent[0]} (confidence: {best_intent[1]:.2f})")
        return best_intent
    
    def get_all_intents(self, text: str) -> Dict[str, float]:
        """Get all matching intents with scores"""
        text_lower = text.lower()
        scores = {}
        
        for intent, pattern in self.patterns.items():
            matches = pattern.findall(text_lower)
            if matches:
                score = len(matches) / len(text_lower.split())
                scores[intent] = min(score * 2, 1.0)
        
        return dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))


# ========================================
# ML-BASED INTENT CLASSIFIER (Optional)
# ========================================

class MLIntentClassifier:
    """Machine Learning based intent classification using sentence transformers"""
    
    def __init__(self):
        self.model = None
        self.intent_embeddings = {}
        self._load_model()
    
    def _load_model(self):
        """Load sentence transformer model"""
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            log_info("ML Intent Classifier loaded")
            self._compute_intent_embeddings()
        except ImportError:
            log_info("sentence-transformers not installed, using keyword classifier only")
        except Exception as e:
            log_error(f"Failed to load ML classifier: {e}")
    
    def _compute_intent_embeddings(self):
        """Pre-compute embeddings for intent keywords"""
        if not self.model:
            return
        
        # Sample sentences for each intent
        intent_samples = {
            "system_control": [
                "open chrome browser",
                "close notepad application",
                "start the calculator",
                "chrome kholo",
                "notepad band karo"
            ],
            "volume_control": [
                "increase the volume",
                "turn down the sound",
                "mute the audio",
                "volume badha do",
                "awaaz kam karo"
            ],
            "weather": [
                "what's the weather today",
                "is it going to rain",
                "temperature in Delhi",
                "aaj mausam kaisa hai",
                "Delhi ka weather batao"
            ],
            "time_date": [
                "what time is it",
                "what's today's date",
                "kitne baje hain",
                "aaj kya date hai"
            ],
            "greeting": [
                "hello how are you",
                "good morning",
                "namaste VEDA",
                "hi there"
            ],
            "question": [
                "what is artificial intelligence",
                "how does this work",
                "why is the sky blue",
                "kya hai ye"
            ],
            "search": [
                "search for python tutorials",
                "google machine learning",
                "find restaurants nearby",
                "youtube pe search karo"
            ],
            "media_control": [
                "play some music",
                "pause the video",
                "next song please",
                "gaana chalao"
            ]
        }
        
        for intent, samples in intent_samples.items():
            embeddings = self.model.encode(samples)
            # Store mean embedding for each intent
            self.intent_embeddings[intent] = embeddings.mean(axis=0)
    
    def classify(self, text: str) -> Tuple[str, float]:
        """Classify text using ML embeddings"""
        if not self.model or not self.intent_embeddings:
            return ("unknown", 0.0)
        
        try:
            import numpy as np
            from numpy.linalg import norm
            
            # Get embedding for input text
            text_embedding = self.model.encode([text])[0]
            
            # Calculate cosine similarity with each intent
            scores = {}
            for intent, intent_emb in self.intent_embeddings.items():
                similarity = np.dot(text_embedding, intent_emb) / (norm(text_embedding) * norm(intent_emb))
                scores[intent] = float(similarity)
            
            if not scores:
                return ("unknown", 0.0)
            
            best_intent = max(scores.items(), key=lambda x: x[1])
            log_info(f"ML Intent: {best_intent[0]} (similarity: {best_intent[1]:.2f})")
            return best_intent
            
        except Exception as e:
            log_error(f"ML classification error: {e}")
            return ("unknown", 0.0)


# ========================================
# HYBRID INTENT CLASSIFIER
# ========================================

class HybridIntentClassifier:
    """
    Combines keyword and ML-based classification
    Uses keyword for speed, ML for accuracy
    """
    
    def __init__(self):
        self.keyword_classifier = KeywordIntentClassifier()
        self.ml_classifier = MLIntentClassifier()
        self.use_ml = self.ml_classifier.model is not None
    
    def classify(self, text: str) -> Dict:
        """
        Classify intent using hybrid approach
        
        Returns:
            {
                "intent": str,
                "confidence": float,
                "method": str,
                "all_intents": Dict[str, float]
            }
        """
        # Always get keyword classification (fast)
        keyword_intent, keyword_conf = self.keyword_classifier.classify(text)
        all_intents = self.keyword_classifier.get_all_intents(text)
        
        result = {
            "intent": keyword_intent,
            "confidence": keyword_conf,
            "method": "keyword",
            "all_intents": all_intents
        }
        
        # Use ML if keyword confidence is low and ML is available
        if self.use_ml and keyword_conf < 0.5:
            ml_intent, ml_conf = self.ml_classifier.classify(text)
            
            # Use ML result if it's more confident
            if ml_conf > keyword_conf:
                result["intent"] = ml_intent
                result["confidence"] = ml_conf
                result["method"] = "ml"
        
        return result
    
    def get_intent(self, text: str) -> str:
        """Simple interface to get just the intent name"""
        return self.classify(text)["intent"]


# ========================================
# GLOBAL CLASSIFIER INSTANCE
# ========================================

_classifier = None

def get_intent_classifier() -> HybridIntentClassifier:
    """Get or create global intent classifier instance"""
    global _classifier
    if _classifier is None:
        _classifier = HybridIntentClassifier()
    return _classifier


def classify_intent(text: str) -> Dict:
    """Convenience function to classify intent"""
    return get_intent_classifier().classify(text)


def get_intent(text: str) -> str:
    """Convenience function to get intent name"""
    return get_intent_classifier().get_intent(text)
