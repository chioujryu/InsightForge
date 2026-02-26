# 加密貨幣市場快照數據集 (Top 250 Crypto 2025-12-22)

## 數據集概述

本數據集包含 2025 年 12 月 22 日時，市值排名前 250 名的加密貨幣市場快照數據。數據來源參考 Kaggle 數據集：Cryptocurrency Market Snapshot - Top 250 Coins。

**數據文件位置**：`Agents/Database/top_250_crypto_20251222.csv`

**數據集規模**：
- 總記錄數：250 筆（代表 250 種加密貨幣）
- 欄位數量：12 個欄位
- 數據類型：包含數值型、字串型和時間戳記型數據

---

## 欄位詳細說明

### 1. id (字串型)
- **欄位名稱**：`id`
- **數據類型**：String (str)
- **說明**：加密貨幣在數據來源平台（如 CoinGecko）中的唯一識別符。通常為小寫字母和連字符組成的標識碼。
- **範例值**：`bitcoin`, `ethereum`, `tether`
- **用途**：用於唯一識別每種加密貨幣，可作為主鍵使用。

### 2. symbol (字串型)
- **欄位名稱**：`symbol`
- **數據類型**：String (str)
- **說明**：加密貨幣的交易代碼，通常為 2-5 個大寫字母的縮寫。這是市場上最常用的識別符號。
- **範例值**：`BTC`, `ETH`, `USDT`, `BNB`
- **用途**：快速識別加密貨幣，常用於交易平台和市場報價。

### 3. name (字串型)
- **欄位名稱**：`name`
- **數據類型**：String (str)
- **說明**：加密貨幣的完整名稱。
- **範例值**：`Bitcoin`, `Ethereum`, `Tether`, `BNB`
- **用途**：提供加密貨幣的正式名稱，便於理解。

### 4. current_price (浮點數型)
- **欄位名稱**：`current_price`
- **數據類型**：Float (float64)
- **說明**：加密貨幣的當前價格，以美元（USD）計價。這是數據快照時的即時價格。
- **單位**：美元 (USD)
- **範例值**：`90107.0` (Bitcoin), `3054.47` (Ethereum)
- **用途**：了解當前市場價格，是投資決策的重要參考指標。
- **分析建議**：
  - 可繪製直方圖觀察價格分佈
  - 可與 market_cap 繪製散點圖觀察價格與市值的關係
  - 可與 price_change_percentage_24h 繪製散點圖觀察價格與變動率的關係

### 5. market_cap (浮點數型)
- **欄位名稱**：`market_cap`
- **數據類型**：Float (float64)
- **說明**：市值（Market Capitalization），計算方式為 `current_price × circulating_supply`。代表該加密貨幣的總市場價值。
- **單位**：美元 (USD)
- **範例值**：`1799491440213` (Bitcoin，約 1.8 兆美元)
- **用途**：衡量加密貨幣的市場規模和重要性，是排名的主要依據。
- **分析建議**：
  - 與 market_cap_rank 有強負相關（排名越高，市值越大，但 rank 數字越小）
  - 可繪製直方圖觀察市值分佈（通常呈現長尾分佈）
  - 可與 total_volume 繪製散點圖觀察市值與交易量的關係
  - 可與 current_price 繪製散點圖觀察價格與市值的關係

### 6. market_cap_rank (整數型)
- **欄位名稱**：`market_cap_rank`
- **數據類型**：Integer (int64)
- **說明**：按市值排序的排名，1 代表市值最高的加密貨幣，數字越小代表市值越大。
- **範圍**：1 到 250（本數據集中）
- **範例值**：`1` (Bitcoin), `2` (Ethereum), `3` (Tether)
- **用途**：快速了解加密貨幣在市場中的地位。
- **分析建議**：
  - 與 market_cap 有強負相關（Spearman 相關係數接近 -1）
  - 可繪製長條圖或箱型圖觀察排名分佈
  - 可與 price_change_percentage_24h 繪製散點圖觀察排名與價格變動的關係

### 7. total_volume (浮點數型)
- **欄位名稱**：`total_volume`
- **數據類型**：Float (float64)
- **說明**：過去 24 小時內的總交易量，以美元計價。代表該時段內所有交易的總金額。
- **單位**：美元 (USD)
- **範例值**：`31855493113.0` (Bitcoin，約 318 億美元)
- **用途**：衡量市場流動性和交易活躍度。
- **分析建議**：
  - 通常與 market_cap 有正相關（市值越大，交易量通常也越大）
  - 可繪製直方圖觀察交易量分佈
  - 可與 market_cap 繪製散點圖觀察市值與交易量的關係
  - 可與 price_change_percentage_24h 繪製散點圖觀察交易量與價格變動的關係

### 8. high_24h (浮點數型)
- **欄位名稱**：`high_24h`
- **數據類型**：Float (float64)
- **說明**：過去 24 小時內的最高價格，以美元計價。
- **單位**：美元 (USD)
- **範例值**：`90096.0` (Bitcoin)
- **用途**：了解過去 24 小時的價格波動範圍上限。
- **分析建議**：
  - 可與 current_price 和 low_24h 一起分析，計算價格波動幅度
  - 可繪製箱型圖觀察 24 小時價格區間的分佈

### 9. low_24h (浮點數型)
- **欄位名稱**：`low_24h`
- **數據類型**：Float (float64)
- **說明**：過去 24 小時內的最低價格，以美元計價。
- **單位**：美元 (USD)
- **範例值**：`87655.0` (Bitcoin)
- **用途**：了解過去 24 小時的價格波動範圍下限。
- **分析建議**：
  - 可與 current_price 和 high_24h 一起分析，計算價格波動幅度
  - 可計算 `(high_24h - low_24h) / current_price` 作為波動率指標

### 10. price_change_percentage_24h (浮點數型)
- **欄位名稱**：`price_change_percentage_24h`
- **數據類型**：Float (float64)
- **說明**：過去 24 小時內價格變動的百分比。正值表示上漲，負值表示下跌。
- **單位**：百分比 (%)
- **範例值**：`1.41837` (Bitcoin，表示上漲 1.42%), `-0.01186` (Tether，表示下跌 0.01%)
- **用途**：衡量短期價格變動趨勢，是投資者關注的重要指標。
- **分析建議**：
  - 可繪製直方圖觀察價格變動百分比的分佈（通常接近常態分佈）
  - 可繪製箱型圖識別異常變動的幣種
  - 可與 market_cap 繪製散點圖觀察市值與價格變動的關係
  - 可與 total_volume 繪製散點圖觀察交易量與價格變動的關係

### 11. circulating_supply (浮點數型)
- **欄位名稱**：`circulating_supply`
- **數據類型**：Float (float64)
- **說明**：目前在市場上流通的代幣數量。這是實際可用於交易的代幣總數，不包括被鎖定或未發行的代幣。
- **單位**：代幣數量（無單位）
- **範例值**：`19965496.0` (Bitcoin，約 1997 萬枚), `120695004.1126167` (Ethereum，約 1.2 億枚)
- **用途**：計算市值的重要組成部分，也影響代幣的稀缺性。
- **分析建議**：
  - 與 current_price 和 market_cap 有數學關係：`market_cap = current_price × circulating_supply`
  - 可繪製直方圖觀察流通供給量的分佈
  - 可與 current_price 繪製散點圖觀察供給量與價格的關係

### 12. last_updated (字串型/時間戳記型)
- **欄位名稱**：`last_updated`
- **數據類型**：String (str)，格式為 `YYYY-MM-DD HH:MM`
- **說明**：數據最後更新的時間戳記。
- **格式**：`2025-12-22 12:23`
- **範例值**：`2025-12-22 12:23`
- **用途**：確認數據的新鮮度和時效性。
- **注意**：本數據集為單一時點快照，所有記錄的 last_updated 時間應該相同或接近。

---

## 欄位之間的關係

### 數學關係
1. **市值計算公式**：
   ```
   market_cap = current_price × circulating_supply
   ```
   這是一個嚴格的數學關係，可用於數據驗證。

### 統計相關性關係

#### 強相關關係（建議分析）
1. **market_cap 與 market_cap_rank**：
   - 關係類型：強負相關（Spearman 相關係數接近 -1）
   - 原因：排名是根據市值排序的
   - 建議圖表：散點圖（會呈現明顯的負相關趨勢）

2. **market_cap 與 total_volume**：
   - 關係類型：通常為正相關
   - 原因：市值大的幣種通常交易量也較大
   - 建議圖表：散點圖（可能呈現對數關係）

3. **current_price 與 market_cap**：
   - 關係類型：正相關，但關係複雜（受 circulating_supply 影響）
   - 原因：價格是市值的組成部分
   - 建議圖表：散點圖（可能呈現非線性關係）

#### 中等相關關係
4. **total_volume 與 price_change_percentage_24h**：
   - 關係類型：可能為正相關或無明顯關係
   - 原因：高交易量可能伴隨較大的價格波動
   - 建議圖表：散點圖

5. **market_cap 與 price_change_percentage_24h**：
   - 關係類型：可能為弱負相關
   - 原因：大市值幣種價格變動通常較小（更穩定）
   - 建議圖表：散點圖

#### 價格區間關係
6. **high_24h、low_24h 與 current_price**：
   - 關係類型：current_price 應該在 high_24h 和 low_24h 之間
   - 建議分析：計算波動幅度 `(high_24h - low_24h) / current_price`

---

## 數據類型總結

### 數值型欄位（可用於統計分析和圖表）
- `current_price` (float64)
- `market_cap` (float64)
- `market_cap_rank` (int64)
- `total_volume` (float64)
- `high_24h` (float64)
- `low_24h` (float64)
- `price_change_percentage_24h` (float64)
- `circulating_supply` (float64)

### 字串型欄位（用於標識和分類）
- `id` (str)
- `symbol` (str)
- `name` (str)
- `last_updated` (str)

---

## 分析建議

### 適合單變量分析的欄位（直方圖、箱型圖）
1. **current_price**：觀察價格分佈，通常呈現長尾分佈（少數幣種價格極高）
2. **market_cap**：觀察市值分佈，通常呈現極度長尾分佈
3. **price_change_percentage_24h**：觀察價格變動分佈，可能接近常態分佈
4. **total_volume**：觀察交易量分佈
5. **circulating_supply**：觀察供給量分佈

### 適合雙變量分析的欄位組合（散點圖）
1. **market_cap vs market_cap_rank**：強負相關，適合驗證數據一致性
2. **market_cap vs total_volume**：觀察市值與流動性的關係
3. **current_price vs market_cap**：觀察價格與市值的關係
4. **total_volume vs price_change_percentage_24h**：觀察交易量與價格變動的關係
5. **market_cap vs price_change_percentage_24h**：觀察市值大小與價格穩定性的關係

### 相關性分析建議
建議計算所有數值型欄位之間的相關係數矩陣，並繪製熱力圖（heatmap）來視覺化：
- 識別強相關的欄位對（|r| > 0.7）
- 識別弱相關或無關的欄位對（|r| < 0.3）
- 發現意外的相關關係

---

## 數據品質注意事項

1. **缺失值**：某些幣種可能缺少部分欄位數據（如 high_24h、low_24h），分析時需處理缺失值。
2. **異常值**：市值和價格可能包含極端值（如 Bitcoin 的市值遠高於其他幣種），建議使用對數尺度或分層分析。
3. **數據時效性**：本數據集為單一時點快照，不適合時間序列分析。
4. **單位一致性**：所有價格和市值相關欄位均以美元計價，單位一致。

---

## 參考資料

- **Kaggle 數據集**：https://www.kaggle.com/datasets/nudratabbas/cryptocurrency-market-snapshot-top-250-coins/data
- **數據來源平台**：CoinGecko（推測）
- **數據快照時間**：2025-12-22

---

## 使用範例

### Python 讀取數據
```python
import pandas as pd

# 讀取數據
df = pd.read_csv('Agents/Database/top_250_crypto_20251222.csv')

# 查看基本資訊
print(df.info())
print(df.describe())

# 查看欄位
print(df.columns.tolist())
```

### 分析範例
```python
# 計算相關係數
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
correlation_matrix = df[numeric_cols].corr()
print(correlation_matrix)

# 繪製散點圖：market_cap vs market_cap_rank
import matplotlib.pyplot as plt
plt.scatter(df['market_cap_rank'], df['market_cap'])
plt.xlabel('Market Cap Rank')
plt.ylabel('Market Cap')
plt.title('Market Cap vs Rank')
plt.show()
```
