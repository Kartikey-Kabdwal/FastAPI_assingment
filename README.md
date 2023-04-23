# FastAPI_assingment

This API provides access to a list of trades, with filtering and search capabilities.

## Requirements

- Python 3.9 or later
- FastAPI
- Pydantic

## Usage

1. Clone the repository: `git clone https://github.com/your-username/trade-api.git`
2. Install the dependencies: `pip install -r requirements.txt`
3. Start the server: `uvicorn main:app --reload`
4. Open your web browser and go to [http://localhost:8000](http://localhost:8000) to access the API documentation (provided by Swagger UI).

### Endpoints

#### `GET /`

Returns a welcome message.

#### `GET /trades`

Returns a list of trades that match the search criteria (if any) and the filter criteria (if any).

##### Query parameters

- `search` (optional): search for trades by Counterparty, Instrument ID, Instrument name and Trader.
- `assetClass` (optional): filter by asset class.
- `start` (optional): filter by minimum trade date.
- `end` (optional): filter by maximum trade date.
- `tradeType` (optional): filter by trade type (BUY or SELL).
- `minPrice` (optional): filter by minimum trade price.
- `maxPrice` (optional): filter by maximum trade price.

#### `GET /trades/{id}`

Returns a  trades with id number.
