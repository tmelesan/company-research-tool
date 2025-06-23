import json
import os
import time
from typing import Dict, Any, Optional
from pathlib import Path
import hashlib
import logging

logger = logging.getLogger(__name__)

class CacheManager:
    """
    A cache manager for storing and retrieving research results.
    Implements disk-based caching with TTL (Time To Live) and namespace support.
    """
    def __init__(self, cache_dir: str = ".cache", default_ttl: int = 86400):
        """
        Initialize the cache manager.
        
        Args:
            cache_dir (str): Directory to store cache files
            default_ttl (int): Default TTL in seconds (86400 = 24 hours)
        """
        self.cache_dir = Path(cache_dir)
        self.default_ttl = default_ttl
        self._ensure_cache_dir()
    
    def _ensure_cache_dir(self) -> None:
        """Ensure the cache directory exists."""
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def _get_cache_key(self, namespace: str, key_data: Dict[str, Any]) -> str:
        """
        Generate a cache key from the input data.
        
        Args:
            namespace (str): Cache namespace (e.g., 'company_existence', 'domain_validation')
            key_data (Dict[str, Any]): Data to generate key from
            
        Returns:
            str: Cache key
        """
        # Sort dictionary keys for consistent hashing
        serialized = json.dumps(key_data, sort_keys=True)
        key_hash = hashlib.sha256(serialized.encode()).hexdigest()
        return f"{namespace}_{key_hash}"
    
    def _get_cache_path(self, cache_key: str) -> Path:
        """Get the full path for a cache file."""
        return self.cache_dir / f"{cache_key}.json"
    
    def get(self, namespace: str, key_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Retrieve data from cache if it exists and is not expired.
        
        Args:
            namespace (str): Cache namespace
            key_data (Dict[str, Any]): Data to generate cache key from
            
        Returns:
            Optional[Dict[str, Any]]: Cached data or None if not found/expired
        """
        try:
            cache_key = self._get_cache_key(namespace, key_data)
            cache_path = self._get_cache_path(cache_key)
            
            if not cache_path.exists():
                return None
            
            with open(cache_path, 'r', encoding='utf-8') as f:
                cached = json.load(f)
            
            # Check if cache is expired
            if time.time() > cached['expires_at']:
                self.delete(namespace, key_data)
                return None
            
            logger.debug(f"Cache hit for {namespace}: {key_data}")
            return cached['data']
            
        except Exception as e:
            logger.warning(f"Error reading cache: {str(e)}")
            return None
    
    def set(self, namespace: str, key_data: Dict[str, Any], data: Dict[str, Any], ttl: Optional[int] = None) -> None:
        """
        Store data in cache with TTL.
        
        Args:
            namespace (str): Cache namespace
            key_data (Dict[str, Any]): Data to generate cache key from
            data (Dict[str, Any]): Data to cache
            ttl (Optional[int]): Time to live in seconds, uses default_ttl if None
        """
        try:
            cache_key = self._get_cache_key(namespace, key_data)
            cache_path = self._get_cache_path(cache_key)
            
            cache_data = {
                'expires_at': time.time() + (ttl or self.default_ttl),
                'data': data,
                'key_data': key_data,
                'namespace': namespace
            }
            
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
                
            logger.debug(f"Cached data for {namespace}: {key_data}")
            
        except Exception as e:
            logger.warning(f"Error writing to cache: {str(e)}")
    
    def delete(self, namespace: str, key_data: Dict[str, Any]) -> bool:
        """
        Delete a cache entry.
        
        Args:
            namespace (str): Cache namespace
            key_data (Dict[str, Any]): Data to generate cache key from
            
        Returns:
            bool: True if cache was deleted, False otherwise
        """
        try:
            cache_key = self._get_cache_key(namespace, key_data)
            cache_path = self._get_cache_path(cache_key)
            
            if cache_path.exists():
                os.remove(cache_path)
                logger.debug(f"Deleted cache for {namespace}: {key_data}")
                return True
                
            return False
            
        except Exception as e:
            logger.warning(f"Error deleting cache: {str(e)}")
            return False
    
    def clear_namespace(self, namespace: str) -> int:
        """
        Clear all cache entries in a namespace.
        
        Args:
            namespace (str): Cache namespace to clear
            
        Returns:
            int: Number of cache entries cleared
        """
        try:
            count = 0
            for cache_file in self.cache_dir.glob(f"{namespace}_*.json"):
                try:
                    os.remove(cache_file)
                    count += 1
                except OSError:
                    continue
            
            logger.info(f"Cleared {count} entries from namespace: {namespace}")
            return count
            
        except Exception as e:
            logger.warning(f"Error clearing namespace {namespace}: {str(e)}")
            return 0
    
    def clear_all(self) -> int:
        """
        Clear all cache entries.
        
        Returns:
            int: Number of cache entries cleared
        """
        try:
            count = 0
            for cache_file in self.cache_dir.glob("*.json"):
                try:
                    os.remove(cache_file)
                    count += 1
                except OSError:
                    continue
            
            logger.info(f"Cleared all cache entries: {count} total")
            return count
            
        except Exception as e:
            logger.warning(f"Error clearing all cache: {str(e)}")
            return 0
