from flask import Flask, jsonify
from flask_cors import CORS
from flask import request
import Parsers

app = Flask(__name__)
CORS(app)
api_url = '/api/v1.0'
dota = Parsers.Dota()
overwatch = Parsers.Overwatch()


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
            resp = dota.get_stats(id=account)
        elif game_id == 1:
            resp = overwatch.get_stats(nickname=account)
        # print(resp)
        return jsonify(resp)
    except Exception as e:
        raise e
        print(e)
        return e


if __name__ == '__main__':
    app.run()
