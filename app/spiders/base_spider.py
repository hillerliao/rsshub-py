from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
from app.core.cache import cache

class BaseSpider(ABC):
    """
    Base class for all spiders.
    Provides common functionality for fetching and parsing content.
    """
    
    def __init__(self, name=None, cache_ttl=3600):
        """
        Initialize the spider.
        
        Args:
            name (str): Name of the spider
            cache_ttl (int): Cache time-to-live in seconds
        """
        self.name = name or self.__class__.__name__
        self.cache_ttl = cache_ttl
    
    @abstractmethod
    def fetch_items(self):
        """
        Fetch items from the source.
        Must be implemented by subclasses.
        
        Returns:
            list: List of items with title, link, description, pub_date
        """
        pass
    
    def fetch_url(self, url, headers=None, use_cache=True):
        """
        Fetch URL content with caching support.
        
        Args:
            url (str): URL to fetch
            headers (dict): Optional headers
            use_cache (bool): Whether to use cache
        
        Returns:
            str: Response content
        """
        cache_key = f'url_{url}'
        
        # Try to get from cache first
        if use_cache:
            cached_content = cache.get(cache_key)
            if cached_content:
                return cached_content
        
        # Default headers
        if headers is None:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        
        # Fetch content
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        content = response.text
        
        # Cache the result
        if use_cache:
            cache.set(cache_key, content, self.cache_ttl)
        
        return content
    
    def parse_html(self, html_content):
        """
        Parse HTML content with BeautifulSoup.
        
        Args:
            html_content (str): HTML to parse
        
        Returns:
            BeautifulSoup: Parsed HTML object
        """
        return BeautifulSoup(html_content, 'html.parser')
    
    def create_item(self, title, link, description='', pub_date=None):
        """
        Create a standard item dictionary.
        
        Args:
            title (str): Item title
            link (str): Item link
            description (str): Item description
            pub_date (str): Item publication date in RSS format
        
        Returns:
            dict: Item dictionary
        """
        return {
            'title': title,
            'link': link,
            'description': description,
            'pub_date': pub_date
        }
    
    def clean_text(self, text):
        """
        Clean and normalize text.
        
        Args:
            text (str): Text to clean
        
        Returns:
            str: Cleaned text
        """
        if not text:
            return ''
        # Remove extra whitespace and normalize newlines
        return ' '.join(text.strip().split())