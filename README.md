# InsightForge （還在完善中 Still under development.）

這是一個基於 Agent 的資料智慧系統，能自動讀取多來源資料、進行結構化分析，並生成視覺化洞察。系統整合 LLM 驅動的推理能力、工具調用與自動圖表生成，以支援智慧決策。

## 功能特色

- 📚 **知識庫檢索**：搜索公司政策、編碼標準和程序
- 🌐 **網絡搜索**：訪問外部和最新信息
- 💡 **智能路由**：自動選擇最佳數據源
- 📊 **數據分析與視覺化**：自動生成分析圖表（直方圖、箱型圖、散點圖、相關性熱力圖）
- 🛡️ **安全與合規**：過濾有害內容並確保政策合規
- 💬 **CLI 界面**：用戶友好的命令行界面

## 目錄

- [系統需求](#系統需求)
- [安裝與配置](#安裝與配置)
- [環境設定](#環境設定)
- [使用指南](#使用指南)
- [查詢範例](#查詢範例)
- [被禁止的內容](#被禁止的內容)
- [系統架構](#系統架構)
- [故障排除](#故障排除)
- [專案結構](#專案結構)
- [授權](#授權)

## 系統需求

- **Python**：3.8 或更高版本
- **作業系統**：Windows / Linux / macOS
- **API 金鑰**：OpenAI API 金鑰或 OpenRouter API 金鑰

## 安裝與配置

### 步驟 1：克隆或下載專案

```bash
# 如果使用 git
git clone <repository-url>
cd Agents_eng

# 或下載並解壓縮專案文件
```

### 步驟 2：創建虛擬環境（強烈推薦）

創建虛擬環境可以避免與系統套件發生衝突。

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

啟動後，命令提示字元應該會顯示 `(venv)`。

### 步驟 3：安裝依賴

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

安裝過程會下載並安裝以下套件：
- `openai` - OpenAI API 客戶端
- `langchain` - LLM 框架
- `langchain-openai` - LangChain 的 OpenAI 整合
- `langchain-community` - 社群整合
- `chromadb` - 向量數據庫
- `rich` - 終端機格式化
- `duckduckgo-search` - 網絡搜索
- `python-dotenv` - 環境變數管理
- `matplotlib` - 圖表繪製
- `seaborn` - 統計圖表美化
- `pandas` - 數據處理和分析
- 以及其他依賴項...

**注意**：首次安裝可能需要幾分鐘時間。

### 步驟 4：配置 API 金鑰

在專案根目錄創建 `.env` 文件：

**選項 1：使用 OpenRouter（測試推薦）**
```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

**選項 2：使用 OpenAI API**
```env
OPENAI_API_KEY=your_openai_api_key_here
```

**重要提示**：
- 可以在 [openrouter.ai](https://openrouter.ai) 獲取 OpenRouter API 金鑰（新用戶提供 $5 信用額度）
- OpenAI API 請訪問 [platform.openai.com](https://platform.openai.com)
- 確保 API 金鑰有足夠的額度
- 切勿將 `.env` 文件提交到版本控制系統

### 步驟 5：驗證安裝

執行以下命令檢查是否安裝成功：

```bash
python -c "import langchain; import chromadb; import openai; print('安裝成功！')"
```

## 環境設定

### 環境變數

系統使用以下環境變數（在 `.env` 文件中設定）：

| 變數名稱 | 說明 | 必填 |
|----------|------|------|
| `OPENROUTER_API_KEY` | OpenRouter API 金鑰 | 是（如果不使用 OpenAI） |
| `OPENAI_API_KEY` | OpenAI API 金鑰 | 是（如果不使用 OpenRouter） |

**優先順序**：如果同時提供兩個金鑰，系統會優先使用 OpenRouter API。

### 知識庫文件

系統會自動載入 `Agents/Knowledge Base/` 目錄中的 Markdown 文件：
- `Coding Style.md` - 編碼標準和風格指南
- `Company Policies.md` - 公司政策和規定
- `Company Procedures & Guidelines.md` - 程序和指南

您可以在此目錄中添加更多 Markdown 文件來擴展知識庫。系統會在首次運行時自動索引這些文件。

## 使用指南

### 啟動系統

1. **導航到專案目錄：**
```bash
cd Agents_eng
```

2. **啟動虛擬環境（如果尚未啟動）：**
```bash
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

3. **運行 CLI：**
```bash
python cli.py
```

您應該會看到歡迎訊息和使用說明。

### 基本操作

#### 1. 提問

系統啟動後，只需輸入您的問題並按 Enter：

```
您: 公司的編碼風格是什麼？
```

系統會：
1. 檢查查詢是否安全（安全過濾器）
2. 判斷適當的數據源
3. 檢索相關信息
4. 生成並顯示回應

#### 2. 查看回應

回應會以格式化的面板顯示，包含：
- **回應內容**（Markdown 格式）
- **來源標籤**，指示信息來源：
  - 📚 **知識庫** - 來自公司文件的信息
  - 🌐 **網絡搜索** - 來自網絡搜索的信息
  - 💡 **內在知識** - 來自 AI 訓練數據的信息
  - 📊 **數據分析** - 來自數據分析模組的信息
  - 🚫 **安全過濾** - 查詢已被阻止
- **圖表文件**：如果查詢生成了圖表，會顯示圖表保存路徑

#### 3. 數據分析與圖表生成

系統支持對加密貨幣數據進行分析和視覺化。您可以通過自然語言查詢或 CLI 命令來生成圖表。

**自然語言查詢範例：**
```
您: 請畫出 market_cap 跟 market_cap_rank 的關係
您: 畫出 current_price 的分佈圖
您: 請生成相關性熱力圖
您: 繪製市值與交易量的散點圖
```

**CLI 命令模式：**
```
您: crypto info                    # 查看數據集概要
您: crypto columns                 # 列出所有欄位名稱
您: crypto suggest current_price   # 獲取欄位分析建議
您: crypto plot hist current_price # 繪製直方圖
您: crypto plot box market_cap     # 繪製箱型圖
您: crypto plot scatter market_cap total_volume  # 繪製散點圖
```

**支持的圖表類型：**
- **直方圖（Histogram）**：觀察單一數值欄位的分佈
- **箱型圖（Boxplot）**：觀察中位數、四分位數和異常值
- **散點圖（Scatter Plot）**：觀察兩個數值欄位之間的關係
- **相關性熱力圖（Correlation Heatmap）**：視覺化所有數值欄位之間的相關係數

**圖表輸出：**
- 所有圖表會自動保存為 PNG 格式
- 圖表文件保存在 `Agents/Database/crypto_plots/` 目錄
- 系統會在回應中顯示圖表的完整路徑

#### 4. 特殊命令

| 命令 | 說明 |
|------|------|
| `help` | 顯示幫助信息 |
| `quit` 或 `exit` | 退出程序 |
| `Ctrl+C` | 中斷當前查詢或退出 |
| `crypto help` | 顯示數據分析相關命令幫助 |

### 回應時間

- **知識庫查詢**：通常 2-5 秒
- **網絡搜索查詢**：通常 5-10 秒
- **複雜查詢**：可能需要 10-15 秒

## 查詢範例

### 1. 公司相關查詢

**編碼標準：**
```
您: 公司的編碼風格是什麼？
您: 根據公司標準，我應該如何格式化 Python 代碼？
您: 變數的命名規範是什麼？
```

**公司政策：**
```
您: 公司有哪些政策？
您: 著裝規範政策是什麼？
您: 關於工作時間有什麼規定？
```

**程序：**
```
您: 請假的流程是什麼？
您: 我該如何申請休假？
您: 報告問題的程序是什麼？
```

### 2. 一般知識查詢

**技術問題：**
```
您: 什麼是 RAG 技術？
您: 解釋向量數據庫的工作原理
您: Python 的最新功能有哪些？
```

**外部信息：**
```
您: Python 的當前版本是什麼？
您: Docker 是如何工作的？
您: API 設計的最佳實踐是什麼？
```

### 3. 數據分析與圖表生成查詢

**自然語言圖表查詢：**
```
您: 請畫出 market_cap 跟 market_cap_rank 的關係
您: 畫出 current_price 的分佈圖
您: 請生成相關性熱力圖
您: 繪製市值與交易量的散點圖
您: 畫出價格變動百分比的箱型圖
您: 給我分析建議，哪些欄位應該一起分析
```

**CLI 命令查詢：**
```
您: crypto info
您: crypto columns
您: crypto suggest current_price market_cap
您: crypto plot hist current_price
您: crypto plot box price_change_percentage_24h
您: crypto plot scatter market_cap total_volume
```

### 4. 複雜查詢（結合多個來源）

```
您: 根據公司編碼風格，我應該如何使用 Python 類型提示？
您: 公司關於數據隱私的政策是什麼，以及行業最佳實踐是什麼？
您: 解釋 API 設計原則以及它們如何符合我們的編碼標準
```

### 5. 更好的查詢技巧

- **具體明確**：「公司的遠程工作政策是什麼？」比「遠程工作」更好
- **使用上下文**：對於公司相關問題，提及「公司」或「內部」
- **一次一個問題**：複雜的多部分問題可能效果不佳
- **使用自然語言**：系統理解對話式查詢
- **圖表查詢**：可以直接說「畫出...的關係」或「繪製...的分佈」，系統會自動識別欄位和圖表類型
- **欄位名稱**：支持英文欄位名稱（如 `market_cap`）和中文別名（如「市值」）

## 被禁止的內容

系統會自動阻止違反公司政策或包含有害內容的查詢。了解這些限制有助於您適當地提出問題。

### 1. 限制關鍵詞

以下關鍵詞（或變體）會觸發安全過濾器：

| 類別 | 關鍵詞 |
|------|--------|
| **安全相關** | hack（駭客）、bypass（繞過）、security breach（安全漏洞） |
| **暴力相關** | violence（暴力）、weapon（武器）、threat（威脅） |
| **非法活動** | illegal（非法）、unlawful（違法） |
| **有害內容** | harmful（有害）、dangerous（危險） |
| **歧視性內容** | discriminatory（歧視性）、discrimination（歧視）、bias（偏見） |
| **不當內容** | explicit（露骨）、offensive（冒犯性） |

**注意**：系統使用模式匹配（不區分大小寫），因此變體如 "hacking"、"bypassing" 也會被阻止。

### 2. 政策違規內容

以下特定政策違規模式會被阻止：

- **數據洩露**：關於洩露客戶數據、分享機密信息的查詢
- **安全繞過**：嘗試繞過安全措施、忽略安全協議
- **不道德行為**：不道德行為的指示
- **歧視性內容**：包含歧視性語言的查詢
- **非法活動**：關於非法活動的查詢

### 3. 繞過安全機制嘗試

系統會檢測並阻止嘗試繞過安全檢查的行為：

- `ignore policy`（忽略政策）
- `bypass rules`（繞過規則）
- `ignore security`（忽略安全）
- `skip safety`（跳過安全檢查）

### 為什麼要限制這些內容？

1. **法律合規**：防止生成非法或法律問題內容
2. **公司政策**：確保符合公司政策和倫理規範
3. **安全性**：防止安全漏洞和系統濫用
4. **專業環境**：在企業環境中維持適當使用

### 內容被阻止時會發生什麼？

當查詢被阻止時：
1. 系統立即停止處理
2. 顯示安全過濾訊息
3. 來源標記為「🚫 安全過濾」
4. 不生成回應

**範例：**
```
您: 如何駭入系統
🚫 安全過濾: 抱歉，查詢包含不當內容，違反公司政策。
```

## 系統架構

### 核心組件

1. **RAG 系統 (`rag_system.py`)**
   - 管理向量數據庫（ChromaDB）
   - 處理文檔嵌入和檢索
   - 使用 OpenAI embeddings 進行語義搜索
   - 支持文檔分塊和相似度檢索

2. **Agent 系統 (`agent.py`)**
   - 智能查詢路由
   - 多源數據整合
   - 上下文感知回應生成
   - 查詢分類和來源選擇

3. **網絡搜索 (`web_search.py`)**
   - DuckDuckGo 整合用於外部搜索
   - 結果格式化和排序
   - 優雅處理搜索錯誤

4. **安全過濾 (`safety_filter.py`)**
   - 查詢內容驗證
   - 回應內容過濾
   - 政策合規驗證
   - 關鍵詞模式匹配

5. **CLI 界面 (`cli.py`)**
   - 用戶互動界面
   - Rich 終端格式化
   - 回應顯示和格式化
   - 命令處理

6. **數據分析模組 (`crypto_analysis.py`)**
   - 加密貨幣數據讀取和處理
   - 自然語言查詢解析
   - 多種圖表類型生成（直方圖、箱型圖、散點圖、相關性熱力圖）
   - 數據欄位說明和建議
   - 相關性分析和統計

### 工作原理

1. **查詢輸入**：用戶通過 CLI 輸入查詢
2. **安全檢查**：安全過濾器驗證查詢
3. **來源選擇**：Agent 判斷適當的數據源
4. **信息檢索**：
   - 公司查詢：搜索知識庫
   - 一般查詢：搜索網絡或使用內在知識
   - 數據分析查詢：解析自然語言並生成圖表
5. **回應生成**：LLM 基於檢索的上下文生成回應，或直接生成圖表文件
6. **回應過濾**：安全過濾器檢查回應
7. **顯示**：格式化的回應顯示給用戶，包含圖表路徑（如果適用）

### RAG (Retrieval-Augmented Generation)

系統使用 RAG 技術增強回應準確性：

1. **文檔處理**：
   - Markdown 文件分割成塊（1000 字符，200 重疊）
   - OpenAI embeddings 生成向量表示
   - 向量存儲在 ChromaDB 中

2. **檢索過程**：
   - 用戶查詢轉換為向量
   - 相似度搜索找到相關文檔塊
   - 檢索的上下文與查詢一起發送給 LLM

3. **生成過程**：
   - LLM 基於檢索的上下文生成回應
   - 確保準確性並基於實際文檔內容

## 故障排除

### 常見問題

#### 1. API 金鑰錯誤

**問題**：`Authentication error` 或 `Invalid API key`

**解決方案**：
- 確認 `.env` 文件存在且包含正確的 API 金鑰
- 檢查 API 金鑰是否有足夠的額度
- 確保 `.env` 文件中沒有多餘的空格或引號
- 嘗試重新生成 API 金鑰
- 對於 OpenRouter，請在 openrouter.ai 檢查帳戶狀態

#### 2. 向量數據庫錯誤

**問題**：`Vector database error` 或 `Collection not found`

**解決方案**：
- 刪除 `.vectordb` 目錄並重新啟動（系統會重建）
- 檢查磁碟空間可用性
- 驗證專案目錄的寫入權限
- 首次運行會自動創建數據庫（可能需要時間）

#### 3. 網絡搜索失敗

**問題**：`Web search error` 或沒有網絡結果

**解決方案**：
- 檢查網絡連接
- DuckDuckGo 服務可能暫時不可用
- 幾分鐘後重試
- 如果網絡搜索失敗，系統會回退到內在知識

#### 4. 依賴安裝失敗

**問題**：`pip install` 失敗或套件衝突

**解決方案**：
- 確保已安裝 Python 3.8+：`python --version`
- 升級 pip：`pip install --upgrade pip`
- 使用虛擬環境（推薦）
- 嘗試單獨安裝套件以識別衝突
- 在 Windows 上，某些套件可能需要 Visual C++ Build Tools

#### 5. 模組導入錯誤

**問題**：`ModuleNotFoundError` 或 `ImportError`

**解決方案**：
- 確保虛擬環境已啟動
- 重新安裝依賴：`pip install -r requirements.txt`
- 檢查 Python 路徑和虛擬環境設置

#### 6. 性能緩慢

**問題**：查詢時間過長

**解決方案**：
- 檢查網絡連接（對於網絡搜索）
- API 速率限制可能導致延遲（等待幾秒）
- 向量數據庫首次運行較慢（後續運行更快）
- 大型知識庫需要更長的處理時間

#### 7. 圖表生成錯誤

**問題**：`找不到欄位` 或 `圖表生成失敗`

**解決方案**：
- 確認數據文件 `Agents/Database/top_250_crypto_20251222.csv` 存在
- 使用 `crypto columns` 命令查看所有可用欄位名稱
- 確認欄位名稱拼寫正確（區分大小寫）
- 檢查 `Agents/Database/crypto_plots/` 目錄的寫入權限
- 確保已安裝 `matplotlib` 和 `seaborn`：`pip install matplotlib seaborn`

### 獲取幫助

如果您遇到此處未涵蓋的問題：
1. 仔細檢查錯誤訊息
2. 確認所有安裝步驟都已遵循
3. 確保 API 金鑰有效且有額度
4. 檢查系統日誌（如果可用）


## 專案結構

```
Agents_eng/
├── Agents/
│   ├── Knowledge Base/              # 公司知識庫文件
│   │   ├── Coding Style.md
│   │   ├── Company Policies.md
│   │   └── Company Procedures & Guidelines.md
│   └── Database/                    # 數據文件目錄
│       ├── top_250_crypto_20251222.csv  # 加密貨幣數據集
│       └── crypto_plots/            # 圖表輸出目錄（自動生成）
├── Agent_Assignment/                # 作業文檔
│   └── Agent assignment.md
├── .vectordb/                       # 向量數據庫（自動生成）
├── venv/                            # 虛擬環境（如果已創建）
├── config.py                        # 配置模組
├── rag_system.py                    # RAG 系統實現
├── agent.py                         # Agent 系統
├── crypto_analysis.py               # 數據分析與圖表生成模組
├── web_search.py                    # 網絡搜索模組
├── safety_filter.py                 # 安全和合規過濾器
├── cli.py                           # CLI 界面
├── requirements.txt                 # Python 依賴項
├── .env                             # 環境變數（需創建此文件）
├── README.md                        # 英文文檔
├── README_zh.md                     # 本文件（中文文檔）
└── 使用說明.md                      # 詳細使用說明（繁體中文）
```

## 文檔

- **English**: [README.md](README.md)
- **繁體中文**: 本文件 (README_zh.md)
- **詳細使用說明（繁體中文）**: [使用說明.md](使用說明.md)

## 版本信息

- **版本**：1.0.0
- **Python 需求**：3.8+
- **最後更新**：2025

---

**感謝使用 ZURU Melon 公司助手！**
