from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config
from controllers.company_management_controller import CompanyManagementController
from controllers.company_overview_controller import CompanyOverviewController
from controllers.company_stock_details_controller import CompanyStockDetailsController
from controllers.company_summary_controller import CompanySummaryController
from controllers.financial_metrics_controller import FinancialMetricsController
from controllers.share_holdings_structure_controller import ShareHoldingsStructureController
from controllers.stock_price_performance_controller import StockPricePerformanceController
from controllers.user_controller import UserController

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

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

@app.get("/company-summary/{company_name}")
def get_company_summary(company_name: str):
    company_summary_controller = CompanySummaryController()
    return company_summary_controller.get_company_summary(company_name)

@app.get("/company-management/{company_name}")
def get_company_management(company_name: str):
    company_management_controller = CompanyManagementController()
    return company_management_controller.get_company_management(company_name)

@app.get("/company-stock-details/{company_name}")
def get_company_stock_details(company_name: str):
    company_stock_details_controller = CompanyStockDetailsController()
    return company_stock_details_controller.get_company_stock_details(company_name)

@app.get("/company-overview/{company_name}")
def get_company_overview(company_name: str):
    company_overview_controller = CompanyOverviewController()
    return company_overview_controller.get_company_overview(company_name)

@app.get("/")
def read_root():
    # return the status
    return {"status": "ok"}