import pprint
from pycoingecko import CoinGeckoAPI
from app import AllCoins, Profiles
from app import app, db
from sqlalchemy import func, desc, asc

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


# removes unrated cryptocurrencies
def delete_wtht_rtng():
    with app.app_context():
        null_rank = Profiles.query.filter_by(cg_rank=None).all()
        for profile in null_rank:
            db.session.delete(profile)
        db.session.commit()

        coins_to_delete = db.session.query(AllCoins). \
            outerjoin(Profiles, AllCoins.id_coin == Profiles.coin_id). \
            filter(Profiles.coin_id is None).all()

        for coin in coins_to_delete:
            db.session.delete(coin)
        db.session.commit()

# rating CG update
def update_rtng():
    id_list = []
    with app.app_context():
        id_list = AllCoins.query.all()
        for coin in id_list:
            try:
                info_coin = cg.get_coin_by_id(coin.id_coin)
                print(f"{coin.id_coin} new cg_rank {info_coin['market_data']['market_cap']['usd']}")
                db.session.query(Profiles).filter_by\
                    (coin_id=coin.id_coin).update({Profiles.cg_rank: info_coin['market_data']['market_cap']['usd']})

                db.session.commit()
            except Exception as e:
                print(e)

# sorting id in the profiles table
def sorted_profiles():
    with app.app_context():
        profiles_sorted = Profiles.query.order_by(Profiles.cg_rank.desc()).all()
        i = 0
        for profile in profiles_sorted:
            print(f'old_id={profile.id}')
            print(f'{profile.coin_id}')
            i += 1
            print(f'new_id={i}')
            db.session.query(AllCoins).filter_by(id_coin=profile.coin_id).update({'rating': i})
            db.session.flush()
        db.session.commit()

# update price coins
def updata_price():
    with app.app_context():
        all_coins_data = db.session.query(AllCoins).order_by(asc(AllCoins.rating)).all()
        id_coin_list = [coin.id_coin for coin in all_coins_data]
        for i in range(0, len(id_coin_list), 500):
            price = cg.get_price(id_coin_list[i:i+500], vs_currencies='usd')

            for coin_id in price:
                try:
                    db.session.query(AllCoins).filter_by(id_coin=coin_id).update({'price': price[coin_id]['usd']})
                    db.session.commit()
                except Exception as e:
                    print(e)


# Delete coin withaout coin price
def delete_coin_wpr():
    with app.app_context():
        coins_to_delete = db.session.query(AllCoins).filter(AllCoins.price == None).all()
        for delete in coins_to_delete:
            db.session.delete(delete)
            db.session.commit()

