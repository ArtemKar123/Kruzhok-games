drop table if exists dota_stats;
drop table if exists overwatch_stats;
drop table if exists users;

create table if not exists users(
	talent_id varchar primary key,
	steam_id varchar default '',
	blizzard_id varchar default ''
);

create table if not exists dota_stats(
	steam_id varchar unique,
	stats_data json
);

create table if not exists overwatch_stats(
	blizzard_id varchar unique,
	stats_data json
);