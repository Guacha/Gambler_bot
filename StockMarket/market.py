from google.cloud.firestore_v1.document import DocumentReference

class StockMarket:

    def __init__(self, db):
        print(f"\tInicializando submódulo {__name__}")
        self.__db = db
        self.load_stock_refs()
        print("\tMódulo cargado con éxito")
    
        
    def setup_stock(self, symbol: str, data: dict):
        try:
            symbol_doc = self.stock_refs[symbol]
            symbol_doc.update(data)
        except KeyError:
            symbol_doc = self.__db.collection("config").document("bot_config").collection("stonks").document(symbol).set(data)
        
        self.load_stock_refs()
    
    
    def load_stock_refs(self) -> "dict[str:DocumentReference]":
        self.stock_refs = {doc.id: doc for doc in self.__db.collection("config").document("bot_config").collection("stonks").list_documents()}
    
    
    def get_stock_price(self, symbol: str) -> float:
        stock = self.stock_refs[symbol].get()
        return stock.to_dict()['per_stock_price']
        