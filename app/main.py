from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
import asyncio
import logging
import pandas as pd
import numpy as np
from tinkoff.invest import Client, SecurityTradingStatus, CandleInterval
from tinkoff.invest.services import InstrumentsService
from tinkoff.invest.utils import quotation_to_decimal, now
import ta
from copy import deepcopy
import joblib
import joblib
import ta 
import numpy as np
from copy import deepcopy
from sqlalchemy import desc, distinct

try:
    import models
    import auth
except:
    from app import auth, models 

try:
    from database import engine, get_db
except:
    from app.database import engine, get_db

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Загружаем модель один раз при старте
try:
    ml_model = joblib.load('catboost_lr 0.38121, mae 0.1857300913901133 , mape 0.009344126631801567, rmse 0.10354896606489733.joblib')
    logger.info("ML model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load ML model: {e}")
    raise

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Конфигурация Tinkoff API
TOKEN = 't.YbAt3ov-iNU4jt9A4l9ML4ga77xB1z_NYKOFEvZZDRv72ilghDUEJVk3B86XRSCeyNz5_do2Go_cAqj2qjH9Jg'

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

async def update_prediction():
    from concurrent.futures import ThreadPoolExecutor
    executor = ThreadPoolExecutor(max_workers=1)
    
    while True:
        try:
            logger.info("Starting prediction update...")
            # Запускаем get_current_features1 в отдельном потоке
            loop = asyncio.get_event_loop()
            features = await loop.run_in_executor(executor, get_current_features1)
            
            if not features.empty and not features.isna().all().all():
                prediction = ml_model.predict(features)[0]
                current_time = datetime.utcnow()
                
                # Сохраняем в базу
                db = next(get_db())
                new_prediction = models.Prediction(
                    value=float(prediction),
                    timestamp=current_time
                )
                db.add(new_prediction)
                db.commit()
                logger.info(f"New prediction saved: {prediction} at {current_time}")
            else:
                logger.error("Failed to create valid features DataFrame")

        except Exception as e:
            logger.error(f"Error in prediction update: {e}")
        
        await asyncio.sleep(10)  # 5 минут между обновлениями

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(update_prediction())

@app.post("/register")
def register(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logger.info(f"Attempting to register user with email: {form_data.username}")
    try:
        user = db.query(models.User).filter(models.User.email == form_data.username).first()
        if user:
            logger.warning(f"User with email {form_data.username} already exists")
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = auth.get_password_hash(form_data.password)
        new_user = models.User(email=form_data.username, hashed_password=hashed_password)
        db.add(new_user)
        db.commit()
        logger.info(f"Successfully registered user with email: {form_data.username}")
        return {"message": "User created successfully"}
    except Exception as e:
        logger.error(f"Error during registration: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logger.info(f"Login attempt for user: {form_data.username}")
    try:
        user = db.query(models.User).filter(models.User.email == form_data.username).first()
        if not user:
            logger.warning(f"User not found: {form_data.username}")
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not auth.verify_password(form_data.password, user.hashed_password):
            logger.warning(f"Invalid password for user: {form_data.username}")
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        logger.info(f"Successful login for user: {form_data.username}")
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/prediction")
async def get_prediction(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    try:
        latest_prediction = db.query(models.Prediction).order_by(desc(models.Prediction.timestamp)).first()
        
        if not latest_prediction:
            return {
                "status": "initializing",
                "message": "ML model is warming up, please wait..."
            }
        
        return {
            "status": "ready",
            "prediction": latest_prediction.value,
            "timestamp": latest_prediction.timestamp
        }
    except Exception as e:
        logger.error(f"Error in get_prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/prediction/history")
async def get_prediction_history(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    try:
        recent_predictions = db.query(models.Prediction)\
            .order_by(desc(models.Prediction.timestamp))\
            .limit(2000)\
            .all()
        
        return {
            "history": [
                {
                    "prediction": pred.value,
                    "timestamp": pred.timestamp
                } for pred in recent_predictions
            ]
        }
    except Exception as e:
        logger.error(f"Error in get_prediction_history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))