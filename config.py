import os
from datetime import timedelta

class Config:
    """
    应用配置类
    包含所有环境下共享的配置项
    """
    # 基本配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_ENV') != 'production'
    
    # 缓存配置
    CACHE_DIR = os.environ.get('CACHE_DIR') or './cache'
    DEFAULT_CACHE_TTL = int(os.environ.get('DEFAULT_CACHE_TTL', 3600))  # 默认缓存1小时
    
    # 请求配置
    REQUEST_TIMEOUT = int(os.environ.get('REQUEST_TIMEOUT', 30))  # 请求超时时间（秒）
    MAX_RETRIES = int(os.environ.get('MAX_RETRIES', 3))  # 请求失败最大重试次数
    
    # RSS配置
    RSS_FEED_TITLE = os.environ.get('RSS_FEED_TITLE', 'RSS Generator')
    RSS_FEED_LINK = os.environ.get('RSS_FEED_LINK', 'https://example.com')
    RSS_FEED_DESCRIPTION = os.environ.get('RSS_FEED_DESCRIPTION', '多源RSS聚合服务')
    
    # 日志配置
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # API配置
    API_RATE_LIMIT = int(os.environ.get('API_RATE_LIMIT', 60))  # 每分钟请求限制

class DevelopmentConfig(Config):
    """
    开发环境配置
    """
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    DEFAULT_CACHE_TTL = 300  # 开发环境缓存5分钟

class TestingConfig(Config):
    """
    测试环境配置
    """
    TESTING = True
    WTF_CSRF_ENABLED = False
    DEBUG = False
    DEFAULT_CACHE_TTL = 60  # 测试环境缓存1分钟

class ProductionConfig(Config):
    """
    生产环境配置
    """
    DEBUG = False
    LOG_LEVEL = 'INFO'
    # 生产环境应该从环境变量获取密钥
    @property
    def SECRET_KEY(self):
        secret_key = os.environ.get('SECRET_KEY')
        if not secret_key:
            raise ValueError('生产环境必须设置SECRET_KEY环境变量')
        return secret_key

# 配置映射，用于根据环境变量选择配置类
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}