import json
import psycopg2

from contextlib import closing


class Postgress:

    def __init__(self):
        self.user = 'postgres'
        self.password = 'root'
        self.dbname = 'kruzhok'

    def get_steam(self, talent_id):
        with closing(psycopg2.connect(dbname=self.dbname, user=self.user,
                                      password=self.password, host='localhost')) as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT steam_id FROM users where talent_id = %s', (talent_id,))
                for row in cursor:
                    return row[0]

    def get_blizzard(self, talent_id):
        with closing(psycopg2.connect(dbname=self.dbname, user=self.user,
                                      password=self.password, host='localhost')) as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT blizzard_id FROM users where talent_id = %s', (talent_id,))
                for row in cursor:
                    return row[0]

    def get_user(self, talent_id):
        with closing(psycopg2.connect(dbname=self.dbname, user=self.user,
                                      password=self.password, host='localhost')) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'select * from users where talent_id = %s',
                    (talent_id, ))
                for row in cursor:
                    return row

    def add_steam(self, talent_id, steam_id):
        with closing(psycopg2.connect(dbname=self.dbname, user=self.user,
                                      password=self.password, host='localhost')) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'insert into users (talent_id, steam_id) values (%s, %s) ON CONFLICT (talent_id) DO UPDATE SET steam_id = excluded.steam_id;',
                    (talent_id, steam_id,))
                conn.commit()

    def add_blizzard(self, talent_id, blizzard_id):
        with closing(psycopg2.connect(dbname=self.dbname, user=self.user,
                                      password=self.password, host='localhost')) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'insert into users (talent_id, blizzard_id) values (%s, %s) ON CONFLICT (talent_id) DO UPDATE SET blizzard_id = excluded.blizzard_id;',
                    (talent_id, blizzard_id,))
                conn.commit()

    def save_dota(self, steam_id, data):
        with closing(psycopg2.connect(dbname=self.dbname, user=self.user,
                                      password=self.password, host='localhost')) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'insert into dota_stats values (%s, %s) on conflict(steam_id) do update set stats_data = excluded.stats_data;',
                    (steam_id, json.dumps(data),))
                conn.commit()

    def save_overwatch(self, blizzard_id, data):
        with closing(psycopg2.connect(dbname=self.dbname, user=self.user,
                                      password=self.password, host='localhost')) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'insert into overwatch_stats values (%s, %s) on conflict(blizzard_id) do update set stats_data = excluded.stats_data;',
                    (blizzard_id, json.dumps(data),))
                conn.commit()

    def get_dota_stats(self, steam_id):
        with closing(psycopg2.connect(dbname=self.dbname, user=self.user,
                                      password=self.password, host='localhost')) as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT stats_data FROM dota_stats where steam_id = %s', (steam_id,))
                for row in cursor:
                    return row[0]

    def get_overwatch_stats(self, blizzard_id):
        with closing(psycopg2.connect(dbname=self.dbname, user=self.user,
                                      password=self.password, host='localhost')) as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT stats_data FROM overwatch_stats where blizzard_id = %s', (blizzard_id,))
                for row in cursor:
                    return row[0]


if __name__ == '__main__':
    pg = Postgress()
    # pg.create_user('7', '18', '23')
    print(pg.get_steam('123'))
    # print(pg.get_blizzard('7'))
    # pg.save_dota('178121778', {'1': 1})
    # print(pg.get_dota_stats('178121778'))
