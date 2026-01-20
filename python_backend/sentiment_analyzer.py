"""
VEDA AI - Sentiment Analysis
Detects user mood and emotional state for empathetic responses
"""

import re
from typing import Dict, Tuple, Optional
from python_backend.logger import log_info, log_error

# ========================================
# SENTIMENT CATEGORIES
# ========================================

SENTIMENT_POSITIVE = "positive"
SENTIMENT_NEGATIVE = "negative"
SENTIMENT_NEUTRAL = "neutral"
SENTIMENT_FRUSTRATED = "frustrated"
SENTIMENT_HAPPY = "happy"
SENTIMENT_SAD = "sad"
SENTIMENT_ANGRY = "angry"
SENTIMENT_CONFUSED = "confused"

# ========================================
# KEYWORD-BASED SENTIMENT ANALYZER
# ========================================

class KeywordSentimentAnalyzer:
    """Fast keyword-based sentiment analysis"""
    
    def __init__(self):
        # Positive indicators (English + Hindi/Hinglish)
        self.positive_words = {
            "english": [
                "good", "great", "awesome", "excellent", "amazing", "wonderful",
                "love", "like", "happy", "thanks", "thank", "perfect", "nice",
                "fantastic", "brilliant", "superb", "best", "beautiful", "yes",
                "correct", "right", "helpful", "useful", "appreciate"
            ],
            "hindi": [
                "achha", "accha", "badhiya", "shandar", "zabardast", "mast",
                "pyaar", "khush", "shukriya", "dhanyavaad", "theek", "sahi",
                "bahut achha", "bohot", "bohut", "bilkul", "haan", "ji"
            ]
        }
        
        # Negative indicators
        self.negative_words = {
            "english": [
                "bad", "terrible", "awful", "horrible", "hate", "dislike",
                "wrong", "error", "failed", "fail", "broken", "useless",
                "stupid", "dumb", "worst", "poor", "no", "not", "never",
                "can't", "cannot", "doesn't", "didn't", "won't", "problem"
            ],
            "hindi": [
                "bura", "kharab", "galat", "bekaar", "bekar", "ghatiya",
                "nafrat", "nahi", "nahin", "mat", "naa", "problem",
                "mushkil", "pareshani", "dikkat", "kyu nahi", "kyun nahi"
            ]
        }
        
        # Frustrated indicators
        self.frustrated_words = {
            "english": [
                "frustrated", "annoying", "annoyed", "irritating", "irritated",
                "ugh", "argh", "come on", "seriously", "again", "still",
                "why won't", "why doesn't", "not working", "doesn't work"
            ],
            "hindi": [
                "pareshan", "frustrated", "tang", "thak gaya", "thak gayi",
                "kyu", "kyun", "phir se", "fir se", "abhi bhi", "abhi tak"
            ]
        }
        
        # Confused indicators
        self.confused_words = {
            "english": [
                "confused", "confusing", "don't understand", "what", "how",
                "why", "unclear", "lost", "help", "explain", "meaning"
            ],
            "hindi": [
                "samajh nahi", "samajh nhi", "kya", "kaise", "kyun", "kyu",
                "matlab", "confused", "clear nahi", "pata nahi"
            ]
        }
        
        # Compile all words into sets for faster lookup
        self.all_positive = set(self.positive_words["english"] + self.positive_words["hindi"])
        self.all_negative = set(self.negative_words["english"] + self.negative_words["hindi"])
        self.all_frustrated = set(self.frustrated_words["english"] + self.frustrated_words["hindi"])
        self.all_confused = set(self.confused_words["english"] + self.confused_words["hindi"])
    
    def analyze(self, text: str) -> Dict:
        """
        Analyze sentiment of text
        
        Returns:
            {
                "sentiment": str,
                "confidence": float,
                "scores": {positive, negative, frustrated, confused},
                "emoji_suggestion": str
            }
        """
        text_lower = text.lower()
        words = set(re.findall(r'\b\w+\b', text_lower))
        
        # Count matches
        positive_count = len(words & self.all_positive)
        negative_count = len(words & self.all_negative)
        frustrated_count = len(words & self.all_frustrated)
        confused_count = len(words & self.all_confused)
        
        total = positive_count + negative_count + frustrated_count + confused_count
        
        if total == 0:
            return {
                "sentiment": SENTIMENT_NEUTRAL,
                "confidence": 0.5,
                "scores": {"positive": 0, "negative": 0, "frustrated": 0, "confused": 0},
                "emoji_suggestion": ""
            }
        
        scores = {
            "positive": positive_count / total,
            "negative": negative_count / total,
            "frustrated": frustrated_count / total,
            "confused": confused_count / total
        }
        
        # Determine primary sentiment
        if frustrated_count > 0 and frustrated_count >= negative_count:
            sentiment = SENTIMENT_FRUSTRATED
            confidence = scores["frustrated"]
        elif confused_count > 0 and confused_count > positive_count:
            sentiment = SENTIMENT_CONFUSED
            confidence = scores["confused"]
        elif positive_count > negative_count:
            sentiment = SENTIMENT_POSITIVE
            confidence = scores["positive"]
        elif negative_count > positive_count:
            sentiment = SENTIMENT_NEGATIVE
            confidence = scores["negative"]
        else:
            sentiment = SENTIMENT_NEUTRAL
            confidence = 0.5
        
        # Suggest emoji
        emoji_map = {
            SENTIMENT_POSITIVE: "😊",
            SENTIMENT_NEGATIVE: "😔",
            SENTIMENT_FRUSTRATED: "😤",
            SENTIMENT_CONFUSED: "🤔",
            SENTIMENT_NEUTRAL: ""
        }
        
        return {
            "sentiment": sentiment,
            "confidence": min(confidence + 0.3, 1.0),  # Boost confidence
            "scores": scores,
            "emoji_suggestion": emoji_map.get(sentiment, "")
        }


# ========================================
# ML-BASED SENTIMENT ANALYZER (Optional)
# ========================================

class MLSentimentAnalyzer:
    """ML-based sentiment analysis using transformers"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self._load_model()
    
    def _load_model(self):
        """Load sentiment model"""
        try:
            from transformers import pipeline
            self.model = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                truncation=True
            )
            log_info("ML Sentiment analyzer loaded")
        except ImportError:
            log_info("transformers not installed, using keyword-based sentiment only")
        except Exception as e:
            log_error(f"Failed to load sentiment model: {e}")
    
    def analyze(self, text: str) -> Dict:
        """Analyze sentiment using ML model"""
        if not self.model:
            return {"sentiment": SENTIMENT_NEUTRAL, "confidence": 0.0, "method": "unavailable"}
        
        try:
            result = self.model(text[:512])[0]  # Truncate for model
            
            # Map model labels to our categories
            label_map = {
                "positive": SENTIMENT_POSITIVE,
                "negative": SENTIMENT_NEGATIVE,
                "neutral": SENTIMENT_NEUTRAL
            }
            
            sentiment = label_map.get(result["label"].lower(), SENTIMENT_NEUTRAL)
            
            return {
                "sentiment": sentiment,
                "confidence": result["score"],
                "method": "ml"
            }
        except Exception as e:
            log_error(f"ML sentiment error: {e}")
            return {"sentiment": SENTIMENT_NEUTRAL, "confidence": 0.0, "method": "error"}


# ========================================
# HYBRID SENTIMENT ANALYZER
# ========================================

class HybridSentimentAnalyzer:
    """Combines keyword and ML sentiment analysis"""
    
    def __init__(self):
        self.keyword_analyzer = KeywordSentimentAnalyzer()
        self.ml_analyzer = MLSentimentAnalyzer()
        self.use_ml = self.ml_analyzer.model is not None
    
    def analyze(self, text: str) -> Dict:
        """Analyze sentiment using hybrid approach"""
        # Always get keyword analysis
        keyword_result = self.keyword_analyzer.analyze(text)
        
        result = {
            "sentiment": keyword_result["sentiment"],
            "confidence": keyword_result["confidence"],
            "scores": keyword_result["scores"],
            "emoji_suggestion": keyword_result["emoji_suggestion"],
            "method": "keyword"
        }
        
        # Use ML if available and keyword confidence is low
        if self.use_ml and keyword_result["confidence"] < 0.6:
            ml_result = self.ml_analyzer.analyze(text)
            
            if ml_result["confidence"] > keyword_result["confidence"]:
                result["sentiment"] = ml_result["sentiment"]
                result["confidence"] = ml_result["confidence"]
                result["method"] = "ml"
        
        log_info(f"Sentiment: {result['sentiment']} (confidence: {result['confidence']:.2f})")
        return result
    
    def get_response_modifier(self, sentiment: str) -> str:
        """Get response prefix based on sentiment"""
        modifiers = {
            SENTIMENT_POSITIVE: "",  # No modifier needed
            SENTIMENT_NEGATIVE: "I understand. ",
            SENTIMENT_FRUSTRATED: "I apologize for any inconvenience. ",
            SENTIMENT_CONFUSED: "Let me help clarify. ",
            SENTIMENT_NEUTRAL: ""
        }
        return modifiers.get(sentiment, "")
    
    def get_empathetic_response(self, sentiment: str, language: str = "english") -> str:
        """Get empathetic response based on sentiment"""
        responses = {
            SENTIMENT_POSITIVE: {
                "english": "I'm glad you're happy! ",
                "hindi": "Bahut khushi hui! "
            },
            SENTIMENT_NEGATIVE: {
                "english": "I'm sorry to hear that. How can I help make things better? ",
                "hindi": "Mujhe dukh hua. Main kaise madad kar sakta hoon? "
            },
            SENTIMENT_FRUSTRATED: {
                "english": "I understand your frustration. Let me try to help. ",
                "hindi": "Main aapki pareshani samajhta hoon. Main koshish karta hoon. "
            },
            SENTIMENT_CONFUSED: {
                "english": "Let me explain more clearly. ",
                "hindi": "Main aur clearly explain karta hoon. "
            },
            SENTIMENT_NEUTRAL: {
                "english": "",
                "hindi": ""
            }
        }
        
        sentiment_responses = responses.get(sentiment, responses[SENTIMENT_NEUTRAL])
        return sentiment_responses.get(language, sentiment_responses["english"])


# ========================================
# GLOBAL INSTANCE
# ========================================

_analyzer = None

def get_sentiment_analyzer() -> HybridSentimentAnalyzer:
    """Get or create global sentiment analyzer instance"""
    global _analyzer
    if _analyzer is None:
        _analyzer = HybridSentimentAnalyzer()
    return _analyzer


def analyze_sentiment(text: str) -> Dict:
    """Convenience function to analyze sentiment"""
    return get_sentiment_analyzer().analyze(text)


def get_sentiment(text: str) -> str:
    """Get just the sentiment label"""
    return analyze_sentiment(text)["sentiment"]


def get_empathetic_prefix(text: str, language: str = "english") -> str:
    """Get empathetic response prefix based on text sentiment"""
    result = analyze_sentiment(text)
    return get_sentiment_analyzer().get_empathetic_response(result["sentiment"], language)
