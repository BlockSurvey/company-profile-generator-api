from fastapi import FastAPI

import config
from controllers.financial_metrics_controller import FinancialMetricsController
from controllers.share_holdings_structure_controller import ShareHoldingsStructureController
from controllers.stock_price_performance_controller import StockPricePerformanceController
from controllers.user_controller import UserController

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    # Create a new instance of UserController
    user_controller = UserController()
    return user_controller.get_user(user_id)

@app.get("/fmp/financial-key-metrics/{symbol}")
def get_financial_key_metrics(symbol: str):
    fmp_controller = FinancialMetricsController()
    return fmp_controller.get_financial_metrics(symbol)

@app.get("/fmp/share-holdings-structure/{symbol}")
def get_share_holdings_structure(symbol: str):
    share_holdings_structure_controller = ShareHoldingsStructureController()
    return share_holdings_structure_controller.get_share_holdings_structure(symbol)

@app.get("/fmp/stock-price-performance/{symbol}")
def get_stock_price_performance(symbol: str):
    stock_price_performance_controller = StockPricePerformanceController()
    return stock_price_performance_controller.get_stock_price_performance(symbol)

@app.get("/")
def read_root():
    # return the status
    return {"status": "ok"}