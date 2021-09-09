from pathlib import Path
from swyftx import Swyftx

config = {key.lower() : value.rstrip('\n') for key, value in (line.split(' = ') for line in open(Path.cwd() / 'config.txt'))}

swyftx = Swyftx(config)

# Authentication
def test_refresh_access_token():
    token = swyftx.refresh_access_token(data = {'apiKey': config['api_key']})
    assert token.json()['accessToken'].startswith('ey')

# Account
def test_get_account_balances():
    token = swyftx.refresh_access_token(data = {'apiKey': config['api_key']})
    account_balances = swyftx.get_account_balances(headers = {'Authorization': f'Bearer {token}'}).json()
    assert account_balances

# Markets
def test_get_market_assets():
    market_assets = swyftx.get_market_assets().json()
    assert market_assets[0]['code'] == 'AUD'

def test_get_live_rates():
    btc_live_rates = swyftx.get_live_rates(asset = 3).json()
    assert btc_live_rates