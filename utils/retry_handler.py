"""
Retry handler utility for API calls
"""
import time
import functools
from typing import Callable, Any, Type, Tuple
from utils.logger import Logger


def retry_on_failure(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """
    Decorator to retry function on failure
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay after each retry
        exceptions: Tuple of exception types to catch
        
    Returns:
        Decorated function with retry logic
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        Logger.warning(
                            f"{func.__name__} failed (attempt {attempt + 1}/{max_attempts}): {str(e)}"
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        Logger.error(
                            f"{func.__name__} failed after {max_attempts} attempts: {str(e)}"
                        )
            
            # If all retries failed, raise the last exception
            if last_exception:
                raise last_exception
            
        return wrapper
    return decorator


class RetryHandler:
    """Class-based retry handler for more complex scenarios"""
    
    def __init__(self, max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
        self.max_attempts = max_attempts
        self.delay = delay
        self.backoff = backoff
    
    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function with retry logic
        
        Args:
            func: Function to execute
            *args: Function positional arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function result
        """
        current_delay = self.delay
        last_exception = None
        
        for attempt in range(self.max_attempts):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt < self.max_attempts - 1:
                    Logger.warning(
                        f"Retry attempt {attempt + 1}/{self.max_attempts} failed: {str(e)}"
                    )
                    time.sleep(current_delay)
                    current_delay *= self.backoff
                else:
                    Logger.error(
                        f"All {self.max_attempts} retry attempts failed: {str(e)}"
                    )
        
        if last_exception:
            raise last_exception
