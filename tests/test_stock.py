from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_stock_price():
    response = client.get("/stock/AAPL")
    assert response.status_code == 200
    data = response.json()
    # basic shape checks
    assert "ticker" in data
    assert "price" in data
    assert data["ticker"] == "AAPL"
    assert isinstance(data["price"], (float, int))
