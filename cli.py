"""
CLI 用戶界面模組
"""
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from agent import CompanyAssistantAgent
from crypto_analysis import CryptoDataExplorer


class CLI:
    """
    命令行界面：提供互動式用戶體驗
    """
    
    def __init__(self):
        """初始化 CLI"""
        self.console = Console()
        self.agent = CompanyAssistantAgent()
        self.crypto_explorer = CryptoDataExplorer()
        self._print_welcome()
    
    def _print_welcome(self):
        """打印歡迎訊息"""
        welcome_text = """
# ZURU Melon 公司助手

歡迎使用 AI 公司助手！我可以幫助您：

- 回答關於公司政策、程序和編碼風格的問題
- 提供外部知識和最新信息
- **加密貨幣數據分析**：使用自然語言查詢分析 top_250_crypto_20251222.csv
  - 例如：「請畫出 market_cap 跟 market_cap_rank 的關係」
  - 例如：「給我分析建議，哪些欄位應該一起分析」
  - 例如：「畫出相關性熱力圖」

輸入 'quit' 或 'exit' 退出，輸入 'help' 查看幫助。
        """
        self.console.print(Panel(Markdown(welcome_text), title='歡迎', border_style='green'))
    
    def _print_help(self):
        """打印幫助信息"""
        help_text = """
## 使用說明

1. **公司相關問題**：直接詢問關於公司政策、程序、編碼風格等問題
   - 例如：「公司的編碼風格是什麼？」
   - 例如：「請假的流程是什麼？」

2. **一般知識問題**：詢問外部知識或最新信息
   - 例如：「什麼是 RAG？」
   - 例如：「最新的 Python 版本是什麼？」

3. **加密貨幣數據分析（top_250_crypto_20251222.csv）**：
   
   **自然語言查詢（推薦）**：
   - 「請畫出 market_cap 跟 market_cap_rank 的關係」
   - 「畫出 current_price 的直方圖」
   - 「給我分析建議，哪些欄位應該一起分析」
   - 「畫出相關性熱力圖」
   - 「請畫出市值與交易量的散點圖」
   
   **指令模式（進階）**：
   - `crypto info`：查看數據集概要與欄位說明
   - `crypto columns`：只列出所有欄位名稱
   - `crypto suggest <欄位1> [欄位2]`：根據一個或兩個欄位給出建議圖表類型
   - `crypto plot hist <欄位>`：繪製直方圖
   - `crypto plot box <欄位>`：繪製箱型圖
   - `crypto plot scatter <欄位X> <欄位Y>`：繪製散點圖

4. **退出**：輸入 'quit' 或 'exit' 退出程序

5. **幫助**：輸入 'help' 查看此幫助信息
        """
        self.console.print(Panel(Markdown(help_text), title='幫助', border_style='blue'))
    
    def run(self):
        """運行 CLI 主循環"""
        while True:
            try:
                # 獲取用戶輸入
                user_input = Prompt.ask('\n[bold cyan]您[/bold cyan]', default='').strip()
                
                if not user_input:
                    continue
                
                # 處理特殊命令（保留指令模式以向後兼容）
                if user_input.lower().startswith('crypto '):
                    self._handle_crypto_command(user_input)
                    continue
                
                if user_input.lower() in ['quit', 'exit', '退出']:
                    self.console.print('\n[green]感謝使用，再見！[/green]')
                    break
                
                if user_input.lower() in ['help', '幫助']:
                    self._print_help()
                    continue
                
                # 處理查詢
                self.console.print('\n[dim]思考中...[/dim]')
                result = self.agent.query(user_input)
                
                # 顯示回應
                self._display_response(result)
                
            except KeyboardInterrupt:
                self.console.print('\n\n[yellow]程序被中斷[/yellow]')
                break
            except Exception as e:
                self.console.print(f'\n[red]錯誤：{str(e)}[/red]')
    
    def _handle_crypto_command(self, command: str):
        """處理與加密貨幣數據集相關的指令"""
        parts = command.strip().split()
        if len(parts) == 1 or parts[1].lower() in ['help', '幫助']:
            help_text = """
## Crypto 數據指令說明

- **crypto info**：顯示數據集簡要說明與所有欄位解釋
- **crypto columns**：僅列出欄位名稱
- **crypto suggest <欄位1> [欄位2]**：根據欄位關係建議適合的圖表類型
- **crypto plot hist <欄位>**：為指定欄位繪製直方圖
- **crypto plot box <欄位>**：為指定欄位繪製箱型圖
- **crypto plot scatter <欄位X> <欄位Y>**：繪製兩個欄位之間的散點圖

圖檔會輸出到 `Agents/Database/crypto_plots/` 目錄中。
            """
            self.console.print(Panel(Markdown(help_text), title='Crypto 數據幫助', border_style='magenta'))
            return
        
        action = parts[1].lower()
        
        try:
            if action == 'info':
                summary = self.crypto_explorer.describe_dataset()
                self.console.print(Panel(Markdown(summary), title='Crypto 數據概要', border_style='magenta'))
            
            elif action == 'columns':
                cols = self.crypto_explorer.get_columns()
                text = "## 欄位名稱\n\n" + "\n".join(f"- **{c}**" for c in cols)
                self.console.print(Panel(Markdown(text), title='Crypto 欄位列表', border_style='magenta'))
            
            elif action == 'suggest':
                if len(parts) < 3:
                    self.console.print('[red]請提供至少一個欄位名稱，例如：crypto suggest current_price market_cap[/red]')
                    return
                col_x = parts[2]
                col_y = parts[3] if len(parts) >= 4 else None
                suggestions = self.crypto_explorer.suggest_plots(col_x, col_y)
                text = "## 圖表建議\n\n" + "\n\n".join(suggestions)
                self.console.print(Panel(Markdown(text), title='Crypto 圖表建議', border_style='magenta'))
            
            elif action == 'plot':
                if len(parts) < 4:
                    self.console.print('[red]用法：crypto plot <hist|box|scatter> ...[/red]')
                    return
                plot_type = parts[2].lower()
                
                if plot_type in ['hist', 'histogram']:
                    column = parts[3]
                    result = self.crypto_explorer.plot_histogram(column)
                elif plot_type in ['box', 'boxplot']:
                    column = parts[3]
                    result = self.crypto_explorer.plot_boxplot(column)
                elif plot_type in ['scatter']:
                    if len(parts) < 5:
                        self.console.print('[red]散點圖用法：crypto plot scatter <欄位X> <欄位Y>[/red]')
                        return
                    x, y = parts[3], parts[4]
                    result = self.crypto_explorer.plot_scatter(x, y)
                else:
                    self.console.print(f"[red]未知的圖表類型：{plot_type}，請使用 hist / box / scatter。[/red]")
                    return
                
                text = f"## 圖表已產生\n\n- **輸出檔案**：`{result.path}`\n\n{result.description}"
                self.console.print(Panel(Markdown(text), title='Crypto 圖表結果', border_style='magenta'))
            
            else:
                self.console.print(f"[red]未知的 crypto 子命令：{action}，輸入 `crypto help` 查看用法。[/red]")
        
        except Exception as e:
            self.console.print(f"[red]處理 crypto 指令時發生錯誤：{str(e)}[/red]")
    
    def _display_response(self, result: dict):
        """顯示回應結果"""
        response = result.get('response', '')
        source = result.get('source', 'unknown')
        plot_path = result.get('plot_path', None)
        
        # 根據來源設置顏色
        source_colors = {
            'knowledge_base': 'green',
            'web_search': 'blue',
            'intrinsic_knowledge': 'yellow',
            'safety_filter': 'red',
            'error': 'red',
            'crypto_analysis': 'magenta'
        }
        color = source_colors.get(source, 'white')
        
        # 來源標籤
        source_labels = {
            'knowledge_base': '📚 知識庫',
            'web_search': '🌐 網絡搜索',
            'intrinsic_knowledge': '💡 內在知識',
            'safety_filter': '🚫 安全過濾',
            'error': '❌ 錯誤',
            'crypto_analysis': '📊 加密貨幣數據分析'
        }
        source_label = source_labels.get(source, '❓ 未知')
        
        # 如果有圖表路徑，在回應中強調顯示
        if plot_path:
            response += f"\n\n**📁 圖表已儲存至**：`{plot_path}`"
        
        # 顯示回應
        self.console.print('\n')
        self.console.print(
            Panel(
                Markdown(response),
                title=f'[bold {color}]{source_label}[/bold {color}]',
                border_style=color
            )
        )


def main():
    """主函數"""
    cli = CLI()
    cli.run()


if __name__ == '__main__':
    main()

