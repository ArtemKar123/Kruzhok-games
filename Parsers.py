import json
import time

import requests
import helper


class Dota:
    def __init__(self, nickname, ):
        self.steam_id = '132851371'  # '178121777'
        self.nickname = nickname
        with open('heroes.json', 'r') as r:
            self.heroes = json.loads(r.read())
        self.roles = []
        for key in self.heroes.keys():
            for role in self.heroes[key]['roles']:
                self.roles.append(role)
        self.roles = set(self.roles)
        print(self.roles)
        with open('mean_dota_data.json', 'r') as r:
            self.mean_stats = json.loads(r.read())
        print(self.mean_stats)
        self.coeffs = helper.coeffs
        # print(self.heroes.keys())

    def count_mean(self):
        s = time.time()
        mean_stats = {
            'Carry': {'kills': 0, 'deaths': 0, 'assists': 0, 'hero_healing': 0, 'hero_damage': 0, 'tower_damage': 0,
                      'xp_per_min': 0, 'gold_per_min': 0, 'n_games': 0},
            'Nuker': {'kills': 0, 'deaths': 0, 'assists': 0, 'hero_healing': 0, 'hero_damage': 0, 'tower_damage': 0,
                      'xp_per_min': 0, 'gold_per_min': 0, 'n_games': 0},
            'Disabler': {'kills': 0, 'deaths': 0, 'assists': 0, 'hero_healing': 0, 'hero_damage': 0, 'tower_damage': 0,
                         'xp_per_min': 0, 'gold_per_min': 0, 'n_games': 0},
            'Durable': {'kills': 0, 'deaths': 0, 'assists': 0, 'hero_healing': 0, 'hero_damage': 0, 'tower_damage': 0,
                        'xp_per_min': 0, 'gold_per_min': 0, 'n_games': 0},
            'Initiator': {'kills': 0, 'deaths': 0, 'assists': 0, 'hero_healing': 0, 'hero_damage': 0, 'tower_damage': 0,
                          'xp_per_min': 0, 'gold_per_min': 0, 'n_games': 0},
            'Escape': {'kills': 0, 'deaths': 0, 'assists': 0, 'hero_healing': 0, 'hero_damage': 0, 'tower_damage': 0,
                       'xp_per_min': 0, 'gold_per_min': 0, 'n_games': 0},
            'Pusher': {'kills': 0, 'deaths': 0, 'assists': 0, 'hero_healing': 0, 'hero_damage': 0, 'tower_damage': 0,
                       'xp_per_min': 0, 'gold_per_min': 0, 'n_games': 0},
            'Jungler': {'kills': 0, 'deaths': 0, 'assists': 0, 'hero_healing': 0, 'hero_damage': 0, 'tower_damage': 0,
                        'xp_per_min': 0, 'gold_per_min': 0, 'n_games': 0},
            'Support': {'kills': 0, 'deaths': 0, 'assists': 0, 'hero_healing': 0, 'hero_damage': 0, 'tower_damage': 0,
                        'xp_per_min': 0, 'gold_per_min': 0, 'n_games': 0}}
        pros = self.get_pros(count=500)
        print(len(pros))
        c = 0
        for p in pros:
            one_s = time.time()
            c += 1
            print(c)
            try:
                stats = self.get_stats(p['account_id'])
                for role in stats.keys():
                    for key in stats[role].keys():
                        if key in mean_stats[role]:
                            mean_stats[role][key] += stats[role][key]
            except Exception as e:
                print(e)
                continue
            if c % 5 == 0:
                with open('mean_dota_data_reserve.txt', 'w') as write:
                    write.write(str(mean_stats) + str(c))

            step_time = time.time() - one_s
            # print(step_time)
            # if step_time < 1:
            #    time.sleep(1 - step_time)

        print(time.time() - s)
        for role in mean_stats.keys():
            for key in mean_stats[role].keys():
                mean_stats[role][key] /= len(pros)

        with open('mean_dota_data.json', 'w') as write:
            write.write(str(mean_stats))

    def get_pros(self, count=3):
        url = 'https://api.opendota.com/api/proPlayers'
        response = requests.get(url)
        data = response.json()
        if count == -1:
            count = len(data)
        return data[:count]

    def get_stats(self, id='132851371'):
        url = f'https://api.opendota.com/api/players/{id}/matches'
        p = {'project': ["game_mode", "lobby_type", "hero_id", "kills", "deaths", "assists", "xp_per_min",
                         "gold_per_min", "hero_damage", "tower_damage", "hero_healing", "last_hits", "cluster",
                         "leaver_status", "party_size"]}
        response = requests.get(url, params=p)
        data = response.json()
        print(len(data))
        self.parse_data(data[:])
        # with open('data2.txt', 'r') as f:

    #            data = json.loads(f.read())
    #           self.parse_data(data[:])

    def parse_data(self, data):
        stats = {"kills": 0, "deaths": 0, "assists": 0, 'hero_healing': 0, 'hero_damage': 0, 'tower_damage': 0,
                 'xp_per_min': 0, 'gold_per_min': 0, 'role_value': 0}
        role_stats = {}
        for role in self.roles:
            role_stats[role] = stats.copy()
            role_stats[role]['n_games'] = 0
        # print(role_stats)
        n_games = len(data)
        for game in data:
            game_stats = {"kills": 0, "deaths": 0, "assists": 0, 'hero_healing': 0, 'hero_damage': 0, 'tower_damage': 0,
                          'xp_per_min': 0, 'gold_per_min': 0, 'hero': -1}
            if 'hero_id' in game:
                game_stats['hero'] = str(game['hero_id'])

            for key in stats.keys():
                if key in game:
                    if not game[key] is None:
                        stats[key] += game[key]
                        game_stats[key] += game[key]

            # print(self.heroes[game_stats['hero']]['roles'])
            if game_stats['hero'] in self.heroes:
                for r in self.heroes[game_stats['hero']]['roles']:
                    for key in game_stats.keys():
                        if key in role_stats[r]:
                            role_stats[r][key] += game_stats[key]
                    role_stats[r]['n_games'] += 1

            stats['role_value'] += self.count_role_metric(game_stats)
        for role in role_stats.keys():
            for key in role_stats[role].keys():
                if key != 'n_games':
                    if role_stats[role]['n_games'] > 0:
                        role_stats[role][key] /= role_stats[role]['n_games']

        for key in stats.keys():
            if key != 'n_games':
                if len(data) > 0:
                    stats[key] /= len(data)

        print(stats)
        return role_stats

    def count_role_metric(self, stats):
        if int(stats['hero']) > 0:
            # print(stats)
            roles = self.heroes[stats['hero']]['roles']
            diff = {}
            total = {}
            for role in roles:
                diff[role] = stats.copy()
                total[role] = stats.copy()
                total[role]['score'] = 0
                for key in stats.keys():
                    if key in self.mean_stats[role]:
                        if key == 'deaths':
                            diff[role][key] = stats[key] / self.mean_stats[role][key]
                            diff[role][key] = 1 + (1 - diff[role][key])
                        else:
                            diff[role][key] = stats[key] / self.mean_stats[role][key]
                        total[role][key] = diff[role][key] * self.coeffs[role][key]
                        total[role]['score'] += total[role][key]
            #            print(diff['Durable'])
            res = 0
            c = 0
            for key in total:
                c += 1
                # print(total[key]['score'])
                res += total[key]['score']
            return res / c
        else:
            return 200


class Overwatch:
    def __init__(self):
        self.url = 'https://public-api.tracker.gg/v2/overwatch/standard/profile/battlenet/'
        self.main_stats = {'timePlayed': 0, 'wins': 0, 'matchesPlayed': 0, 'timeSpentOnFire': 0, 'wlPercentage': 0,
                           'medals': 0, 'goldMedals': 0, 'silverMedals': 0, 'bronzeMedals': 0, 'multiKills': 0,
                           'soloKills': 0,
                           'objectiveKills': 0, 'environmentalKills': 0, 'finalBlows': 0, 'damageDone': 0,
                           'healingDone': 0,
                           'eliminations': 0, 'deaths': 0, 'kd': 0, 'kg': 0, 'objectiveTime': 0, 'defensiveAssists': 0,
                           'offensiveAssists': 0}

    def get_stats(self, nickname='bame%231784'):
        url = self.url + nickname
        p = {'TRN-Api-Key': 'd91bbc29-6e7c-41ae-adb5-56c6235f5954'}
        response = requests.get(url, params=p)
        data = response.json()
        print(data)
        if 'data' in data:
            data = data['data']
            self.parse_data(data)

    def parse_data(self, data):
        if 'segments' in data:
            parsed_data = self.main_stats.copy()
            segments = data['segments']
            for segm in segments:
                segm = segm['stats']
                for stat in self.main_stats:
                    if stat in segm:
                        parsed_data[stat] += segm[stat]['value']
            print(parsed_data)
            for param in parsed_data:
                if param != 'timePlayed':
                    parsed_data[param] = parsed_data[param] * 600 / parsed_data['timePlayed']
            print(parsed_data)


if __name__ == '__main__':
    ov = Overwatch()
    ov.get_stats()
# dota = Dota('Daltoosh')
# dota.get_stats()
# print(dota.get_stats())
