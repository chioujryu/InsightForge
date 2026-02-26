"""
Agent 系統模組：智能決策和查詢路由
"""
from typing import Optional, Dict, Any
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.tools import Tool
import config
from rag_system import RAGSystem
from web_search import WebSearch
from safety_filter import SafetyFilter
from crypto_analysis import CryptoDataExplorer


class CompanyAssistantAgent:
    """
    公司助手 Agent：智能路由查詢到適當的數據源
    """
    
    def __init__(self):
        """初始化 Agent 系統"""
        # 初始化組件
        self.rag_system = RAGSystem()
        self.web_search = WebSearch()
        self.safety_filter = SafetyFilter()
        self.crypto_explorer = CryptoDataExplorer()
        
        # 初始化 LLM
        api_key = config.OPENROUTER_API_KEY or config.OPENAI_API_KEY
        
        # 配置 LLM，優先使用 OpenRouter
        if config.OPENROUTER_API_KEY:
            # 使用 OpenRouter
            self.llm = ChatOpenAI(
                model=config.LLM_MODEL,
                temperature=config.LLM_TEMPERATURE,
                openai_api_key=api_key,
                base_url=config.OPENROUTER_API_BASE,
                default_headers={
                    "HTTP-Referer": "https://github.com/zurumelon/company-assistant",
                    "X-Title": "ZURU Melon Company Assistant"
                }
            )
        else:
            # 使用標準 OpenAI API
            self.llm = ChatOpenAI(
                model=config.OPENAI_LLM_MODEL,
                temperature=config.LLM_TEMPERATURE,
                openai_api_key=api_key
            )
        
        # 建立工具
        self.tools = self._create_tools()
    
    def _create_tools(self) -> list:
        """
        創建 Agent 可使用的工具
        
        Returns:
            list: 工具列表
        """
        def search_knowledge_base(query: str) -> str:
            """搜索公司知識庫"""
            context = self.rag_system.get_relevant_context(query)
            if not context:
                return '知識庫中未找到相關信息。'
            return f'知識庫內容：\n{context}'
        
        def search_web(query: str) -> str:
            """搜索網絡信息"""
            results = self.web_search.search(query, max_results=3)
            return self.web_search.format_results(results)
        
        # 注意：這裡創建的工具目前未在主要查詢流程中使用
        # 但保留了結構以便未來擴展為完整的 Agent 系統
        try:
            tools = [
                Tool(
                    name='search_knowledge_base',
                    func=search_knowledge_base,
                    description='用於搜索公司內部知識庫，包括編碼風格、公司政策、程序指南等內部文檔。當用戶詢問關於公司內部政策、程序、編碼標準等問題時使用。'
                ),
                Tool(
                    name='search_web',
                    func=search_web,
                    description='用於搜索互聯網上的最新信息。當用戶詢問外部知識、最新技術、一般性問題或知識庫中沒有信息時使用。'
                )
            ]
            return tools
        except Exception:
            # 如果 Tool 導入有問題，返回空列表
            return []
    
    def _should_use_knowledge_base(self, query: str) -> bool:
        """
        判斷是否應該使用知識庫
        
        Args:
            query: 用戶查詢
            
        Returns:
            bool: 是否使用知識庫
        """
        company_keywords = [
            '公司', '政策', '程序', '指南', '編碼風格', 'coding style',
            'policy', 'procedure', 'guideline', 'zuru', 'melon',
            '內部', '員工', '規定', '規範', '標準'
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in company_keywords)
    
    def _is_crypto_query(self, query: str) -> bool:
        """
        判斷是否為加密貨幣數據分析相關的查詢
        
        Args:
            query: 用戶查詢
            
        Returns:
            bool: 是否為 crypto 相關查詢
        """
        crypto_keywords = [
            'crypto', '加密貨幣', 'bitcoin', 'btc', 'ethereum', 'eth',
            'market_cap', '市值', '價格', 'current_price', '交易量',
            '畫出', '繪製', '圖表', '分析', '關係', '散點圖', '直方圖', '箱型圖',
            'correlation', '相關性', '熱力圖', 'heatmap',
            'top_250', 'crypto_20251222'
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in crypto_keywords)
    
    def _handle_crypto_query(self, query: str) -> Dict[str, Any]:
        """
        處理加密貨幣數據分析相關的查詢
        
        Args:
            query: 用戶查詢
            
        Returns:
            Dict: 包含回應、來源等信息的字典
        """
        try:
            # 嘗試解析自然語言查詢
            parsed = self.crypto_explorer.parse_natural_language_query(query)
            
            if parsed:
                # 成功解析，執行對應的圖表繪製
                plot_type = parsed["plot_type"]
                columns = parsed["columns"]
                
                if plot_type == "correlation":
                    # 繪製相關性熱力圖
                    result = self.crypto_explorer.plot_correlation_heatmap()
                    analysis = self.crypto_explorer.get_correlation_analysis()
                    response = f"{result.description}\n\n{analysis}"
                    return {
                        'response': response,
                        'source': 'crypto_analysis',
                        'plot_path': result.path,
                        'needs_clarification': False
                    }
                elif plot_type == "scatter" and len(columns) >= 2:
                    # 繪製散點圖
                    result = self.crypto_explorer.plot_scatter(columns[0], columns[1])
                    # 計算相關係數
                    df = self.crypto_explorer.load_data()
                    corr = df[[columns[0], columns[1]]].corr().iloc[0, 1]
                    response = f"{result.description}\n\n**相關係數**：{corr:.3f}"
                    return {
                        'response': response,
                        'source': 'crypto_analysis',
                        'plot_path': result.path,
                        'needs_clarification': False
                    }
                elif plot_type == "histogram" and len(columns) >= 1:
                    # 繪製直方圖
                    result = self.crypto_explorer.plot_histogram(columns[0])
                    response = result.description
                    return {
                        'response': response,
                        'source': 'crypto_analysis',
                        'plot_path': result.path,
                        'needs_clarification': False
                    }
                elif plot_type == "boxplot" and len(columns) >= 1:
                    # 繪製箱型圖
                    result = self.crypto_explorer.plot_boxplot(columns[0])
                    response = result.description
                    return {
                        'response': response,
                        'source': 'crypto_analysis',
                        'plot_path': result.path,
                        'needs_clarification': False
                    }
            
            # 如果查詢包含「建議」、「分析建議」、「應該分析」等關鍵詞
            if any(word in query.lower() for word in ['建議', '應該', '分析', 'suggest', 'recommend', 'correlation']):
                # 提供相關性分析建議
                analysis = self.crypto_explorer.get_correlation_analysis()
                response = f"## 加密貨幣數據分析建議\n\n{analysis}\n\n**提示**：您可以說「請畫出相關性熱力圖」來查看完整的相關係數矩陣。"
                return {
                    'response': response,
                    'source': 'crypto_analysis',
                    'needs_clarification': False
                }
            
            # 如果查詢包含「欄位」、「column」、「意思」等關鍵詞
            if any(word in query.lower() for word in ['欄位', 'column', '意思', '說明', '解釋', 'info', 'columns']):
                summary = self.crypto_explorer.describe_dataset()
                response = f"## 加密貨幣數據集資訊\n\n{summary}"
                return {
                    'response': response,
                    'source': 'crypto_analysis',
                    'needs_clarification': False
                }
            
            # 如果無法解析，使用 LLM 來理解查詢並提供建議
            prompt = self._create_crypto_prompt(query)
            llm_response = self.llm.invoke([HumanMessage(content=prompt)]).content
            
            return {
                'response': llm_response,
                'source': 'crypto_analysis',
                'needs_clarification': False
            }
            
        except Exception as e:
            return {
                'response': f'處理加密貨幣數據查詢時發生錯誤：{str(e)}',
                'source': 'error',
                'needs_clarification': False
            }
    
    def _create_crypto_prompt(self, query: str) -> str:
        """創建加密貨幣數據分析的提示"""
        df = self.crypto_explorer.load_data()
        columns = self.crypto_explorer.get_columns()
        column_descriptions = self.crypto_explorer.get_column_descriptions()
        
        columns_info = "\n".join([f"- **{col}**: {column_descriptions.get(col, '無說明')}" for col in columns])
        
        return f"""你是一個專業的數據分析助手，專門處理加密貨幣市場數據分析。

用戶查詢：{query}

可用的數據欄位：
{columns_info}

數據集包含 250 種加密貨幣的市場快照數據。

請根據用戶的查詢，提供以下幫助：
1. 如果用戶想要繪製圖表，請明確告訴他們應該使用哪些欄位和圖表類型
2. 如果用戶詢問欄位意思，請根據上述欄位說明回答
3. 如果用戶想要分析建議，請根據數據特性提供建議
4. 如果用戶的查詢不夠明確，請詢問更多細節

可用的圖表類型：
- 直方圖（histogram）：用於單一數值欄位的分佈分析
- 箱型圖（boxplot）：用於觀察中位數、四分位數和異常值
- 散點圖（scatter）：用於兩個數值欄位之間的關係分析
- 相關性熱力圖（correlation heatmap）：用於查看所有數值欄位之間的相關係數

回答（使用繁體中文，要具體且實用）："""
    
    def query(self, user_query: str) -> Dict[str, Any]:
        """
        處理用戶查詢
        
        Args:
            user_query: 用戶查詢字符串
            
        Returns:
            Dict: 包含回應、來源等信息的字典
        """
        # 安全檢查
        is_safe, safety_message = self.safety_filter.check_query(user_query)
        if not is_safe:
            return {
                'response': f'抱歉，{safety_message}',
                'source': 'safety_filter',
                'needs_clarification': False
            }
        
        # 判斷查詢類型並生成回應
        try:
            # 優先檢查是否為加密貨幣數據分析查詢
            if self._is_crypto_query(user_query):
                return self._handle_crypto_query(user_query)
            
            # 使用簡單的決策邏輯（也可以使用更複雜的 Agent）
            if self._should_use_knowledge_base(user_query):
                # 使用知識庫
                context = self.rag_system.get_relevant_context(user_query)
                
                if context:
                    prompt = self._create_kb_prompt(user_query, context)
                    response = self.llm.invoke([HumanMessage(content=prompt)]).content
                    source = 'knowledge_base'
                else:
                    # 知識庫沒有信息，嘗試網絡搜索
                    web_results = self.web_search.search(user_query, max_results=3)
                    if web_results:
                        web_context = self.web_search.format_results(web_results)
                        prompt = self._create_web_prompt(user_query, web_context)
                        response = self.llm.invoke([HumanMessage(content=prompt)]).content
                        source = 'web_search'
                    else:
                        response = self._generate_fallback_response(user_query)
                        source = 'intrinsic_knowledge'
            else:
                # 使用網絡搜索
                web_results = self.web_search.search(user_query, max_results=3)
                if web_results:
                    web_context = self.web_search.format_results(web_results)
                    prompt = self._create_web_prompt(user_query, web_context)
                    response = self.llm.invoke([HumanMessage(content=prompt)]).content
                    source = 'web_search'
                else:
                    response = self._generate_fallback_response(user_query)
                    source = 'intrinsic_knowledge'
            
            # 過濾回應
            response = self.safety_filter.filter_response(response)
            
            return {
                'response': response,
                'source': source,
                'needs_clarification': False
            }
            
        except Exception as e:
            return {
                'response': f'處理查詢時發生錯誤：{str(e)}',
                'source': 'error',
                'needs_clarification': False
            }
    
    def _create_kb_prompt(self, query: str, context: str) -> str:
        """創建知識庫查詢的提示"""
        return f"""你是一個專業的公司助手，專注於 ZURU Melon 公司。

用戶問題：{query}

相關知識庫內容：
{context}

請根據上述知識庫內容回答用戶的問題。回答要準確、專業，並且只基於提供的知識庫內容。如果知識庫內容不足，可以說明並建議用戶查閱相關文檔或聯繫相關部門。

回答（使用繁體中文）："""
    
    def _create_web_prompt(self, query: str, web_context: str) -> str:
        """創建網絡搜索查詢的提示"""
        return f"""你是一個專業的助手。

用戶問題：{query}

網絡搜索結果：
{web_context}

請根據搜索結果回答用戶的問題。回答要準確、客觀。如果搜索結果不足以回答問題，請誠實說明。

回答（使用繁體中文）："""
    
    def _generate_fallback_response(self, query: str) -> str:
        """生成後備回應（使用內在知識）"""
        prompt = f"""你是一個專業的助手。請回答以下問題。

問題：{query}

如果問題涉及 ZURU Melon 公司的具體政策或程序，請建議用戶查閱公司內部文檔或聯繫相關部門。

回答（使用繁體中文）："""
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)]).content
            return response
        except Exception as e:
            return f'抱歉，我無法回答這個問題。錯誤：{str(e)}'

