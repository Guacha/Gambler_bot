from datetime import datetime
from google.cloud.firestore_v1.query import Query
from google.cloud.firestore_v1.document import DocumentReference
import random
from typing import Tuple
import yfinance as yf
import numpy as np
from scipy.stats import norm
from discord.ext import commands
class Stock:
    """Clase que modela las acciones y tiene los métodos que se usan para obtener información de estas
    """
    
    def __init__(self, symbol: str, price: float, doc_ref: DocumentReference):
        self.__last_update = datetime.now()
        self.symbol = symbol
        self.ticker = yf.Ticker(symbol)
        self.price = price
        self.history = self.get_history(force_update=True)
        self.doc_ref = doc_ref
        
    
    def update_values():
        data = self.doc_ref.get().to_dict()
        
    
    def get_price(self) -> float:
        if (datetime.now() - self.__last_update).min > 1:
            return self.doc_ref.get().to_dict()['per_stock_price']
        else:
            return this
        
    def set_price(self, newprice):
        """Función que establece el precio de la acción en la BD

        Args:
            newprice (float): El nuevo precio en el que se establecerá la acción
        """
        self.doc_ref.update({'per_stock_price': newprice})
    
    def get_free_stocks(self):
        data = self.doc_ref.get().to_dict()
        return data['current_stock_amount']/data['total_stock_amount']
    
    def price_to_history(self, price: float, free_stocks: float):
        self.doc_ref.collection("price_history").add({
                "timestamp": datetime.now(),
                "price": price,
                "free_stocks": free_stocks
        })
        
    def calculate_price_change(self, curr_price: float, free_stocks: float, trials: int=1000) -> float:
        """Esta función es un larguero sin sentido que procesa el histórico de una acción y genera un
        modelo basado en movimiento browniano que le permite al computador generar probabilidades hipotéticas
        para calcular el siguiente precio de una acción, este método es básico en naturaleza y optimizado logarítmicamente
        con el fin de 

        Args:
            curr_price (float): [description]
            trials (int, optional): [description]. Defaults to 1000.

        Returns:
            float: El valor probabilístico calculado
        """        
        data = self.stock.history(period="5d", interval="1m", prepost=True) 
        log_return = np.log(1 + data["Close"].pct_change())
        u = log_return.mean()
        var = log_return.var()
        drift = u - (0.5*var)
        stdev = log_return.std()
        z = norm.ppf(np.random.rand(trials))
        disr = np.exp(drift + stdev * z)
        possible_prices = curr_price*disr*(1/(np.sqrt(free_stocks)+4) + 0.8)
        return np.random.choice(possible_prices)
    
    def advance_time(self):
        curr_price = self.get_price()
        free_stocks = self.cache_docget_free_stocks()
        self.price_to_history(curr_price, free_stocks)
        new_price = self.calculate_price_change(curr_price)
        self.set_price(new_price)
    
    def get_history(self, start_date=dt.datetime.combine(dt.date.today(), dt.datetime.min.time()), end_date):
        """Obtiene el histórico de precios de la acción dada en el periodo de tiempo establecido

        Args:
            mins (int, optional): El tiempo en minutos que se desea ir en el pasado. Default = 360.

        Returns:
            Tuple[list, float]: Una lista de históricos y el cambio total que ocurrió en ese periodo de tiempo
        """
        q = self.doc_ref.collection("price_history").order_by('timestamp', direction=Query.DESCENDING).limit(mins)
        a =  list(q.stream())
        a.reverse()
        try:
            start = a[0].to_dict()["price"]
            closing = self.doc_ref.get().to_dict()["per_stock_price"]
            change = closing/start - 1        
            return a, change
        except IndexError:
            return [], 0
    
    class StockMarket(commands.Cog):
    
        def __init__(self, db):
            self.__db = db
            self.stocks = {}
            docs = self.__db.collection("config").document("bot_config").collection("stonks").get()
            for doc in docs:
                data = doc.to_dict()
                stonk = Stock(doc.id, data["per_stock_price"], doc.reference)
                self.stocks[doc.id] = stonk