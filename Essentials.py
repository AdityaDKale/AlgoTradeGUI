from UserInfo import Info
from fyers_api import fyersModel,accessToken
import os
from datetime import datetime
import pandas as pd
from fuzzywuzzy import fuzz


client_id = Info.APP_ID
secret_key = Info.APP_SECRET
redirect_uri = Info.REDIRECT_URL

class Essentials:
    
    def get_access_token():

        global client_id,secret_key,redirect_uri
        if not os.path.exists('access_token.txt'):

            session = accessToken.SessionModel(client_id=client_id,secret_key=secret_key,redirect_uri=redirect_uri, response_type="code",grant_type="authorization_code")
            response = session.generate_authcode()
            print("Login URL: ",response)
            auth_code = input("Enter Auth Code: ")
            session.set_token(auth_code)
            ACCESS_TOKEN = session.generate_token()['access_token']

            with open('access_token.txt','w') as file:
                file.write(ACCESS_TOKEN)

        else:
            with open('access_token.txt','r') as file:
                ACCESS_TOKEN = file.read()

        return ACCESS_TOKEN

    class SymbolMaster:

        # HEADERS = ['Fytoken','Symbol Details','Exchange Instrument type','Minimum lot size','Tick size','ISIN','Trading Session','Last update date','Expiry date','Symbol ticker','Exchange','Segment','Scrip code','Underlying scrip code','Strike price','Option type']
        EQUITY_DERIVATIVES = pd.read_csv('https://public.fyers.in/sym_details/NSE_FO.csv',names=[i for i in range(19)])
        CAPITAL_MARKET = pd.read_csv('https://public.fyers.in/sym_details/NSE_CM.csv')

    def create_market_order(symbol,qty,side):
        
        global fyers

        side_dict = {'BUY':1,'SELL':-1,'buy':1,'sell':-1}


        data = {
            "symbol":f"{symbol}",
            "qty":qty,
            "type":2,
            "side":side_dict[side],
            "productType":"INTRADAY",
            "limitPrice":0,
            "stopPrice":0,
            "validity":"DAY",
            "disclosedQty":0,
            "offlineOrder":"False",
            "stopLoss":0,
            "takeProfit":0
        }

        order = fyers.place_order(data)
        return order

    def historical_data(symbol,resolution,date_format,range_from,range_to,cont_flag):

        data = {"symbol":symbol,"resolution":resolution,"date_format":date_format,"range_from":range_from,"range_to":range_to,"cont_flag":cont_flag}
        return fyers.history(data)
    
    def options_script_search(search_string):
        df = Essentials.SymbolMaster.EQUITY_DERIVATIVES
        df['match_score'] = df[1].apply(lambda x: fuzz.ratio(x, search_string))
        nearest_match_index = df['match_score'].idxmax()
        return Essentials.SymbolMaster.EQUITY_DERIVATIVES[9][nearest_match_index]




access_token = Essentials.get_access_token()
fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="logs/")
