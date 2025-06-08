def get_current_features1():
    import requests
    import apimoex
    import pandas as pd
    import logging
    import os
    from copy import deepcopy

    from pandas import DataFrame

    from tinkoff.invest import Client, SecurityTradingStatus
    from tinkoff.invest.services import InstrumentsService
    from tinkoff.invest.utils import quotation_to_decimal

    from datetime import timedelta

    from tinkoff.invest import CandleInterval, Client
    from tinkoff.invest.utils import now

    import warnings
    warnings.filterwarnings("ignore")

    TOKEN = 't.YbAt3ov-iNU4jt9A4l9ML4ga77xB1z_NYKOFEvZZDRv72ilghDUEJVk3B86XRSCeyNz5_do2Go_cAqj2qjH9Jg'

    def get_all_quotes_info( figi_series , ticker_series):


        total_quotes = {}

        counter = 0 
        for figi , ticker in zip(figi_series , ticker_series):
            if figi != 0 : 
                with Client(TOKEN) as client:

                    quotes = {'open' : [] , 'high' : [] , 'low' : [] , 'close' : [] , 'volume' : [] , 'datetime' : [] }
                    for candle in client.get_all_candles( figi=figi, from_=now() - timedelta(days= 30), interval=CandleInterval.CANDLE_INTERVAL_1_MIN):

                        open = candle.open.units + candle.open.nano / 1000000000
                        quotes['open'].append(open)

                        high = candle.high.units + candle.high.nano / 1000000000
                        quotes['high'].append(high)

                        low = candle.low.units + candle.low.units / 1000000000
                        quotes['low'].append(low)

                        close = candle.close.units + candle.close.nano / 1000000000
                        quotes['close'].append(close)

                        volume = candle.volume
                        quotes['volume'].append(volume)


                        datetime = candle.time
                        quotes['datetime'].append(datetime)

                        

                    quotes = pd.DataFrame(quotes)


                    total_quotes[ticker] = quotes

                
            else: 
                continue 

        return total_quotes
    
    def get_figi_by_ticker(ticker):

        with Client(TOKEN) as client:
            instruments: InstrumentsService = client.instruments
            tickers = []
            for method in ["shares", "bonds", "etfs", "currencies", "futures"]:
                for item in getattr(instruments, method)().instruments:
                    tickers.append(
                        {
                            "name": item.name,
                            "ticker": item.ticker,
                            "class_code": item.class_code,
                            "figi": item.figi,
                            "uid": item.uid,
                            "type": method,
                            "min_price_increment": quotation_to_decimal(
                                item.min_price_increment
                            ),
                            "scale": 9 - len(str(item.min_price_increment.nano)) + 1,
                            "lot": item.lot,
                            "trading_status": str(
                                SecurityTradingStatus(item.trading_status).name
                            ),
                            "api_trade_available_flag": item.api_trade_available_flag,
                            "currency": item.currency,
                            "exchange": item.exchange,
                            "buy_available_flag": item.buy_available_flag,
                            "sell_available_flag": item.sell_available_flag,
                            "short_enabled_flag": item.short_enabled_flag,
                            "klong": quotation_to_decimal(item.klong),
                            "kshort": quotation_to_decimal(item.kshort),
                        }
                    )

            tickers_df = DataFrame(tickers)

            ticker_df = tickers_df[tickers_df["ticker"] == ticker]
            if ticker_df.empty:
                
                return ( 0 , 0 )

            return ticker_df["figi"].iloc[0] , ticker_df.iloc[0]
    #moex23
    

    lst = ['close_MOEX_ma1500', 'close_MTSS_ma7days', 'close_NVTK_ma1000', 'close_AFLT_ma720', 'close_IRAO_ma3days', 'close_IRAO_ma3.5days', 'close_RTKM_ma2000', 'close_MAGN_ma1000', 'close_SNGS_ma1500', 
           'close_IRAO_ma4days', 'close_LKOH_ma1000', 'close_GAZP_ma1000', 'close_RTS_ma1000', 'close_VTBR_ma720', 'close_IRAO_ma4.5days', 'close_AFKS_ma2000', 'close_FEES_ma1500', 'close_SNGSP_ma6.5days', 
           'close_CHMF_ma1000', 'close_IRAO_ma5days', 'close_MOEX_ma2000', 'close_SBERP_ma720', 'close_ROSN_ma1500', 'close_NLMK_ma1500', 'close_RTKM_ma2500', 'close_TATN_ma1500', 'close_SNGS_ma2000',
             'close_AFKS_ma2500', 'close_SNGSP_ma7days', 'close_ALRS_ma1500', 'close_IRAO_ma5.5days', 'close_FEES_ma2000', 'close_MOEX_ma2500', 'close_AFLT_ma1000', 'close_MAGN_ma1500', 'close_AFKS_ma3000',
               'close_NVTK_ma1500', 'close_IRAO_ma6days', 'close_RTS_ma1500', 'close_GAZP_ma1500', 'close_CHMF_ma1500', 'close_NLMK_ma2000', 'close_SNGS_ma2500', 'close_RTKM_ma3000', 'close_AFKS_ma3500',
                 'close_VTBR_ma1000', 'close_FEES_ma2500', 'close_IMOEX_ma1000', 'close_LKOH_ma1500', 'close_ROSN_ma2000', 'close_IRAO_ma6.5days', 'close_TATN_ma2000', 'close_MOEX_ma3000', 'close_AFKS_ma3days', 
                 'close_ALRS_ma2000', 'close_IRAO_ma7days', 'close_AFKS_ma3.5days', 'close_RTKM_ma3500', 'close_AFKS_ma4days', 'close_MAGN_ma2000', 'close_RTS_ma2000', 'close_FEES_ma3000', 'close_NLMK_ma2500',
                   'close_SBERP_ma1000', 'close_CHMF_ma2000', 'close_GAZP_ma2000', 'close_AFKS_ma4.5days', 'close_SNGS_ma3000', 'close_NVTK_ma2000', 'close_MOEX_ma3500', 'close_AFLT_ma1500', 'close_AFKS_ma5days', 
                   'close_TATN_ma2500', 'close_FEES_ma3500', 'close_ROSN_ma2500', 'close_LKOH_ma2000', 'close_VTBR_ma1500', 'close_RTKM_ma3days', 'close_RTS_ma2500', 'close_SNGS_ma3500', 'close_ALRS_ma2500',
                     'close_AFKS_ma5.5days', 'close_MAGN_ma2500', 'close_NLMK_ma3000', 'close_CHMF_ma2500', 'close_GAZP_ma2500', 'close_FEES_ma3days', 'close_SNGS_ma3days', 'close_RTKM_ma3.5days',
                       'close_FEES_ma3.5days', 'close_AFKS_ma6days', 'close_SNGS_ma3.5days', 'close_IMOEX_ma1500', 'close_NVTK_ma2500', 'close_TATN_ma3000', 'close_MOEX_ma3days', 'close_RTKM_ma4days', 
                       'close_RTS_ma3000', 'close_AFLT_ma2000', 'close_NLMK_ma3500', 'close_GAZP_ma3000', 'close_SNGS_ma4days', 'close_AFKS_ma6.5days', 'close_CHMF_ma3000', 'close_SNGS_ma4.5days', 'close_FEES_ma4days',
                         'close_VTBR_ma2000', 'close_ROSN_ma3000', 'close_MAGN_ma3000', 'close_LKOH_ma2500', 'close_SBERP_ma1500', 'close_RTKM_ma4.5days', 'close_ALRS_ma3000', 'close_SNGS_ma5days', 'close_MOEX_ma3.5days', 
                         'close_AFKS_ma7days', 'close_TATN_ma3500', 'close_RTS_ma3500', 'close_GAZP_ma3500', 'close_SNGS_ma5.5days', 'close_NLMK_ma3days', 'close_FEES_ma4.5days', 'close_SNGS_ma6days', 'close_CHMF_ma3500',
                           'close_RTKM_ma5days', 'close_NVTK_ma3000', 'close_SNGS_ma6.5days', 'close_AFLT_ma2500', 'close_MAGN_ma3500', 'close_SNGS_ma7days', 'close_NLMK_ma3.5days', 'close_ROSN_ma3500', 'close_IMOEX_ma2000',
                             'close_VTBR_ma2500', 'close_MOEX_ma4days', 'close_ALRS_ma3500', 'close_RTKM_ma5.5days', 'close_RTS_ma3days', 'close_TATN_ma3days', 'close_FEES_ma5days', 'close_GAZP_ma3days', 'close_CHMF_ma3days', 
                             'close_NVTK_ma3500', 'close_LKOH_ma3000', 'close_NLMK_ma4days', 'close_SBERP_ma2000', 'close_RTKM_ma6days', 'close_MOEX_ma4.5days', 'close_MAGN_ma3days', 'close_CHMF_ma3.5days', 'close_TATN_ma3.5days',
                               'close_RTS_ma3.5days', 'close_GAZP_ma3.5days', 'close_NLMK_ma4.5days', 'close_AFLT_ma3000', 'close_FEES_ma5.5days', 'close_MAGN_ma3.5days', 'close_MOEX_ma5days', 'close_RTKM_ma6.5days', 'close_CHMF_ma4days',
                                 'close_NLMK_ma5days', 'close_VTBR_ma3000', 'close_ALRS_ma3days', 'close_LKOH_ma3500', 'close_NVTK_ma3days', 'close_ROSN_ma3days', 'close_GAZP_ma4days', 'close_MAGN_ma4days', 'close_CHMF_ma4.5days', 
                                 'close_NLMK_ma5.5days', 'close_IMOEX_ma2500', 'close_MOEX_ma5.5days', 'close_RTS_ma4days', 'close_TATN_ma4days', 'close_RTKM_ma7days', 'close_GAZP_ma4.5days', 'close_FEES_ma6days', 'close_ALRS_ma3.5days', 
                                 'close_SBERP_ma2500', 'close_AFLT_ma3500', 'close_NVTK_ma3.5days', 'close_MAGN_ma4.5days', 'close_NLMK_ma6days', 'close_MOEX_ma6days', 'close_CHMF_ma5days', 'close_GAZP_ma5days', 'close_TATN_ma4.5days', 
                                 'close_RTS_ma4.5days', 'close_ROSN_ma3.5days', 'close_VTBR_ma3500', 'close_NLMK_ma6.5days', 'close_ALRS_ma4days', 'close_TATN_ma5days', 'close_MOEX_ma6.5days', 'close_GAZP_ma5.5days', 'close_MAGN_ma5days', 
                                 'close_GAZP_ma6days', 'close_LKOH_ma3days', 'close_CHMF_ma5.5days', 'close_FEES_ma6.5days', 'close_MOEX_ma7days', 'close_NLMK_ma7days', 'close_AFLT_ma3days', 'close_RTS_ma5days', 'close_TATN_ma5.5days',
                                   'close_ALRS_ma4.5days', 'close_GAZP_ma6.5days', 'close_NVTK_ma4days', 'close_TATN_ma6days', 'close_IMOEX_ma3000', 'close_MAGN_ma5.5days', 'close_CHMF_ma6days', 'close_GAZP_ma7days', 'close_SBERP_ma3000',
                                     'close_ALRS_ma5days', 'close_AFLT_ma3.5days', 'close_TATN_ma6.5days', 'close_LKOH_ma3.5days', 'close_NVTK_ma4.5days', 'close_RTS_ma5.5days', 'close_FEES_ma7days', 'close_VTBR_ma3days', 'close_TATN_ma7days',
                                       'close_ALRS_ma5.5days', 'close_ROSN_ma4days', 'close_MAGN_ma6days', 'close_CHMF_ma6.5days', 'close_AFLT_ma4days', 'close_RTS_ma6days', 'close_NVTK_ma5days', 'close_ALRS_ma6days', 'close_AFLT_ma4.5days',
                                         'close_IMOEX_ma3500', 'close_CHMF_ma7days', 'close_SBERP_ma3500', 'close_ALRS_ma6.5days', 'close_VTBR_ma3.5days', 'close_MAGN_ma6.5days', 'close_RTS_ma6.5days', 'close_AFLT_ma5days', 'close_ROSN_ma4.5days',
                                           'close_LKOH_ma4days', 'close_NVTK_ma5.5days', 'close_ALRS_ma7days', 'close_AFLT_ma5.5days', 'close_RTS_ma7days', 'close_MAGN_ma7days', 'close_AFLT_ma6days', 'close_NVTK_ma6days', 'close_ROSN_ma5days', 'close_LKOH_ma4.5days', 'close_AFLT_ma6.5days', 'close_VTBR_ma4days', 'close_AFLT_ma7days', 'close_NVTK_ma6.5days', 'close_IMOEX_ma3days', 'close_SBERP_ma3days', 'close_LKOH_ma5days', 'close_ROSN_ma5.5days', 'close_VTBR_ma4.5days', 'close_NVTK_ma7days', 'close_LKOH_ma5.5days', 'close_SBERP_ma3.5days', 'close_IMOEX_ma3.5days', 'close_VTBR_ma5days', 'close_LKOH_ma6days', 'close_ROSN_ma6days', 'close_LKOH_ma6.5days', 'close_SBERP_ma4days', 'close_VTBR_ma5.5days', 'close_LKOH_ma7days', 'close_ROSN_ma6.5days', 'close_IMOEX_ma4days', 'close_VTBR_ma6days', 'close_SBERP_ma4.5days', 'close_ROSN_ma7days', 'close_VTBR_ma6.5days', 'close_SBERP_ma5days', 'close_IMOEX_ma4.5days', 'close_VTBR_ma7days', 'close_SBERP_ma5.5days', 'close_IMOEX_ma5days', 
                                           'close_SBERP_ma6days', 'close_SBERP_ma6.5days', 'close_IMOEX_ma5.5days', 'close_SBERP_ma7days', 'close_IMOEX_ma6days', 'close_IMOEX_ma6.5days', 'close_IMOEX_ma7days']
    
    days = {'ma720' : 720 , 'ma1000' : 1000 , 'ma1500' : 1500 ,
         'ma2000' : 2000 , 'ma2500' : 2500 , 'ma3000' : 3000 , 'ma3days' : 1440 * 3 , 'ma3.5days' : int(1440 * 3.5) , 
         'ma4days' : 1440 * 4 , 'ma4.5days' : int(1440 * 4.5) , 'ma5days' : 1440 * 5 ,  'ma5.5days' : int(1440 * 5.5) , 
         'ma6days' : 1440 * 6 , 'ma6.5days' : int(1440 * 6.5) , 'ma7days' : 1440 * 7 , 'ma3500' : 3500  }
    
    import joblib
    import ta 
    import numpy as np
    from copy import deepcopy

    specification = {'SBERP': [], 'IRAO': [], 'LKOH': [], 'NVTK': [], 'TATN': [], 'SNGS': [],'ROSN': [],'FEES': [],
      'CHMF': [], 'IMOEX': [], 'ALRS': [], 'AFLT': [], 'RTS': [], 'MOEX': [],'MTSS': [], 'MAGN': [], 'GAZP': [], 'VTBR': [], 'RTKM': [],'AFKS': [], 'SNGSP': [], 'NLMK': []}
    for i in lst:
      specification[i.split('_')[1]].append(i.split('_')[-1])

    
    total = {}

    for ticker , mas in specification.items():
        
        ticker1 = deepcopy(ticker)

        if ticker == 'IMOEX' :
            ticker = 'IMOEXF'
        if ticker == 'RTS':
            ticker = 'RIM5'  # Поменять потом

        close = get_all_quotes_info( [get_figi_by_ticker(ticker)[1]['figi'] ] , [ticker] )[ticker]['close']
        
        for ma in mas : 
            number = days[ma]
            
            try:
              last = ta.trend.sma_indicator(close= close , window=number ).iloc[-1]
            except:
              last = np.nan
            
            print(f'close_{ticker1}_{ma}')
            total[f'close_{ticker1}_{ma}'] = [last ]
        
    df = pd.DataFrame(total)
    df = df[lst]
    print( df.shape )

    return df 

    
