from .models import *

def is_game_exists(game_id):
	if Games.objects.filter(id=game_id) is None:
		return True
	return False

def retieve_game(game_id):
	game = Games.objects.filter(id=game_id)
	if game is not None and len(game) > 0:
		return game[0]
	return game