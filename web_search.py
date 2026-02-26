"""
網絡搜索模組：處理外部知識查詢
"""
from typing import List, Dict
from duckduckgo_search import DDGS


class WebSearch:
    """
    網絡搜索工具：使用 DuckDuckGo 搜索外部信息
    """
    
    def __init__(self):
        """初始化網絡搜索"""
        self.ddgs = DDGS()
    
    def search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """
        搜索網絡信息
        
        Args:
            query: 搜索查詢
            max_results: 最大結果數量
            
        Returns:
            List[Dict]: 搜索結果列表，每個包含 title, snippet, url
        """
        try:
            results = self.ddgs.text(query, max_results=max_results)
            
            formatted_results = []
            for result in results:
                formatted_results.append({
                    'title': result.get('title', ''),
                    'snippet': result.get('body', ''),
                    'url': result.get('href', '')
                })
            
            return formatted_results
        except Exception as e:
            print(f'網絡搜索錯誤: {e}')
            return []
    
    def format_results(self, results: List[Dict[str, str]]) -> str:
        """
        格式化搜索結果為文本
        
        Args:
            results: 搜索結果列表
            
        Returns:
            str: 格式化後的文本
        """
        if not results:
            return '未找到相關的網絡信息。'
        
        formatted = '網絡搜索結果：\n\n'
        for i, result in enumerate(results, 1):
            formatted += f'{i}. {result["title"]}\n'
            formatted += f'   {result["snippet"]}\n'
            formatted += f'   來源: {result["url"]}\n\n'
        
        return formatted

