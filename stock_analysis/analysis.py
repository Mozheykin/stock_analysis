from tradingview_ta import TA_Handler



class TA(TA_Handler):
    def __init__(self, symbol:str, interval="1D"):
        self.ta = super().__init__(symbol=symbol, interval=interval)

