from datetime import datetime
from google.cloud.firestore_v1.query import Query

class StockMarket:

    def __init__(self, db):
        print(f"\tInicializando submódulo {__name__}")
        self.__db = db
        self.__load_stock_refs()
        print("\tMódulo cargado con éxito")
        
    def setup_stock(self, symbol: str, data: dict):
        """Agregar o renovar la información de una acción a partir de un payload

        Args:
            symbol (str): El símbolo de la acción a agregar/actualizar\n
            data (dict): el payload a subir a firebase, este debe tener la siguiente estructura:\n
            {
                "name": Nombre de la acción
                "market": Mercado en la que la acción se desenvuelve
                "per_stock_price": Precio de la acción al entrar al mercado
                "total_stock_amount": Cantidad de acciones existentes de la compañia
                "current_stock_amount": Cantidad de acciones libres en el marcado (igual que el campo anterior)
                "categories": [] (lista vacía)
                "unique_events": [] (lista vacía)
            }
        """
        
        # Buscar si la acción existe en la lista cacheada de referecias de documentos
        # Si no existe, se crea un documento nuevo      
        try:
            symbol_doc = self.stock_refs[symbol]
            symbol_doc.update(data)
        except KeyError:
            symbol_doc = self.__db.collection("config").document("bot_config").collection("stonks").document(symbol).set(data)
        
        # Volver a cargar la lista cacheada de referecias
        self.__load_stock_refs()
    
    def __load_stock_refs(self) -> None:
        """Método que carga la lista de referecias de documentos de firebase que contienen la info
        de las acciones en una variable local, para facilitar la referencia y minimizar acceso a la db.\n
        Se guarda en la variable de la clase "stock_refs"
        """        
        self.stock_refs = {doc.id: doc for doc in self.__db.collection("config").document("bot_config").collection("stonks").list_documents()}
    
    def get_stock_price(self, symbol: str) -> float:
        """Función que obtiene el precio de una acción en particular

        Args:
            symbol (str): El símbolo de la acción a buscar

        Returns:
            float: El precio de la acción dada
        """
        try:
            stock = self.stock_refs[symbol].get()
            return stock.to_dict()['per_stock_price']
        except KeyError:
            return -1.0
    
    def set_stock_price(self, symbol: str, price: float) -> bool:
        """Función que establece el precio de una acción en particular

        Args:
            symbol (str): El símbolo de la acción en particular
            price (float): El nuevo precio en el que se establecerá la acción

        Returns:
            bool: boleano que determina si la escritura fue válida
        """        
        
        try:
            self.stock_refs[symbol].update({"per_stock_price": price})
            return True
        except KeyError:
            return False

    def price_to_history(self, symbol: str, price: float, change: float) -> bool:
        """Agregar valor actual de acción al histórico de precios

        Args:
            symbol (str): La acción pertinente

        Returns:
            bool: Boleano que determina si la escritura fue correcta
        """
        self.stock_refs[symbol].collection("price_history").add({
                "timestamp": datetime.now(),
                "price": price,
                "change": change,
            })
        return True

    def get_price_history(self, symbol: str, mins: int=360):
        q = self.stock_refs[symbol].collection("price_history").order_by('timestamp', direction=Query.DESCENDING).limit(mins)
        a =  list(q.stream())
        a.reverse()
        return a
    
    def calculate_price_change(self, symbol: str) -> Tuple[float, float]:
        