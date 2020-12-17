import postgres
from flask import Flask, jsonify
from flask_cors import CORS
from flask import request
import Parsers

app = Flask(__name__)
CORS(app)
api_url = '/api/v1.0'
dota = Parsers.Dota()
overwatch = Parsers.Overwatch()
pg = postgres.Postgress()


@app.route('/')
def hello_world():
    return 'Hello World!'


# 1 -- dota, 2 -- over, 3 -- HS
# http://127.0.0.1:5000/api/v1.0/GAME_ID/GAMING_PROFILE
@app.route(f'{api_url}/<int:game_id>/<account>', methods=['GET'])
def get_metrics(game_id, account):
    try:
        game_id -= 1
        games = ['Dota', 'Overwatch', 'HyperScape']
        resp = {}
        if game_id == 0:
            db_data = pg.get_dota_stats(account)
            # print('data:', db_data)
            if db_data is not None:
                return jsonify(db_data)
            else:
                resp = dota.get_stats(id=account)
                pg.save_dota(account, resp)
        elif game_id == 1:
            db_data = pg.get_overwatch_stats(account)
            # print(db_data)
            if db_data is not None:
                return jsonify(db_data)
            else:
                resp = overwatch.get_stats(nickname=account)
                pg.save_overwatch(account, resp)
        # print(resp)
        return jsonify(resp)
    except Exception as e:
        print(e)
        return e


@app.route(f'{api_url}/users/get/<talent_id>', methods=['GET'])
def get_user(talent_id):
    try:
        row = pg.get_user(talent_id=talent_id)
        return {'talent_id': talent_id, 'steam': row[1], 'blizzard': row[2]}
    except Exception as e:
        print(e)
        return 'error'


@app.route(f'{api_url}/users/put', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        if 'platform' in data:
            if data['platform'] == 'steam':
                pg.add_steam(data['talent_id'], data['account_id'])
            elif data['platform'] == 'blizzard':
                pg.add_blizard(data['talent_id'], data['account_id'])
        return '123'
    except Exception as e:
        print(e)
        return 'bad data'


if __name__ == '__main__':
    app.run()
