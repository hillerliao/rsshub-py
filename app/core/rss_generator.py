import datetime
import os
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

def generate_rss(items, feed_title):
    """
    Generate RSS XML content from a list of items.
    
    Args:
        items (list): List of dictionaries containing item data (title, link, description, pub_date)
        feed_title (str): Title of the RSS feed
    
    Returns:
        str: Formatted RSS XML string
    """
    # Create root element
    rss = Element('rss')
    rss.set('version', '2.0')
    # 添加XML命名空间声明以支持UTF-8","},{"old_str":
    
    # Create channel element
    channel = SubElement(rss, 'channel')
    
    # Add channel elements
    title = SubElement(channel, 'title')
    title.text = f'{feed_title.title()} RSS Feed'
    
    link = SubElement(channel, 'link')
    # 从环境变量读取RSS链接前缀，如果未设置则使用默认值
    rss_feed_link = os.environ.get('RSS_FEED_LINK', 'https://rsshubpy.vercel.app')
    link.text = f'{rss_feed_link}/{feed_title}'
    
    description = SubElement(channel, 'description')
    description.text = f'Latest updates from {feed_title.title()} source'
    
    pub_date = SubElement(channel, 'pubDate')
    pub_date.text = datetime.datetime.now(datetime.timezone.utc).strftime('%a, %d %b %Y %H:%M:%S %z')
    
    last_build_date = SubElement(channel, 'lastBuildDate')
    last_build_date.text = pub_date.text
    
    # Add items to channel
    for item in items:
        item_elem = SubElement(channel, 'item')
        
        # Add title
        item_title = SubElement(item_elem, 'title')
        item_title.text = item.get('title', 'Untitled')
        
        # Add link
        item_link = SubElement(item_elem, 'link')
        item_link.text = item.get('link', '')
        
        # Add description
        item_description = SubElement(item_elem, 'description')
        item_description.text = item.get('description', '')
        
        # Add pubDate
        if 'pub_date' in item:
            item_pub_date = SubElement(item_elem, 'pubDate')
            item_pub_date.text = item['pub_date']
        
        # Add guid
        item_guid = SubElement(item_elem, 'guid')
        item_guid.set('isPermaLink', 'true')
        item_guid.text = item.get('link', f'urn:uuid:{datetime.datetime.now().timestamp()}')
    
    # Convert to pretty XML string with proper encoding
    rough_string = tostring(rss, encoding='unicode')
    # 手动添加XML声明
    xml_declaration = '<?xml version="1.0" encoding="UTF-8" ?>\n'
    
    # 使用minidom美化XML
    reparsed = minidom.parseString(rough_string.encode('utf-8'))
    pretty_xml = reparsed.toprettyxml(indent='  ', encoding='utf-8').decode('utf-8')
    
    # 移除minidom自动添加的XML声明，使用我们自己的
    if pretty_xml.startswith('<?xml'):
        # 找到第一个换行符的位置
        first_newline = pretty_xml.find('\n')
        if first_newline != -1:
            pretty_xml = xml_declaration + pretty_xml[first_newline+1:]
    
    return pretty_xml