"""
Logger utility
"""
import logging
import os
from datetime import datetime
from typing import Optional


class Logger:
    _instance: Optional[logging.Logger] = None
    
    @classmethod
    def get_logger(cls, name: str = "TravelMind") -> logging.Logger:
        """
        Get or create logger instance
        
        Args:
            name: Logger name
            
        Returns:
            Configured logger instance
        """
        if cls._instance is None:
            cls._instance = cls._setup_logger(name)
        return cls._instance
    
    @classmethod
    def _setup_logger(cls, name: str) -> logging.Logger:
        """Setup logger with console and file handlers"""
        logger = logging.Logger(name)
        logger.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)
        
        # File handler (optional)
        if os.getenv("DEBUG", "False").lower() == "true":
            os.makedirs("logs", exist_ok=True)
            log_file = f"logs/travelmind_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_format = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
            )
            file_handler.setFormatter(file_format)
            logger.addHandler(file_handler)
        
        return logger
    
    @classmethod
    def info(cls, message: str):
        """Log info message"""
        logger = cls.get_logger()
        logger.info(message)
    
    @classmethod
    def error(cls, message: str):
        """Log error message"""
        logger = cls.get_logger()
        logger.error(message)
    
    @classmethod
    def warning(cls, message: str):
        """Log warning message"""
        logger = cls.get_logger()
        logger.warning(message)
    
    @classmethod
    def debug(cls, message: str):
        """Log debug message"""
        logger = cls.get_logger()
        logger.debug(message)
