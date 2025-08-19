from fastapi import FastAPI, HTTPException
import yfinance as yf
import redis
import json
import os

# Connect to Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/stock/{ticker}")
def get_stock_price(ticker: str):
    try:
        ticker = ticker.upper()

        # Check cache
        cached_value = redis_client.get(ticker)
        if cached_value:
            return json.loads(cached_value)

        # Fetch from Yahoo
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")

        if hist.empty:
            raise HTTPException(status_code=404, detail="Ticker not found or no data")

        latest_price = hist["Close"].iloc[-1]
        response = {"ticker": ticker, "price": float(latest_price)}

        # Save to Redis with a TTL (e.g., 60 seconds)
        redis_client.setex(ticker, 60, json.dumps(response))

        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
