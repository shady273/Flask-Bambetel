import pprint
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
id_coin = ["bitcoin", "ethereum", "tether", "binancecoin"]

price = cg.get_coins_markets("bitcoin")

print(price)