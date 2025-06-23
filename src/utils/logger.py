import logging
import pprint
import inspect
from typing import Any

def setup_logger():
    """Configure and get the logger for the application."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)

def debug_print(obj: Any, title: str = None):
    """
    Pretty print an object with an optional title and caller information.
    Useful for debugging complex data structures.
    
    Args:
        obj: Any object to debug print
        title: Optional title to print before the object
    """
    caller = inspect.currentframe().f_back
    caller_info = f"{inspect.getmodule(caller).__name__}:{caller.f_lineno}"
    
    print("\n" + "="*80)
    if title:
        print(f"DEBUG [{caller_info}] - {title}")
    else:
        print(f"DEBUG [{caller_info}]")
    print("-"*80)
    pprint.pprint(obj)
    print("="*80 + "\n")
