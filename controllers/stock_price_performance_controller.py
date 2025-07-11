import os
import yfinance as yf

class StockPricePerformanceController:
    def __init__(self):
        pass

    def get_stock_price_performance(self, symbol: str):
        # Get stock data using yfinance
        df = yf.download(symbol, period="3y", interval="1d", auto_adjust=True)

        # Check if data was downloaded successfully
        if df.empty:
            print(f"No data found for symbol {symbol}")
            exit()

        # Convert DataFrame to JSON format suitable for charts
        chart_data = {
            "labels": [date.strftime("%Y-%m-%d") for date in df.index],
            "datasets": [
                {
                    "label": f"{symbol} Stock Price",
                    "data": df['Close'].values.tolist(),  # Use .values.tolist() instead of .tolist()
                    "borderColor": "#2563eb",
                    "backgroundColor": "rgba(37, 99, 235, 0.1)",
                    "fill": True
                }
            ]
        }

        index_symbol = "^GSPC" # Relevant index for the stock
        # Get the index data
        index_df = yf.download(index_symbol, period="3y", interval="1d", auto_adjust=True)

        # Check if index data was downloaded successfully
        if index_df.empty:
            raise ValueError(f"No data found for index {index_symbol}. Please check the symbol and try again.")

        # index chart data
        index_chart_data = {
            "labels": [date.strftime("%Y-%m-%d") for date in index_df.index],
            "datasets": [
                {
                    "label": f"{index_symbol} Index Price",
                    "data": index_df['Close'].values.tolist(),
                    "borderColor": "#2563eb",
                    "backgroundColor": "rgba(37, 99, 235, 0.1)",
                    "fill": True
                }
            ]
        }

        chart_data = {
            "stock": chart_data,
            "index": index_chart_data
        }

        return chart_data