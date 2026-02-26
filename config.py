"""
配置模組：管理系統設定和環境變數
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 基礎路徑
BASE_DIR = Path(__file__).parent
KNOWLEDGE_BASE_DIR = BASE_DIR / 'Agents' / 'Knowledge Base'
VECTOR_DB_DIR = BASE_DIR / '.vectordb'

# API 配置
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
OPENROUTER_API_BASE = 'https://openrouter.ai/api/v1'

# 模型配置
EMBEDDING_MODEL = 'text-embedding-3-small'
LLM_MODEL = 'openai/gpt-4o-mini'  # OpenRouter 格式
LLM_TEMPERATURE = 0.7

# 如果使用標準 OpenAI API，使用以下模型名稱
OPENAI_LLM_MODEL = 'gpt-4o-mini'  # 標準 OpenAI 格式

# 向量數據庫配置
VECTOR_DB_COLLECTION_NAME = 'company_knowledge_base'
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# 安全關鍵詞（用於過濾有害內容）
RESTRICTED_KEYWORDS = [
    'hack', 'violence', 'illegal', 'harmful', 'discriminat',
    'explicit', 'offensive', 'threat', 'weapon'
]

