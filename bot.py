from DB_Control import db
from StockMarket.market import StockMarket
import json

stonks = StockMarket(db)

# TODO: Agregar las categorías a Firebase
# NOTE: Esta funcion es temporal, y solo cumple el propósito del setup inicial

categories = ("tech",           # 0
              "mobile",         # 1
              "computer",       # 2
              "hardware",       # 3
              "software",       # 4
              "automotive",     # 5
              "mechanical",     # 6
              "pharma",         # 7
              "entertainment",  # 8
              "business",       # 9
              "gaming",         # 10
              "shopping",       # 11
              "finance",        # 12
              "social",         # 13
              "electric",       # 14
              "enterprise",     # 15
              "cosmetics",      # 16
              "food",           # 17
              "industry",       # 18
              "telecom",        # 19
            )
with open("dump.json") as file:
    dump = json.load(file)
    for symbol, info in dump.items():
        cats = input(f"Categorías de {info['name']}: ")
        list_cats = [categories[int(i)] for i in cats.split(",")]
        payload = {
            "name": info['name'],
            "market": info['market'],
            "website": info['website'],
            "total_stock_amount": info["vol"],
            "per_stock_price": info["per_stock_price"],
            "categories": list_cats,
        }
        stonks.setup_stock(symbol, payload)


    
    