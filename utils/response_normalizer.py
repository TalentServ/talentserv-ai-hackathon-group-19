"""
Response normalizer utility
"""
from typing import Dict, Any
from datetime import datetime


class ResponseNormalizer:
    
    @staticmethod
    def normalize_response(data: Dict[str, Any], source: str = "Unknown", 
                          status: str = "success") -> Dict[str, Any]:
        """
        Normalize API response with standard metadata
        
        Args:
            data: Response data
            source: Data source name
            status: Response status
            
        Returns:
            Normalized response with metadata
        """
        normalized = {
            **data,
            "timestamp": data.get("timestamp", datetime.utcnow().isoformat()),
            "source": data.get("source", source),
            "status": data.get("status", status)
        }
        
        # Add confidence if not present
        if "confidence" not in normalized:
            normalized["confidence"] = ResponseNormalizer._infer_confidence(data, status)
        
        return normalized
    
    @staticmethod
    def normalize_error_response(error: str, source: str = "Unknown", 
                                location: str = "Unknown") -> Dict[str, Any]:
        """
        Create standardized error response
        
        Args:
            error: Error message
            source: Data source name
            location: Location context
            
        Returns:
            Normalized error response
        """
        return {
            "status": "error",
            "error": error,
            "location": location,
            "source": source,
            "timestamp": datetime.utcnow().isoformat(),
            "confidence": "none",
            "data": None
        }
    
    @staticmethod
    def normalize_list_response(items: list, source: str = "Unknown", 
                               location: str = "Unknown") -> Dict[str, Any]:
        """
        Normalize list response with metadata
        
        Args:
            items: List of items
            source: Data source name
            location: Location context
            
        Returns:
            Normalized list response
        """
        return {
            "items": items,
            "total_count": len(items),
            "location": location,
            "source": source,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "success",
            "confidence": "high" if len(items) > 0 else "low"
        }
    
    @staticmethod
    def add_metadata(data: Dict[str, Any], **metadata) -> Dict[str, Any]:
        """
        Add additional metadata to response
        
        Args:
            data: Original data
            **metadata: Additional metadata fields
            
        Returns:
            Data with added metadata
        """
        return {
            **data,
            **metadata,
            "timestamp": data.get("timestamp", datetime.utcnow().isoformat())
        }
    
    @staticmethod
    def _infer_confidence(data: Dict, status: str) -> str:
        """Infer confidence level from data completeness"""
        if status == "error":
            return "none"
        
        # Count non-null values
        non_null = sum(1 for v in data.values() if v is not None and v != "")
        total = len(data)
        
        completeness = non_null / total if total > 0 else 0
        
        if completeness >= 0.9:
            return "high"
        elif completeness >= 0.6:
            return "medium"
        elif completeness >= 0.3:
            return "low"
        else:
            return "very_low"
