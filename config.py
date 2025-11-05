import os
from datetime import timedelta

class Config:
    """
    应用配置类
    统一处理所有环境的配置，避免property问题
    """
    def __init__(self):
        # 基本配置
        self.DEBUG = os.environ.get('FLASK_ENV') != 'production'
        
        # SECRET_KEY 统一处理
        self.SECRET_KEY = os.environ.get('SECRET_KEY')
        if not self.SECRET_KEY:
            if os.environ.get('FLASK_ENV') == 'production':
                raise ValueError('生产环境必须设置SECRET_KEY环境变量')
            else:
                self.SECRET_KEY = 'dev-secret-key-change-in-production'
        
        # 缓存配置
        self.CACHE_DIR = os.environ.get('CACHE_DIR') or '/tmp/cache'
        self.DEFAULT_CACHE_TTL = int(os.environ.get('DEFAULT_CACHE_TTL', 3600))
        
        # 请求配置
        self.REQUEST_TIMEOUT = int(os.environ.get('REQUEST_TIMEOUT', 30))
        self.MAX_RETRIES = int(os.environ.get('MAX_RETRIES', 3))
        
        # RSS配置
        self.RSS_FEED_TITLE = os.environ.get('RSS_FEED_TITLE', 'RSS Generator')
        self.RSS_FEED_LINK = os.environ.get('RSS_FEED_LINK', 'https://example.com')
        self.RSS_FEED_DESCRIPTION = os.environ.get('RSS_FEED_DESCRIPTION', 'RSS生成服务')
        
        # 日志配置
        self.LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
        self.LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # API配置
        self.API_RATE_LIMIT = int(os.environ.get('API_RATE_LIMIT', 60))

# 创建配置实例
def get_config():
    env = os.environ.get('FLASK_ENV', 'development')
    
    config = Config()
    
    # 根据环境调整特定配置
    if env == 'development':
        config.DEBUG = True
        config.LOG_LEVEL = 'DEBUG'
        config.DEFAULT_CACHE_TTL = 300
    elif env == 'testing':
        config.TESTING = True
        config.DEBUG = False
        config.DEFAULT_CACHE_TTL = 60
    elif env == 'production':
        config.DEBUG = False
        config.LOG_LEVEL = 'INFO'
    
    return config

# 为了保持向后兼容性
config_by_name = {
    'development': lambda: get_config(),
    'testing': lambda: get_config(), 
    'production': lambda: get_config(),
    'default': lambda: get_config()
}