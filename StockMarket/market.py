class StockMarket:

    def __init__(self, db):
        print(f"Inicializando submódulo {__name__}")
        self.__db = db
        self.stock_refs: list = db.collection("config").document("bot_config").collection("stonks").list_documents()
