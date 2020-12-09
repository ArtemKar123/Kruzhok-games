import json
import requests


class Dota:
    def __init__(self, nickname, ):
        self.steam_id = '132851371'#'178121777'
        self.nickname = nickname
        with open('heroes.json', 'r') as r:
            self.heroes = json.loads(r.read())

    def get_stats(self):
        url = f'https://api.opendota.com/api/players/{self.steam_id}/matches'
        p = {'project': ["game_mode", "lobby_type", "hero_id", "kills", "deaths", "assists", "xp_per_min",
                         "gold_per_min", "hero_damage", "tower_damage", "hero_healing", "last_hits", "cluster",
                         "leaver_status", "party_size"]}
        # response = requests.get(url, params=p)
        # data = response.json()
        with open('data2.txt', 'r') as f:
            data = json.loads(f.read())
            self.parse_data(data[:])

    def parse_data(self, data):
        stats = {"kills": 0, "deaths": 0, "assists": 0, 'hero_healing': 0, 'hero_damage': 0, 'tower_damage': 0,
                 'xp_per_min': 0, 'gold_per_min': 0}
        n_games = len(data)
        for game in data:
            game_stats = {"kills": 0, "deaths": 0, "assists": 0, 'hero_healing': 0, 'hero_damage': 0, 'tower_damage': 0,
                          'xp_per_min': 0, 'gold_per_min': 0, 'hero': -1}
            if 'hero_id' in game:
                game_stats['hero'] = game['hero_id']
            for key in stats.keys():
                if key in game:
                    if not game[key] is None:
                        stats[key] += game[key]
                        game_stats[key] += game[key]
            # self.count_role_metric(game_stats)

        print(stats, n_games)
        for key in stats.keys():
            stats[key] /= n_games
        print(stats)

    def count_role_metric(self, stats):
        means = {"kills": 0, "deaths": 0, "assists": 0, 'hero_healing': 0, 'hero_damage': 0, 'tower_damage': 0,
                 'xp_per_min': 0, 'gold_per_min': 0}

        roles = self.heroes[str(stats['hero'])]['roles']
        print(roles)


if __name__ == '__main__':
    apex = Dota('Daltoosh')
    apex.get_stats()
