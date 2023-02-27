import pprint
from pycoingecko import CoinGeckoAPI
from DataBase import AllCoins, Profiles
from app import app, db

cg = CoinGeckoAPI()


# function populates a table with data
def coin_list():
    all_coins = cg.get_coins_list()
    with app.app_context():
        for coin in all_coins:
            ac = AllCoins(id_coin=coin['id'], symbol=coin['symbol'], name=coin['name'])
            db.session.add(ac)
            db.session.flush()
            db.session.commit()


# The function adds cryptocurrency ratings and other data
def coin_data():
    ls_coin = []
    with app.app_context():
        ls_coin = AllCoins.query.all()
        profiles = Profiles.query.all()
        coin_ids = [profile.coin_id for profile in profiles]
        print(coin_ids)
        for coin in ls_coin:
            if coin.id_coin in coin_ids:
                print(f'id {coin.id_coin} вже у таблиці')
                pass
            else:
                print(coin.id_coin)
                try:
                    info_coin = cg.get_coin_by_id(coin.id_coin)
                    pr = Profiles(coin_id=coin.id_coin, cg_rank=info_coin['market_cap_rank'],
                                  img_large=info_coin['image']['large'],
                                  img_small=info_coin['image']['small'],
                                  img_thumb=info_coin['image']['thumb'],
                                  homepage=info_coin['links']['homepage'][0])
                    db.session.add(pr)
                    db.session.flush()
                    db.session.commit()
                except Exception as e:
                    print(e)


coin_data()
