from app.spiders.base_spider import BaseSpider
from datetime import datetime
import xml.etree.ElementTree as ET

class EMagazineSpider(BaseSpider):
    """
    Spider for electronic magazine content from OPDS feed.
    Fetches and parses magazine data from https://emagazine.link/opds/new
    """
    
    def __init__(self):
        # 设置较长的缓存时间，OPDS源通常更新不频繁
        super().__init__(name='emagazine', cache_ttl=7200)
        self.opds_url = 'https://emagazine.link/opds/new'
    
    def fetch_items(self):
        """
        Fetch items from the OPDS feed.
        
        Returns:
            list: List of magazine items
        """
        try:
            # 获取OPDS XML数据
            opds_content = self.fetch_url(self.opds_url)
            
            # 解析OPDS XML
            items = self._parse_opds_feed(opds_content)
            
            return items
        except Exception as e:
            # 发生错误时返回空列表
            print(f"Error fetching OPDS feed: {e}")
            return []
    
    def _parse_opds_feed(self, xml_content):
        """
        Parse OPDS XML feed and extract magazine information.
        
        Args:
            xml_content (str): OPDS XML content
            
        Returns:
            list: List of parsed magazine items
        """
        items = []
        
        # 定义OPDS命名空间
        namespaces = {
            'atom': 'http://www.w3.org/2005/Atom',
            'dc': 'http://purl.org/dc/terms/',
            'dcterms': 'http://purl.org/dc/terms/'
        }
        
        try:
            # 解析XML
            root = ET.fromstring(xml_content)
            
            # 获取所有entry元素
            entries = root.findall('.//atom:entry', namespaces)
            
            for entry in entries:
                # 提取标题
                title_elem = entry.find('./atom:title', namespaces)
                title = title_elem.text if title_elem is not None else 'Unknown Title'
                
                    # 首先尝试获取acquisition类型的链接
                link = ''
                acquisition_links = entry.findall('./atom:link', namespaces)
                
                # 先寻找包含/epub/的链接
                epub_link = None
                for a_link in acquisition_links:
                    if a_link.get('rel') == 'http://opds-spec.org/acquisition':
                        href = a_link.get('href')
                        if href and '/epub/' in href:
                            epub_link = href
                            break
                
                # 如果找到epub链接，使用它
                if epub_link:
                    href = epub_link
                else:
                    # 否则使用第一个acquisition链接
                    href = None
                    for a_link in acquisition_links:
                        if a_link.get('rel') == 'http://opds-spec.org/acquisition':
                            href = a_link.get('href')
                            if href:
                                break
                
                # 处理找到的链接
                if href:
                    # 拼接完整的URL
                    if not href.startswith(('http://', 'https://')):
                        if href.startswith('/'):
                            link = f'https://emagazine.link{href}'
                        else:
                            link = f'https://emagazine.link/{href}'
                    else:
                        link = href
                
                # 如果没有找到acquisition链接，使用id作为备选
                if not link:
                    id_elem = entry.find('./atom:id', namespaces)
                    if id_elem is not None:
                        link = id_elem.text
                
                # 提取更新时间
                updated_elem = entry.find('./atom:updated', namespaces)
                pub_date = self._parse_opds_date(updated_elem.text) if updated_elem is not None else datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
                
                # 提取作者信息
                author_elem = entry.find('./atom:author/atom:name', namespaces)
                author = author_elem.text if author_elem is not None else ''
                
                # 提取出版社信息
                publisher_elem = entry.find('./atom:publisher/atom:name', namespaces)
                publisher = publisher_elem.text if publisher_elem is not None else ''
                
                # 提取摘要
                summary_elem = entry.find('./atom:summary', namespaces)
                summary = summary_elem.text if summary_elem is not None else ''
                
                # 构建描述信息
                description_parts = []
                if author:
                    description_parts.append(f'作者: {author}')
                if publisher:
                    description_parts.append(f'出版社: {publisher}')
                if summary:
                    description_parts.append(f'内容: {summary}')
                
                description = '<br>'.join(description_parts) if description_parts else '电子杂志'
                
                # 创建RSS项目
                items.append(self.create_item(
                    title=title,
                    link=link,
                    description=description,
                    pub_date=pub_date
                ))
        
        except ET.ParseError as e:
            print(f"XML parsing error: {e}")
        except Exception as e:
            print(f"Error parsing OPDS feed: {e}")
        
        return items
    
    def _parse_opds_date(self, date_str):
        """
        Parse date string from OPDS feed (ISO 8601 format).
        
        Args:
            date_str (str): ISO 8601 date string
            
        Returns:
            str: Formatted date string in RSS format
        """
        try:
            # OPDS使用ISO 8601格式，例如：2025-11-01T23:16:11+00:00
            # 移除时区部分的冒号以兼容strptime
            if ':' in date_str[-6:] and date_str[-3] == ':':
                date_str = date_str[:-3] + date_str[-2:]
            
            # 尝试不同的ISO 8601格式
            formats = ['%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%dT%H:%M:%SZ']
            
            for fmt in formats:
                try:
                    date_obj = datetime.strptime(date_str, fmt)
                    # 转换为RSS格式
                    return date_obj.strftime('%a, %d %b %Y %H:%M:%S %z')
                except ValueError:
                    continue
            
            # 如果所有格式都失败，返回当前时间
            return datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
            
        except Exception:
            # 发生任何错误时返回当前时间
            return datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')