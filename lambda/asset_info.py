# -*- coding: utf-8 -*-
from __future__ import print_function
import zaifapi

class AssetInfo(object):
    def __init__(self, key_zaif, secret_zaif):
        self.key_zaif = key_zaif
        self.secret_zaif = secret_zaif
    
    def get_zaif_asset(self):
        zaif_trade = zaifapi.ZaifTradeApi(key=self.key_zaif, secret=self.secret_zaif)
        zaif_public = zaifapi.ZaifPublicApi()
        deposits = zaif_trade.get_info2()["deposit"] #所有通貨とその量を取得
        asset_zaif = 0 #初期値
        for currency, amount in deposits.items():
            if currency == "jpy": #jpyのみレートはいらない
                asset_zaif += amount
            else:
                asset_zaif += amount * zaif_public.last_price(currency.lower() + "_jpy")["last_price"]
        return round(asset_zaif) #小数点以下省略