import torch
from transformers import pipeline
from collections import defaultdict

class ReviewAnalyzer:
    def __init__(self):
        # Use GPU if available
        self.device = 0 if torch.cuda.is_available() else -1
        
        # Load zero-shot classification model
        self.classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
            device=self.device
        )

        # Predefined categories and candidate labels
        self.insight_categories = {
            "Positive Highlights (Strengths)": [
                "what the customer liked",
                "positive experience",
                "trust or loyalty",
                "good design",
                "ease of use",
                "satisfaction",
            ],
            "Negative Feedback (Pain Points)": [
                "what the customer disliked",
                "bugs or issues",
                "frustration",
                "unmet expectations",
                "confusion or disappointment",
            ],
            "Feature Requests / Improvement Suggestions": [
                "requested features",
                "improvements",
                "enhancements",
                "missing functionality",
            ],
            "Usability & Experience Insights": [
                "ease of use",
                "navigation",
                "user interface",
                "learning curve",
                "discoverability",
            ],
            "Performance & Reliability": [
                "crashes",
                "lag",
                "slow performance",
                "instability",
                "bugs or inconsistency",
            ],
            "Support & Communication": [
                "customer support",
                "response time",
                "clarity of instructions",
                "communication quality",
            ],
            "Pricing & Value Perception": [
                "price",
                "value for money",
                "affordability",
                "expensive or cheap",
            ],
            "Customer Persona Insight": [
                "casual user",
                "business owner",
                "student",
                "developer",
                "professional",
            ],
        }

        # Storage for aggregated data
        self.insight_summary = defaultdict(lambda: defaultdict(int))
        self.sentiment_summary = defaultdict(int)

    def analyze(self, review_text: str):
        # Sentiment analysis
        sentiment_labels = ["Positive", "Negative", "Neutral"]
        sentiment_result = self.classifier(review_text, sentiment_labels)
        sentiment = sentiment_result["labels"][0]
        self.sentiment_summary[sentiment] += 1

        # Insight detection
        for category, candidate_labels in self.insight_categories.items():
            result = self.classifier(review_text, candidate_labels, multi_label=True)
            for label, score in zip(result["labels"], result["scores"]):
                if score > 0.4:  # confidence threshold
                    self.insight_summary[category][label] += 1

    def get_summary(self):
        # Return structured Python dictionary (not JSON)
        return {
            "Sentiment Distribution": dict(self.sentiment_summary),
            "Insights Summary": {cat: dict(labels) for cat, labels in self.insight_summary.items()}
        }

# Example usage
if __name__ == "__main__":
    analyzer = ReviewAnalyzer()

    reviews = [
        "I love the clean interface! But it crashes when I upload photos.",
        "It would be great if there was an option to export reports to Excel.",
        "The app is a bit slow but customer support was helpful.",
        "As a business owner, I find the dashboard extremely useful and fast.",
        "Too expensive for what it offers, not worth the subscription cost."
    ]

    for review in reviews:
        analyzer.analyze(review)

    summary = analyzer.get_summary()
    print(summary)