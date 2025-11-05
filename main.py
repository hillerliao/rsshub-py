from flask import Flask
import os
import logging
from app.routes import main as main_blueprint
from app.core.cache import Cache

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 让Vercel的环境变量优先
# 只在本地开发时设置默认环境变量
if not os.environ.get('FLASK_ENV'):
    os.environ['FLASK_ENV'] = 'development'

logger.info(f"Starting Flask application in {os.environ.get('FLASK_ENV')} mode")

# 创建Flask应用实例
app = Flask(__name__, template_folder='app/templates')

# 加载配置
from config import config_by_name
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config_by_name[config_name])

# 初始化缓存
# 在Vercel上使用临时目录存储缓存，因为Vercel的文件系统大部分是只读的
cache_dir = os.environ.get('CACHE_DIR', '/tmp')
# 确保在生产环境下使用临时目录
if os.environ.get('FLASK_ENV') == 'production':
    cache_dir = '/tmp'
cache = Cache(cache_dir=cache_dir)

# 注册蓝图
app.register_blueprint(main_blueprint)

# 自定义错误处理
@app.errorhandler(404)
def page_not_found(e):
    """处理404错误"""
    logger.warning(f"404 Not Found: {e}")
    return {'error': '页面未找到', 'message': '请检查您的URL是否正确'}, 404

@app.errorhandler(500)
def internal_server_error(e):
    """处理500错误"""
    logger.error(f"500 Internal Server Error: {e}")
    return {'error': '服务器内部错误', 'message': '服务器遇到了一个问题，请稍后再试'}, 500

@app.errorhandler(Exception)
def handle_exception(e):
    """处理所有未捕获的异常"""
    logger.error(f"Unhandled exception: {e}", exc_info=True)
    return {'error': '服务器内部错误', 'message': '服务器遇到了一个问题，请稍后再试'}, 500

# 健康检查端点已在蓝图中定义

# 主程序入口
if __name__ == '__main__':
    # 获取端口和主机配置
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    # 启动应用
    app.run(
        host=host,
        port=port,
        debug=app.config.get('DEBUG', False)
    )

# 导出Flask应用实例供Vercel使用
# Vercel需要一个名为'application'的变量来识别Flask应用
application = app