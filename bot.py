from DB_Control import db
from StockMarket.market import StockMarket
import json

stonks = StockMarket(db)

with open("dump.json") as file:
    dump = json.load(file)
    for symbol, info in dump.items():
        payload = {
            "name": info['name'],
            "market": info['market'],
            "website": info['website'],
            "total_stock_amount": info["vol"],
            "per_stock_price": info["per_stock_price"]
        }
        stonks.setup_stock(symbol, payload)


    
    