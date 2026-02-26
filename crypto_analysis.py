"""
加密貨幣數據分析模組：
- 讀取 Agents/Database/top_250_crypto_20251222.csv
- 提供欄位解釋
- 產生常見分析圖表（直方圖、箱型圖、散點圖、相關性熱力圖）
- 支持自然語言查詢解析
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


DATA_PATH = os.path.join("Agents", "Database", "top_250_crypto_20251222.csv")
PLOT_DIR = os.path.join("Agents", "Database", "crypto_plots")


@dataclass
class PlotResult:
    """圖表結果資訊"""

    path: str
    description: str


class CryptoDataExplorer:
    """
    提供對 top_250_crypto_20251222.csv 的高階操作介面。
    """

    def __init__(self, data_path: str = DATA_PATH) -> None:
        self.data_path = data_path
        self._df: Optional[pd.DataFrame] = None
        os.makedirs(PLOT_DIR, exist_ok=True)

    # -------- 資料存取與欄位資訊 --------
    def load_data(self) -> pd.DataFrame:
        """讀取 CSV 並快取 DataFrame。"""
        if self._df is None:
            self._df = pd.read_csv(self.data_path)
        return self._df

    def get_columns(self) -> List[str]:
        """回傳所有欄位名稱。"""
        df = self.load_data()
        return list(df.columns)

    def get_column_descriptions(self) -> Dict[str, str]:
        """
        回傳欄位說明。
        （依據 Kaggle dataset 說明與欄位名稱推斷）
        """
        return {
            "id": "幣種在數據來源中的唯一識別 ID（例如 CoinGecko 的 id）。",
            "symbol": "加密貨幣交易代碼（例如 BTC、ETH）。",
            "name": "加密貨幣名稱（例如 Bitcoin、Ethereum）。",
            "current_price": "當前價格（估計為美元計價）。",
            "market_cap": "市值（價格 × 流通供給量）。",
            "market_cap_rank": "按市值排序的名次（1 代表市值最高）。",
            "total_volume": "24 小時交易量。",
            "high_24h": "過去 24 小時內的最高價。",
            "low_24h": "過去 24 小時內的最低價。",
            "price_change_percentage_24h": "過去 24 小時價格變動百分比。",
            "circulating_supply": "目前在市場上流通的代幣數量。",
            "last_updated": "數據最後更新時間（時間戳記）。",
        }

    def describe_dataset(self) -> str:
        """
        回傳資料集的簡要文字說明與欄位摘要（用於在 CLI 中顯示）。
        """
        df = self.load_data()
        col_desc = self.get_column_descriptions()

        lines: List[str] = []
        lines.append("### 加密貨幣市場快照數據集概要")
        lines.append("")
        lines.append(f"- **總幣種數量**: {len(df)}")
        lines.append(f"- **欄位數量**: {len(df.columns)}")
        lines.append("")
        lines.append("#### 欄位說明")

        for col in df.columns:
            desc = col_desc.get(col, "（暫無說明）")
            lines.append(f"- **{col}**: {desc}")

        return "\n".join(lines)

    # -------- 圖表建議 --------
    def suggest_plots(
        self, col_x: str, col_y: Optional[str] = None
    ) -> List[str]:
        """
        根據欄位型態與是否為單變量 / 雙變量，給出建議圖表類型。
        回傳人類可讀的建議列表。
        """
        df = self.load_data()
        if col_x not in df.columns:
            return [f"找不到欄位 **{col_x}**，請確認名稱是否正確。"]
        if col_y is not None and col_y not in df.columns:
            return [f"找不到欄位 **{col_y}**，請確認名稱是否正確。"]

        suggestions: List[str] = []
        numeric_cols = df.select_dtypes(include="number").columns

        if col_y is None:
            # 單一欄位
            if col_x in numeric_cols:
                suggestions.append(
                    f"對 **{col_x}** 建議：\n"
                    "- 繪製 **直方圖** 觀察分佈。\n"
                    "- 繪製 **箱型圖** 觀察中位數與極端值。"
                )
            else:
                suggestions.append(
                    f"對 **{col_x}** 建議：\n"
                    "- 繪製 **長條圖** 看不同類別的計數或平均值（目前模組著重數值圖表，如有需要可再擴充）。"
                )
        else:
            # 兩個欄位
            both_numeric = col_x in numeric_cols and col_y in numeric_cols
            if both_numeric:
                corr = df[[col_x, col_y]].corr().iloc[0, 1]
                suggestions.append(
                    f"對 **{col_x}** 與 **{col_y}** 建議：\n"
                    "- 繪製 **散點圖** 觀察兩者關係。\n"
                    "- 視需要可加上 **回歸線**（目前先提供基本散點圖）。\n"
                    f"- 兩者皮爾森相關係數約為 **{corr:.3f}**（僅供參考）。"
                )
            else:
                suggestions.append(
                    f"對 **{col_x}** 與 **{col_y}** 建議：\n"
                    "- 若其中一個為類別、一個為數值，可考慮畫 **箱型圖（數值對不同類別）**。\n"
                    "- 目前模組主要支援數值對數值的散點圖，如需更多類別分析可再擴充。"
                )

        return suggestions

    # -------- 圖表繪製 --------
    def _build_output_path(self, name: str) -> str:
        """組出圖檔輸出路徑。"""
        filename = f"{name}.png"
        return os.path.join(PLOT_DIR, filename)

    def plot_histogram(self, column: str) -> PlotResult:
        """針對單一數值欄位繪製直方圖。"""
        df = self.load_data()
        if column not in df.columns:
            raise ValueError(f"找不到欄位: {column}")

        plt.figure(figsize=(10, 6))
        sns.histplot(df[column].dropna(), kde=True)
        plt.title(f"{column} 直方圖")
        plt.xlabel(column)
        plt.ylabel("頻數")
        plt.tight_layout()

        output_path = self._build_output_path(f"hist_{column}")
        plt.savefig(output_path)
        plt.close()

        return PlotResult(
            path=output_path,
            description=f"已產生 **{column}** 的直方圖，檔案路徑：`{output_path}`。",
        )

    def plot_boxplot(self, column: str) -> PlotResult:
        """針對單一數值欄位繪製箱型圖。"""
        df = self.load_data()
        if column not in df.columns:
            raise ValueError(f"找不到欄位: {column}")

        plt.figure(figsize=(8, 6))
        sns.boxplot(x=df[column].dropna())
        plt.title(f"{column} 箱型圖")
        plt.xlabel(column)
        plt.tight_layout()

        output_path = self._build_output_path(f"box_{column}")
        plt.savefig(output_path)
        plt.close()

        return PlotResult(
            path=output_path,
            description=f"已產生 **{column}** 的箱型圖，檔案路徑：`{output_path}`。",
        )

    def plot_scatter(self, x: str, y: str) -> PlotResult:
        """繪製兩個數值欄位之間的散點圖。"""
        df = self.load_data()
        for col in (x, y):
            if col not in df.columns:
                raise ValueError(f"找不到欄位: {col}")

        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x=x, y=y)
        plt.title(f"{x} 與 {y} 的散點圖")
        plt.xlabel(x)
        plt.ylabel(y)
        plt.tight_layout()

        output_path = self._build_output_path(f"scatter_{x}_vs_{y}")
        plt.savefig(output_path)
        plt.close()

        return PlotResult(
            path=output_path,
            description=(
                f"已產生 **{x}** 與 **{y}** 的散點圖，檔案路徑：`{output_path}`。"
            ),
        )

    def plot_correlation_heatmap(self) -> PlotResult:
        """繪製所有數值欄位的相關係數熱力圖。"""
        df = self.load_data()
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        
        if len(numeric_cols) < 2:
            raise ValueError("需要至少兩個數值欄位才能繪製相關性熱力圖")

        # 計算相關係數矩陣
        corr_matrix = df[numeric_cols].corr()

        # 繪製熱力圖
        plt.figure(figsize=(12, 10))
        sns.heatmap(
            corr_matrix,
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            center=0,
            square=True,
            linewidths=1,
            cbar_kws={"shrink": 0.8},
        )
        plt.title("加密貨幣數據欄位相關係數熱力圖", fontsize=14, pad=20)
        plt.tight_layout()

        output_path = self._build_output_path("correlation_heatmap")
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        return PlotResult(
            path=output_path,
            description=f"已產生相關係數熱力圖，檔案路徑：`{output_path}`。",
        )

    def get_correlation_analysis(self) -> str:
        """
        分析所有數值欄位之間的相關性，並提供分析建議。
        
        Returns:
            str: 相關性分析報告（Markdown 格式）
        """
        df = self.load_data()
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        
        if len(numeric_cols) < 2:
            return "需要至少兩個數值欄位才能進行相關性分析。"

        corr_matrix = df[numeric_cols].corr()

        lines: List[str] = []
        lines.append("## 相關性分析報告")
        lines.append("")

        # 找出強相關的欄位對（|r| > 0.7）
        strong_correlations: List[Tuple[str, str, float]] = []
        for i, col1 in enumerate(numeric_cols):
            for j, col2 in enumerate(numeric_cols):
                if i < j:  # 避免重複
                    corr_value = corr_matrix.loc[col1, col2]
                    if abs(corr_value) > 0.7:
                        strong_correlations.append((col1, col2, corr_value))

        if strong_correlations:
            lines.append("### 強相關關係（|相關係數| > 0.7）")
            lines.append("")
            # 按相關係數絕對值排序
            strong_correlations.sort(key=lambda x: abs(x[2]), reverse=True)
            for col1, col2, corr in strong_correlations:
                direction = "正相關" if corr > 0 else "負相關"
                lines.append(f"- **{col1}** 與 **{col2}**：{corr:.3f}（{direction}）")
            lines.append("")

        # 找出中等相關的欄位對（0.3 < |r| <= 0.7）
        moderate_correlations: List[Tuple[str, str, float]] = []
        for i, col1 in enumerate(numeric_cols):
            for j, col2 in enumerate(numeric_cols):
                if i < j:
                    corr_value = corr_matrix.loc[col1, col2]
                    if 0.3 < abs(corr_value) <= 0.7:
                        moderate_correlations.append((col1, col2, corr_value))

        if moderate_correlations:
            lines.append("### 中等相關關係（0.3 < |相關係數| <= 0.7）")
            lines.append("")
            moderate_correlations.sort(key=lambda x: abs(x[2]), reverse=True)
            for col1, col2, corr in moderate_correlations[:10]:  # 只顯示前10個
                direction = "正相關" if corr > 0 else "負相關"
                lines.append(f"- **{col1}** 與 **{col2}**：{corr:.3f}（{direction}）")
            lines.append("")

        # 分析建議
        lines.append("### 分析建議")
        lines.append("")
        lines.append("基於相關性分析，建議您分析以下欄位組合：")
        lines.append("")

        # 建議強相關的組合
        if strong_correlations:
            lines.append("#### 強相關組合（建議優先分析）")
            for col1, col2, corr in strong_correlations[:5]:
                lines.append(f"- **{col1} vs {col2}**：相關係數 {corr:.3f}")
                lines.append(f"  - 建議圖表：散點圖（scatter plot）")
                if corr > 0.8 or corr < -0.8:
                    lines.append(f"  - 注意：這兩個欄位高度相關，可能存在數學關係或因果關係")
            lines.append("")

        # 建議中等相關的組合
        if moderate_correlations:
            lines.append("#### 中等相關組合（值得探索）")
            for col1, col2, corr in moderate_correlations[:5]:
                lines.append(f"- **{col1} vs {col2}**：相關係數 {corr:.3f}")
                lines.append(f"  - 建議圖表：散點圖（scatter plot）")
            lines.append("")

        lines.append("### 如何查看完整相關性矩陣")
        lines.append("")
        lines.append("您可以執行 `plot correlation` 來生成相關係數熱力圖，視覺化所有欄位之間的相關性。")

        return "\n".join(lines)

    def parse_natural_language_query(self, query: str) -> Optional[Dict[str, any]]:
        """
        解析自然語言查詢，識別要繪製的圖表類型和欄位。
        
        Args:
            query: 自然語言查詢，例如「請畫出 market_cap 跟 market_cap_rank 的關係」
            
        Returns:
            Dict 包含 'plot_type', 'columns' 等資訊，如果無法解析則返回 None
        """
        query_lower = query.lower()
        df = self.load_data()
        all_columns = df.columns.tolist()
        
        # 欄位名稱映射（支持中文和英文）
        column_aliases = {
            "價格": "current_price",
            "市值": "market_cap",
            "排名": "market_cap_rank",
            "交易量": "total_volume",
            "24小時交易量": "total_volume",
            "最高價": "high_24h",
            "最低價": "low_24h",
            "價格變動": "price_change_percentage_24h",
            "價格變動百分比": "price_change_percentage_24h",
            "流通供給量": "circulating_supply",
            "流通量": "circulating_supply",
        }
        
        # 找出查詢中提到的欄位
        found_columns = []
        
        # 先檢查完整欄位名稱
        for col in all_columns:
            if col.lower() in query_lower:
                found_columns.append(col)
        
        # 再檢查別名
        for alias, col_name in column_aliases.items():
            if alias in query_lower and col_name not in found_columns:
                found_columns.append(col_name)
        
        # 如果找不到欄位，返回 None
        if not found_columns:
            return None
        
        # 識別圖表類型
        plot_type = None
        if any(word in query_lower for word in ["散點圖", "scatter", "關係", "相關", "vs", "對"]):
            plot_type = "scatter"
        elif any(word in query_lower for word in ["直方圖", "histogram", "hist", "分佈", "分布"]):
            plot_type = "histogram"
        elif any(word in query_lower for word in ["箱型圖", "boxplot", "box", "箱線圖"]):
            plot_type = "boxplot"
        elif any(word in query_lower for word in ["相關性", "correlation", "corr", "熱力圖", "heatmap"]):
            plot_type = "correlation"
        
        # 如果沒有明確指定圖表類型，根據欄位數量推斷
        if plot_type is None:
            if len(found_columns) == 1:
                plot_type = "histogram"  # 單欄位預設直方圖
            elif len(found_columns) >= 2:
                plot_type = "scatter"  # 多欄位預設散點圖
        
        result = {
            "plot_type": plot_type,
            "columns": found_columns[:2] if plot_type in ["scatter", "correlation"] else found_columns[:1],
        }
        
        return result


