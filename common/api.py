#!/usr/bin/env python
import requests
import json
import model
__endpoint_tickers_all = 'https://api.coinmarketcap.com/v1/ticker/?limit=10000'
__endpoint_token = 'https://api.coinmarketcap.com/v1/ticker/%s/?convert=%s'
__endpoint_mcap = 'https://api.coinmarketcap.com/v1/global/'

def get_mcap():
    mcap_json = requests.get(__endpoint_mcap).json()
    return model.MarketCapitalization(mcap_json)

def get_token(name, balance = 0, currency = 'usd'):
    token = requests.get(__endpoint_token % (name, currency)).json()[0]
    return model.Token(token, balance, currency)

def search_token(search):
    r_tokens = requests.get(__endpoint_tickers_all).json()
    for r_token in r_tokens:
        token = model.Token(r_token)
        if token.matches(search):
            return token
    return None

def search_tokens(search):
    r_tokens = requests.get(__endpoint_tickers_all).json()
    tokens = []
    for r_token in r_tokens:
        token = model.Token(r_token)
        if token.matches(search):
            tokens.append(token)
    return tokens

def get_portfolio(portfolio_config, currency):
    portfolio = model.Portfolio()
    # get stats for each coin
    for item in portfolio_config:
        token = get_token(item[0], item[1], currency)
        portfolio.add_token(token)
    return portfolio
