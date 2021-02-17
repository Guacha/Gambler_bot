from google.cloud.firestore_v1.document import DocumentReference

class StockMarket:

    def __init__(self, db):
        print(f"\tInicializando submódulo {__name__}")
        self.__db = db
        self.stock_refs: "dict[str:DocumentReference]" = {doc.id: doc for doc in db.collection("config").document("bot_config").collection("stonks").list_documents()}
        print("\tMódulo cargado con éxito")
        
    def setup_stock(self, symbol: str, data: dict):
    
        symbol_doc = self.stock_refs[symbol]
        symbol_doc.update(data)