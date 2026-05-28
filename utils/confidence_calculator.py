"""
Confidence calculator utility
"""
from typing import Dict, List


class ConfidenceCalculator:
    
    @staticmethod
    def calculate_overall_confidence(scores: List[float], weights: List[float] = None) -> float:
        """
        Calculate weighted average confidence score
        
        Args:
            scores: List of individual scores (0-100)
            weights: Optional list of weights (must sum to 1.0)
            
        Returns:
            Overall confidence score (0-100)
        """
        if not scores:
            return 0.0
        
        if weights is None:
            weights = [1.0 / len(scores)] * len(scores)
        
        if len(scores) != len(weights):
            raise ValueError("Scores and weights must have same length")
        
        if abs(sum(weights) - 1.0) > 0.001:
            raise ValueError("Weights must sum to 1.0")
        
        weighted_sum = sum(score * weight for score, weight in zip(scores, weights))
        return round(weighted_sum, 2)
    
    @staticmethod
    def get_confidence_level(score: float) -> str:
        """
        Convert numeric confidence score to level
        
        Args:
            score: Confidence score (0-100)
            
        Returns:
            Confidence level string
        """
        if score >= 80:
            return "Very High"
        elif score >= 60:
            return "High"
        elif score >= 40:
            return "Moderate"
        elif score >= 20:
            return "Low"
        else:
            return "Very Low"
    
    @staticmethod
    def calculate_data_quality_score(data: Dict) -> float:
        """
        Calculate data quality score based on completeness
        
        Args:
            data: Data dictionary to evaluate
            
        Returns:
            Quality score (0-100)
        """
        if not data:
            return 0.0
        
        total_fields = len(data)
        non_null_fields = sum(1 for v in data.values() if v is not None and v != "")
        
        return (non_null_fields / total_fields) * 100 if total_fields > 0 else 0.0
    
    @staticmethod
    def adjust_confidence_by_source(base_confidence: float, source_status: str) -> float:
        """
        Adjust confidence based on data source status
        
        Args:
            base_confidence: Base confidence score
            source_status: Status of data source ('success', 'error', etc.)
            
        Returns:
            Adjusted confidence score
        """
        if source_status == "success":
            return base_confidence
        elif source_status == "partial":
            return base_confidence * 0.7
        elif source_status == "error":
            return base_confidence * 0.3
        else:
            return base_confidence * 0.5
