from datetime import datetime
from google.cloud.firestore_v1.query import Query
import random
from typing import Tuple

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

    def price_to_history(self, symbol: str, price: float, change: float, free_stock_percent: float) -> bool:
        """Función que agrega el precio dado al histórico de precios de una acción dada

        Args:
            symbol (str): Símbolo de la acción a tratar
            price (float): El precio a agregar al histórico
            change (float): El cambio (en porcentaje) que se aplicó al precio anterior
            free_stock_percent (float): La cantidad de acciones (en porcentaje) que están libres en el mercado

        Returns:
            bool: Si la acción de escribir fue exitosa
        """
        
        self.stock_refs[symbol].collection("price_history").add({
                "timestamp": datetime.now(),
                "price": price,
                "change": change,
                "free_stocks": free_stock_percent
            })
        return True

    def get_price_history(self, symbol: str, mins: int=360) -> Tuple[list, float]:
        """Obtiene el histórico de precios de la acción dada en el periodo de tiempo establecido

        Args:
            symbol (str): El símbolo de la acción a buscar
            mins (int, optional): El tiempo en minutos que se desea ir en el pasado. Default = 360.

        Returns:
            Tuple[list, float]: Una lista de históricos y el cambio total que ocurrió en ese periodo de tiempo
        """                    
        stock = self.stock_refs[symbol].get().to_dict()
        q = self.stock_refs[symbol].collection("price_history").order_by('timestamp', direction=Query.DESCENDING).limit(mins)
        a =  list(q.stream())
        a.reverse()
        try:
            start = a[0].to_dict()["price"]
            closing = stock["per_stock_price"]
            change = closing/start - 1        
            return a, change
        except IndexError:
            return [], 0
    
    def calculate_price_change(self, symbol: str) -> Tuple[float, float, float]:
        """Funcion que calcula aleatoriamente el cambio porcentual de la acción dada

        Args:
            symbol (str): El símbolo de la acción dada

        Returns:
            Tuple[float, float, float]: Tupla que contiene el precio actual, el nuevo precio y el porcentaje de cambio de la acción
        """
        
        stock = self.stock_refs[symbol].get().to_dict()
        history, _ = self.get_price_history(symbol, 1)
        decay_prob = random.random()
        
        # Algoritmo muy primitivo para calcular si la acción sube o baja de precio
        # TODO: Implementar algoritmo basado en precios anteriores
        if decay_prob > 0.5:
            sign = -1
        else:
            sign = 1
            
        # Algoritmo muy primitivo para calcular magnitud del cambio de precios
        # TODO: Implementar algoritmo basado en otras cosas (?)
        magnitude_chance = random.triangular(0,1,0.2)
        
        # Hallar una magnitud de cambion aleatoria
        if magnitude_chance > 0.99:
            change_magnitude = random.uniform(0.1,0.2)
        elif magnitude_chance >= 0.96:
            change_magnitude = random.uniform(0.05,0.1)
        elif magnitude_chance >= 0.93:
            change_magnitude = random.uniform(0.01,0.05)
        else:
            change_magnitude = random.uniform(0.001,0.005)

        # Transformar esa magnitud de cambio según las acciones libres
        # Obtener el porcentaje de acciones que están disponibles en el mercado de
        current_free_stocks = stock["current_stock_amount"]/stock["total_stock_amount"]
        
        # Buscar entre el histórico para ver si el número de acciones libres cambió
        # NOTE: La razón por la que esto está en un for loop es para evitar situaciones en las que la lista esté vacía
        free_change = 1
        for price in history:
            price = price.to_dict()
            if price["free_stocks"] == current_free_stocks:
                free_change = 0.7
            
            # Si las acciones libres disminuyeron, el precio debe aumentar mas (o disminuir menos)
            elif price["free_stocks"] > current_free_stocks:
                percentage = price["free_stocks"] - current_free_stocks
                
                if percentage >= 0.2:
                    free_change += 0.7*sign
                elif percentage > 0.1:
                    free_change += 0.4*sign
                elif percentage > 0.05:
                    free_change += 0.2*sign
                else:
                    free_change += 0.1*sign
            
            # Si las acciones libres aumentaron, el precio debe disminuir mas (o aumentar menos)
            else:
                percentage = current_free_stocks - price["free_stocks"]
                
                if percentage >= 0.2:
                    free_change += 0.7*-sign
                elif percentage > 0.1:
                    free_change += 0.4*-sign
                elif percentage > 0.05:
                    free_change += 0.2*-sign
                else:
                    free_change += 0.1*-sign
            
            change_magnitude *= free_change

        # Calcular el valor final y retornarlo
        new = stock["per_stock_price"] + stock["per_stock_price"]*change_magnitude*sign
        
        return stock["per_stock_price"], new, change_magnitude*sign, current_free_stocks
        
        