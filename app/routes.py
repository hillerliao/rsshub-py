from flask import Blueprint, render_template, jsonify
from importlib import import_module
import os
import inspect
from app.core.rss_generator import generate_rss

main = Blueprint('main', __name__)

# 爬虫注册表 - 用于动态加载和管理所有爬虫
spider_registry = {
    'emagazine': 'app.spiders.emagazine.EMagazineSpider'
}

@main.route('/')
def index():
    """Home page with available RSS feeds"""
    # 传递所有可用的RSS源到前端
    available_feeds = list(spider_registry.keys())
    return render_template('index.html', feeds=available_feeds)

@main.route('/<feed_name>')
def get_feed(feed_name):
    """统一的RSS源路由，支持动态加载任意注册的爬虫"""
    if feed_name not in spider_registry:
        return jsonify({'error': f'Feed "{feed_name}" not found'}), 404
    
    try:
        # 动态导入爬虫类
        module_path, class_name = spider_registry[feed_name].rsplit('.', 1)
        module = import_module(module_path)
        SpiderClass = getattr(module, class_name)
        
        # 实例化爬虫并获取内容
        spider = SpiderClass()
        items = spider.fetch_items()
        rss_content = generate_rss(items, feed_name)
        
        return rss_content, 200, {'Content-Type': 'application/rss+xml; charset=utf-8'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/feeds')
def list_feeds():
    """API端点：获取所有可用的RSS源列表"""
    return jsonify({
        'feeds': list(spider_registry.keys()),
        'count': len(spider_registry)
    })

@main.route('/health')
def health_check():
    """健康检查端点"""
    return jsonify({'status': 'healthy'}), 200