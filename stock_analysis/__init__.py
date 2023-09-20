from tradingview_ta import TA_Handler, Interval
import yfinance as yf
import requests
from typing import Union


class TA():
    SCREENER = 'russia'
    EXCHANGE = 'MOEX'
    SYMBOLS = list() 
    RECOMMENDATIONS = ['STRONG_BUY', 'STRONG_SELL']
    last = dict()

    def __init__(self, symbols:Union[str, list]='all', screener:str='russia', 
                 exchange:str='MOEX') -> None:
        self.screener = screener
        self.exchange = exchange
        match symbols:
            case 'all': TA.SYMBOLS = self.get_all_symbols()
            case symbols if type(symbols) is list: TA.SYMBOLS = symbols
            case _: raise ValueError() 
        for add in self.get_analysis():
            TA.last[add.get('symbol')] = {
                    'rec': add.get('rec'),
                    'info': add.get('info'),
                    }


    
    def get_all_symbols(self) -> list|None:
        response = requests.get(
                f'https://scanner.tradingview.com/{self.screener}/scan'
                )
        if response.status_code == 200:
            scan = response.json()
            tickers = scan.get("data")
            if tickers is not None:
                result = list()
                for ticker in tickers:
                    symbol = ticker.get("s")
                    if symbol is not None:
                        symbol = symbol.split(":")[-1]
                        result.append(symbol)
                return result
    
    def get_analysis(self): 
        if TA.SYMBOLS is not None:
            for symbol in TA.SYMBOLS:
                stock_analysis  = TA_Handler(
                        symbol=symbol, 
                        screener=self.screener, 
                        exchange=self.exchange,
                        interval=Interval.INTERVAL_1_DAY
                        )
                recomendation = stock_analysis.get_analysis()
                if recomendation is None:
                    return None
                summary = recomendation.summary
                if summary is None:
                    return None
                rec = summary.get('RECOMMENDATION')
                info = yf.Ticker(symbol)
                yield {'symbol': symbol, 'rec': rec, 'info': info}

    def alert(self):
        if TA.SYMBOLS is not None:
            for symbol in TA.SYMBOLS:
                stock_analysis  = TA_Handler(
                        symbol=symbol, 
                        screener=self.screener, 
                        exchange=self.exchange,
                        interval=Interval.INTERVAL_1_DAY
                        )
                recomendation = stock_analysis.get_analysis()
                if recomendation is None:
                    return None
                summary = recomendation.summary
                if summary is None:
                    return None
                rec = summary.get('RECOMMENDATION')
                last_rec = TA.last.get(symbol)
                if last_rec is not None:
                    info = last_rec.get('info')
                    last_rec = last_rec.get('rec')
                else:
                    info = yf.Ticker(symbol)
                if rec in TA.RECOMMENDATIONS and rec != last_rec:
                    TA.last[symbol] = {'rec': rec, 'info': info}
                    yield {symbol: {'rec': rec, 'info': info}}
         
        

    def __repr__(self):
        return str(
                list(
                    f'{symbol}:{last.get("rec")}' 
                    for symbol, last in TA.last.items()
                    )
                )


