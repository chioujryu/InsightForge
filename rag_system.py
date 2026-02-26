"""
RAG 系統模組：處理知識庫檢索增強生成
"""
import os
from pathlib import Path
from typing import List, Dict
import chromadb
from chromadb.config import Settings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document
import config


class RAGSystem:
    """
    RAG 系統：管理知識庫的向量化和檢索
    """
    
    def __init__(self):
        """初始化 RAG 系統"""
        self.knowledge_base_dir = config.KNOWLEDGE_BASE_DIR
        self.vector_db_dir = config.VECTOR_DB_DIR
        self.vector_db_dir.mkdir(exist_ok=True)
        
        # 初始化嵌入模型
        # 注意：OpenRouter 主要用於 LLM，embeddings 通常使用 OpenAI API
        api_key = config.OPENAI_API_KEY or config.OPENROUTER_API_KEY
        
        self.embeddings = OpenAIEmbeddings(
            model=config.EMBEDDING_MODEL,
            openai_api_key=api_key
        )
        
        # 初始化向量數據庫
        self.vectorstore = self._initialize_vectorstore()
    
    def _initialize_vectorstore(self) -> Chroma:
        """
        初始化向量數據庫，如果不存在則創建
        
        Returns:
            Chroma: 向量數據庫實例
        """
        persist_directory = str(self.vector_db_dir)
        
        # 檢查是否已存在向量數據庫
        if (self.vector_db_dir / 'chroma.sqlite3').exists():
            # 載入現有的向量數據庫
            return Chroma(
                persist_directory=persist_directory,
                embedding_function=self.embeddings,
                collection_name=config.VECTOR_DB_COLLECTION_NAME
            )
        else:
            # 創建新的向量數據庫
            return self._build_knowledge_base()
    
    def _build_knowledge_base(self) -> Chroma:
        """
        從知識庫文件建立向量數據庫
        
        Returns:
            Chroma: 向量數據庫實例
        """
        # 載入所有 Markdown 文件
        loader = DirectoryLoader(
            str(self.knowledge_base_dir),
            glob='**/*.md',
            loader_cls=TextLoader,
            loader_kwargs={'encoding': 'utf-8'}
        )
        
        documents = loader.load()
        
        if not documents:
            raise ValueError(f'未找到知識庫文件於 {self.knowledge_base_dir}')
        
        # 分割文檔
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            length_function=len,
        )
        
        splits = text_splitter.split_documents(documents)
        
        # 建立向量數據庫
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            persist_directory=str(self.vector_db_dir),
            collection_name=config.VECTOR_DB_COLLECTION_NAME
        )
        
        return vectorstore
    
    def search(self, query: str, k: int = 3) -> List[Dict]:
        """
        在知識庫中搜索相關文檔
        
        Args:
            query: 搜索查詢
            k: 返回的結果數量
            
        Returns:
            List[Dict]: 相關文檔列表，每個包含 content 和 metadata
        """
        try:
            # 使用相似度搜索
            docs = self.vectorstore.similarity_search_with_score(query, k=k)
            
            results = []
            for doc, score in docs:
                results.append({
                    'content': doc.page_content,
                    'metadata': doc.metadata,
                    'score': float(score)
                })
            
            return results
        except Exception as e:
            print(f'搜索錯誤: {e}')
            return []
    
    def get_relevant_context(self, query: str, max_tokens: int = 2000) -> str:
        """
        獲取相關上下文，用於生成回應
        
        Args:
            query: 用戶查詢
            max_tokens: 最大 token 數量（粗略估計）
            
        Returns:
            str: 相關上下文文本
        """
        results = self.search(query, k=5)
        
        context_parts = []
        current_length = 0
        
        for result in results:
            content = result['content']
            # 粗略估計：1 token ≈ 4 字符
            content_tokens = len(content) // 4
            
            if current_length + content_tokens > max_tokens:
                break
            
            context_parts.append(content)
            current_length += content_tokens
        
        return '\n\n'.join(context_parts)

