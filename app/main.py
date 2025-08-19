from fastapi import FastAPI, HTTPException
import yfinance as yf

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/stock/{ticker}")
def get_stock_price(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")
        if hist.empty:
            raise HTTPException(status_code=404, detail="Ticker not found or no data")
        latest_price = hist["Close"].iloc[-1]
        return {"ticker": ticker.upper(), "price": float(latest_price)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
