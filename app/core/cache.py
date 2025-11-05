import json
import os
import time
from datetime import datetime, timedelta

class Cache:
    """
    Simple file-based caching system for RSS feed data.
    """
    
    def __init__(self, cache_dir='./cache', default_ttl=3600):
        """
        Initialize cache with directory and default TTL.
        
        Args:
            cache_dir (str): Directory to store cache files
            default_ttl (int): Default time-to-live in seconds
        """
        self.default_ttl = default_ttl
        
        # Create cache directory if it doesn't exist
        try:
            os.makedirs(cache_dir, exist_ok=True)
            self.cache_dir = cache_dir
        except Exception as e:
            # 如果无法创建目录，可能是生产环境只读文件系统
            # 尝试使用/tmp目录作为备选
            if cache_dir != '/tmp':
                self.cache_dir = '/tmp'
                os.makedirs(self.cache_dir, exist_ok=True)
            else:
                # 如果连/tmp都失败，则无法使用缓存
                raise
    
    def _get_cache_file_path(self, key):
        """
        Get the file path for a cache key.
        
        Args:
            key (str): Cache key
        
        Returns:
            str: File path
        """
        safe_key = key.replace('/', '_').replace('\\', '_')
        return os.path.join(self.cache_dir, f'{safe_key}.json')
    
    def set(self, key, data, ttl=None):
        """
        Set a value in the cache.
        
        Args:
            key (str): Cache key
            data (any): Data to cache (must be JSON serializable)
            ttl (int): Time-to-live in seconds (optional)
        """
        if ttl is None:
            ttl = self.default_ttl
        
        cache_data = {
            'data': data,
            'timestamp': time.time(),
            'expires_at': time.time() + ttl
        }
        
        file_path = self._get_cache_file_path(key)
        with open(file_path, 'w') as f:
            json.dump(cache_data, f)
    
    def get(self, key):
        """
        Get a value from the cache if it exists and hasn't expired.
        
        Args:
            key (str): Cache key
        
        Returns:
            any: Cached data or None if not found or expired
        """
        file_path = self._get_cache_file_path(key)
        
        if not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, 'r') as f:
                cache_data = json.load(f)
            
            # Check if cache has expired
            if time.time() > cache_data['expires_at']:
                # Delete expired cache
                os.remove(file_path)
                return None
            
            return cache_data['data']
        except Exception:
            # If there's any error reading the cache, consider it invalid
            try:
                os.remove(file_path)
            except:
                pass
            return None
    
    def delete(self, key):
        """
        Delete a cache entry.
        
        Args:
            key (str): Cache key
        """
        file_path = self._get_cache_file_path(key)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
    
    def clear(self):
        """
        Clear all cache entries.
        """
        for filename in os.listdir(self.cache_dir):
            if filename.endswith('.json'):
                try:
                    os.remove(os.path.join(self.cache_dir, filename))
                except:
                    pass
    
    def get_stats(self):
        """
        Get cache statistics.
        
        Returns:
            dict: Cache statistics
        """
        total = 0
        expired = 0
        current_time = time.time()
        
        for filename in os.listdir(self.cache_dir):
            if filename.endswith('.json'):
                total += 1
                file_path = os.path.join(self.cache_dir, filename)
                try:
                    with open(file_path, 'r') as f:
                        cache_data = json.load(f)
                    if current_time > cache_data['expires_at']:
                        expired += 1
                except:
                    expired += 1
        
        return {
            'total': total,
            'expired': expired,
            'valid': total - expired
        }

# Create a global cache instance
cache = Cache()