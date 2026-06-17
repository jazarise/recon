class PredictiveEngine:
    @staticmethod
    def analyze_trends(diffs: list) -> list:
        predictions = []
        new_apis = sum(1 for d in diffs if "api" in d.get("event", "").lower())
        
        if new_apis >= 2:
            predictions.append("Predictive Alert: High likelihood of incoming unauthenticated API exposure within 7 days. Action required.")
            
        return predictions
