from sqlalchemy import Column, Integer, String, ForeignKey, Float
# from sqlalchemy.orm import relationship
#----- custom imports ------+
from services.sql.sql_alchemy_utility import Base 

class Player(Base):
	__tablename__ = 'players_new'
	
	id = Column(Integer, primary_key=True)
	name = Column(String(50))
	team_id = Column(Integer, ForeignKey('teams_new.id'))
	baseball_reference_url = Column(String(100))
	pitcher = Column(Integer)

	def __init__(self, name, team_id, baseball_reference_url, pitcher):
		self.name = name
		self.team_id = team_id
		self.baseball_reference_url = baseball_reference_url 
		self.pitcher = pitcher


class Team(Base):
	__tablename__ = 'teams_new'

	id = Column(Integer, primary_key=True)
	name = Column(String(50))
	league = Column(String(40))
	division = Column(String(40))
	baseball_reference_url = Column(String(100))
	logo_name = Column(String(40))

	def __init__(self, name, league, division, baseball_reference_url, logo_name):
		self.name = name
		self.league = league
		self.division = division
		self.baseball_reference_url = baseball_reference_url 
		self.logo_name = logo_name


class PitchingPlayerStats(Base):
	__tablename__ = 'pitching_player_stats'
	
	id = Column(Integer, primary_key=True)
	player_id = Column(Integer, ForeignKey('players_new.id'))
	wins = Column(Integer)
	losses = Column(Integer)
	win_loss_perc = Column(Float)
	earned_run_avg = Column(Float)
	games_started = Column(Integer)
	games_finished = Column(Integer)
	complete_games = Column(Integer)
	shutouts = Column(Integer)
	saves = Column(Integer)
	innings_pitched = Column(Integer)
	hits_allowed = Column(Integer)
	runs_allowed = Column(Integer)
	earned_runs = Column(Integer)
	home_runs_allowed = Column(Integer)
	walks_allowed = Column(Integer)
	intentional_walks = Column(Integer)
	strikeouts_recorded = Column(Integer)
	hit_batters = Column(Integer)
	balks = Column(Integer)
	wild_pitches = Column(Integer)
	batters_faced = Column(Integer)
	adjusted_era_plus = Column(Float)
	fielding_ind_pitching = Column(Float)
	walks_hits_per_nine = Column(Float)
	hits_per_nine = Column(Float)
	homeruns_per_nine = Column(Float)
	walks_per_nine = Column(Float)
	strikeouts_per_nine = Column(Float)
	strikeout_walk_ratio = Column(Float)

	def __init__(self, **kwargs):
		self.id = kwargs.get('id', None)
		self.player_id = kwargs.get('player_id', None)
		self.wins = kwargs.get('wins', None)
		self.losses = kwargs.get('losses', None)
		self.win_loss_perc = kwargs.get('win_loss_perc', None)
		self.earned_run_avg = kwargs.get('earned_run_avg', None)
		self.games_started = kwargs.get('games_started', None)
		self.games_finished = kwargs.get('games_finished', None)
		self.complete_games = kwargs.get('complete_games', None)
		self.shutouts = kwargs.get('shutouts', None)
		self.saves = kwargs.get('saves', None)
		self.innings_pitched = kwargs.get('innings_pitched', None)
		self.hits_allowed = kwargs.get('hits_allowed', None)
		self.runs_allowed = kwargs.get('runs_allowed', None)
		self.earned_runs = kwargs.get('earned_runs', None)
		self.home_runs_allowed = kwargs.get('home_runs_allowed', None)
		self.walks_allowed = kwargs.get('walks_allowed', None)
		self.intentional_walks = kwargs.get('intentional_walks', None)
		self.strikeouts_recorded = kwargs.get('strikeouts_recorded', None)
		self.hit_batters = kwargs.get('hit_batters', None)
		self.balks = kwargs.get('balks', None)
		self.wild_pitches = kwargs.get('wild_pitches', None)
		self.batters_faced = kwargs.get('batters_faced', None)
		self.adjusted_era_plus = kwargs.get('adjusted_era_plus', None)
		self.fielding_ind_pitching = kwargs.get('fielding_ind_pitching', None)
		self.walks_hits_per_nine = kwargs.get('walks_hits_per_nine', None)
		self.hits_per_nine = kwargs.get('hits_per_nine', None)
		self.homeruns_per_nine = kwargs.get('homeruns_per_nine', None)
		self.walks_per_nine = kwargs.get('walks_per_nine', None)
		self.strikeouts_per_nine = kwargs.get('strikeouts_per_nine', None)
		self.strikeout_walk_ratio = kwargs.get('strikeout_walk_ratio', None)
	

class PitchingStats(Base):

	__tablename__ = 'pitching_stats'
	id = Column(Integer, primary_key=True)
	name = Column(String(30))

	def __init__(self, name):
		self.name = name
