from typing import List
from fastapi import FastAPI, HTTPException, Query
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


class TradeDetails(BaseModel):
    buySellIndicator: str
    price: float
    quantity: int


class Trade(BaseModel):
    asset_class: str = ""
    counterparty: str = ""
    instrument_id: str
    instrument_name: str
    trade_date_time: datetime
    trade_details: TradeDetails
    trade_id: str = ""
    trader: str

    def matches_search(self, search_text: str) -> bool:
        """
        Check if the trade matches the search criteria.

        :param search_text: The text to search for.
        :return: True if the trade matches the search criteria, False otherwise.
        """
        if search_text.lower() in self.counterparty.lower():
            return True
        if search_text.lower() in self.instrument_id.lower():
            return True
        if search_text.lower() in self.instrument_name.lower():
            return True
        if search_text.lower() in self.trader.lower():
            return True
        return False


trades = [
    Trade(
        asset_class="Equity",
        counterparty="HDFC Bank",
        instrument_id="RELIANCE",
        instrument_name="Reliance Industries Ltd.",
        trade_date_time=datetime(2023, 4, 23, 11, 30, 0),
        trade_details=TradeDetails(
            buySellIndicator="BUY", price=1000.0, quantity=100),
        trade_id="1",
        trader="Rajesh"
    ),
    Trade(
        asset_class="Commodity",
        counterparty="SBI Bank",
        instrument_id="GOLD",
        instrument_name="Gold",
        trade_date_time=datetime(2023, 4, 24, 15, 0, 0),
        trade_details=TradeDetails(
            buySellIndicator="SELL", price=3000.0, quantity=10),
        trade_id="2",
        trader="Suresh"
    ),
    Trade(
        asset_class="Currency",
        counterparty="SBI Bank",
        instrument_id="INR",
        instrument_name="Indian Rupee",
        trade_date_time=datetime(2023, 4, 25, 9, 30, 0),
        trade_details=TradeDetails(
            buySellIndicator="BUY", price=2000.0, quantity=1000),
        trade_id="3",
        trader="Amit"
    ),
    Trade(
        asset_class="Stocks",
        counterparty="Kotak Bank",
        instrument_id="NIFTY50",
        instrument_name="Nifty 50 Index",
        trade_date_time=datetime(2023, 4, 26, 14, 0, 0),
        trade_details=TradeDetails(
            buySellIndicator="SELL", price=1500.0, quantity=10),
        trade_id="4",
        trader="Vikram"
    ),
    Trade(
        asset_class="Bond",
        counterparty="Axis Bank",
        instrument_id="SBIN",
        instrument_name="State Bank of India Bond",
        trade_date_time=datetime(2023, 4, 27, 11, 0, 0),
        trade_details=TradeDetails(
            buySellIndicator="BUY", price=1200.0, quantity=100),
        trade_id="5",
        trader="Manish Singh"
    )
]


@app.get("/")
async def root():
    return {"message": "Welcome to my API!"}


@app.get("/trades", response_model=List[Trade])
async def get_trades_search_filter(
    search: Optional[str] = Query(
        None, description="Search for trades by Counterparty, Instrument ID, Instrument name and Trader"),
    assetClass: Optional[str] = Query(
        None, description="Filter by asset class."),
    start: Optional[datetime] = Query(
        None, description="Filter by minimum trade date."),
    end: Optional[datetime] = Query(
        None, description="Filter by maximum trade date."),
    tradeType: Optional[str] = Query(
        None, description="Filter by trade type (BUY or SELL)."),
    minPrice: Optional[float] = Query(
        None, description="Filter by minimum trade price."),
    maxPrice: Optional[float] = Query(
        None, description="Filter by maximum trade price.")
):
    """
    Get a list of trades that match the search criteria (if any) and the filter criteria (if any).
    """
    matching_trades = trades

    if search:
        matching_trades = [
            trade for trade in matching_trades if trade.matches_search(search)]
        if not matching_trades:
            raise HTTPException(
                status_code=404, detail="No trades match the search criteria")

    elif assetClass:
        matching_trades = [
            trade for trade in matching_trades if trade.asset_class == assetClass]
        if not matching_trades:
            raise HTTPException(
                status_code=404, detail="No trades match the assetClass criteria")

    elif tradeType:
        matching_trades = [
            trade for trade in matching_trades if trade.trade_details.buySellIndicator == tradeType]
        if not matching_trades:
            raise HTTPException(
                status_code=404, detail="No trades match the tradeType criteria")

    elif minPrice and maxPrice is not None:
        matching_trades = [
            trade for trade in matching_trades if trade.trade_details.price >= minPrice and trade.trade_details.price <= maxPrice]
        if not matching_trades:
            raise HTTPException(
                status_code=404, detail="No trades match the range criteria")

    elif minPrice is not None:
        matching_trades = [
            trade for trade in matching_trades if trade.trade_details.price >= minPrice]
        if not matching_trades:
            raise HTTPException(
                status_code=404, detail="No trades match the minPrice criteria")

    elif maxPrice is not None:
        matching_trades = [
            trade for trade in matching_trades if trade.trade_details.price <= maxPrice]
        if not matching_trades:
            raise HTTPException(
                status_code=404, detail="No trades match the maxPrice criteria")

    elif start is not None:
        matching_trades = [
            trade for trade in matching_trades if trade.trade_date_time >= start]
        if not matching_trades:
            raise HTTPException(
                status_code=404, detail="No trades match the start criteria")

    elif end is not None:
        matching_trades = [
            trade for trade in matching_trades if trade.trade_date_time <= end]
        if not matching_trades:
            raise HTTPException(
                status_code=404, detail="No trades match the end criteria")

    return matching_trades if matching_trades else trades


@app.get("/trades/{trade_id}", response_model=Trade)
def get_trade_by_id(trade_id: str) -> Trade:
    for trade in trades:
        if trade.trade_id == trade_id:
            return trade
    raise HTTPException(status_code=404, detail="Trade not found")


@app.get("/{path:path}")
async def dont_go_in_invalid_path(path: str):
    return {f"The URL {path} is not valid go to /docs or /trades"}
