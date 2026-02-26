"""
安全過濾模組：檢查查詢是否符合公司政策和倫理規範
"""
from typing import Dict, Tuple
import re
from config import RESTRICTED_KEYWORDS


class SafetyFilter:
    """
    安全過濾器：用於檢查和阻止不當查詢
    """
    
    def __init__(self):
        """初始化安全過濾器"""
        self.restricted_patterns = [
            re.compile(pattern, re.IGNORECASE) 
            for pattern in RESTRICTED_KEYWORDS
        ]
        
        # 公司政策相關的禁止內容
        self.policy_violations = [
            '如何洩露客戶資料',
            '如何繞過安全措施',
            '如何進行不道德的行為',
            '歧視性內容',
            '非法活動'
        ]
    
    def check_query(self, query: str) -> Tuple[bool, str]:
        """
        檢查查詢是否安全
        
        Args:
            query: 用戶查詢字符串
            
        Returns:
            Tuple[bool, str]: (是否安全, 如果 unsafe 則返回原因)
        """
        query_lower = query.lower()
        
        # 檢查限制關鍵詞
        for pattern in self.restricted_patterns:
            if pattern.search(query):
                return False, f'查詢包含不當內容，違反公司政策。'
        
        # 檢查政策違規
        for violation in self.policy_violations:
            if violation in query_lower:
                return False, f'查詢違反公司政策和倫理規範。'
        
        # 檢查是否嘗試繞過系統
        bypass_attempts = ['忽略政策', '繞過規則', '無視安全']
        for attempt in bypass_attempts:
            if attempt in query_lower:
                return False, '無法繞過安全檢查。請遵守公司政策。'
        
        return True, ''
    
    def filter_response(self, response: str) -> str:
        """
        過濾回應內容，確保不包含敏感信息
        
        Args:
            response: AI 生成的回應
            
        Returns:
            過濾後的回應
        """
        # 移除可能洩露的敏感信息模式
        # 這裡可以添加更多過濾邏輯
        
        return response

