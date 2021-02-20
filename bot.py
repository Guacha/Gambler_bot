import DB_Control
from StockMarket.market import StockMarket

db = DB_Control.initialise_database()
stonks = StockMarket(db)
    