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
        self.coeffs = helper.dota_coeffs
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
        self.main_stats = {
            "allDamageDoneAvgPer10Min": 0,
            "barrierDamageDoneAvgPer10Min": 0,
            "deathsAvgPer10Min": 0,
            "eliminationsAvgPer10Min": 0,
            "finalBlowsAvgPer10Min": 0,
            "healingDoneAvgPer10Min": 0,
            "heroDamageDoneAvgPer10Min": 0,
            "objectiveKillsAvgPer10Min": 0,
            "objectiveTimeAvgPer10Min": 0,
            "soloKillsAvgPer10Min": 0,
            "timeSpentOnFireAvgPer10Min": 0
        }
        with open('mean_overwatch_data2.json', 'r') as r:
            self.mean_stats = json.loads(r.read())
        self.role_coefs = helper.over_role_coefs

    def get_pro_stats(self):
        with open('1.txt', 'r') as r:
            names = r.read().split('\n')
        print(len(names))
        mean_data = {'tank': self.main_stats.copy(), 'damage': self.main_stats.copy(),
                     'support': self.main_stats.copy(), 'normal': self.main_stats.copy(), }
        for role in mean_data:
            mean_data[role]['count'] = 0
        c = 0
        for name in names:
            print(c)
            try:
                stats = self.get_stats(name)
                role = stats['best_role']
                for key in mean_data[role]:
                    if key in stats:
                        mean_data[role][key] += stats[key]
                mean_data[role]['count'] += 1
                role = 'normal'
                for key in mean_data[role]:
                    if key in stats:
                        mean_data[role][key] += stats[key]
                mean_data[role]['count'] += 1
                c += 1
            except Exception as e:
                print(e)
            if c % 5 == 0:
                with open('mean_overwatch_data_reserve2.txt', 'w') as write:
                    write.write(str(mean_data) + str(c))

        print(mean_data)
        for role in mean_data:
            for key in mean_data[role]:
                mean_data[role][key] /= mean_data[role]['count']
        print(mean_data)

        with open('mean_overwatch_data2.json', 'w') as write:
            write.write(str(mean_data) + str(c))

    def get_stats(self, nickname='Chill-11683'):
        url = f'https://ow-api.com/v1/stats/pc/eu/{nickname}/complete'
        # p = {'TRN-Api-Key': 'd91bbc29-6e7c-41ae-adb5-56c6235f5954'}
        response = requests.get(url)
        data = response.json()
        # data = {}
        # print(data)
        # if 'data' in data:
        #    data = data['data']
        parsed = self.parse_data(data)
        processed = self.process_data(parsed)
        return processed
        # return parsed
        # print(parsed)

    def parse_data(self, data):
        parsed_data = self.main_stats.copy()
        if 'competitiveStats' in data:
            competitive_stats = data['competitiveStats']['careerStats']['allHeroes']
            if 'average' in competitive_stats:
                avg_stats = competitive_stats['average']
                for stat in self.main_stats:
                    if stat in avg_stats:
                        val = avg_stats[stat]
                        if type(val) == str:
                            val = int(val[-5:-3]) * 60 + int(val[-2:])
                        parsed_data[stat] += val
                # print(parsed_data)
                if 'ratings' in data and data['ratings'] is not None:
                    rates = data['ratings']
                    levels = {}
                    for role in rates:
                        levels[role['role']] = role['level']
                    level_keys = sorted(levels, key=lambda x: levels[x])
                    best_role = level_keys[-1]
                    parsed_data['best_role'] = best_role
                else:
                    parsed_data['best_role'] = 'normal'
                return parsed_data

    def process_data(self, data):
        processed_data = data.copy()
        coeffs = self.role_coefs[processed_data['best_role']]
        summ = 0
        for key in processed_data:
            if key == 'best_role':
                print(processed_data[key])
                continue
            mean_stats = self.mean_stats[processed_data['best_role']]
            if key in mean_stats:
                processed_data[key] /= mean_stats[key]
                if key == 'deathsAvgPer10Min':
                    processed_data[key] = 1 + (1 - processed_data[key])
                processed_data[key] *= coeffs[key]
                summ += processed_data[key]
        # print(processed_data)
        print('score:', summ)
        processed_data['score'] = summ
        return processed_data


if __name__ == '__main__':
    ov = Overwatch()
    print(ov.get_stats(nickname='Gael-21904'))
    # dota = Dota('Daltoosh')
    # dota.get_stats()
# print(dota.get_stats())
