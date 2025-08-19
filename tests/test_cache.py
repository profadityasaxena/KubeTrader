from fastapi.testclient import TestClient
from app.main import app
import redis
import json

client = TestClient(app)
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def test_stock_cache():
    ticker = "AAPL"

    # Clear any previous cache
    redis_client.delete(ticker)

    # First request -> should fetch be from yahoo and cache it
    response1 = client.get(f"/stock/{ticker}")
    assert response1.status_code == 200
    data1 = response1.json()

    # Check Redis has stored it
    cached = redis_client.get(ticker)
    assert cached is not None
    cached_data = json.loads(cached)
    assert cached_data["ticker"] == ticker

    # Second request -> should be served from the cache
    response2 =  client.get(f"/stock/{ticker}")
    assert response2.status_code == 200
    data2 = response2.json()

    assert data2 == data1  # Should be the same as the first response