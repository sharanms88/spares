from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
import uuid

# Models
from .models import Games, Moves
from .game_utils import *
from .MoveAction import MoveAction
from .players import *

@csrf_exempt 
def index(request):
    return HttpResponse("Hello, Sharan")

@csrf_exempt 
def create(request, **kwargs):
	params = dict(request.POST)
	# create a new game id 
	game_id, created_at = str(uuid.uuid4()), datetime.datetime.now()
	while is_game_exists(game_id):
		game_id, created_at = str(uuid.uuid4()), datetime.datetime.now()
	params = dict(request.POST)
	board_dimension = params['board_dimension'] if 'board_dimension' in params else [DEFAUT_BOARD_DIMENSION]
	# game = Games(id=game_id, ts=created_at, game_state='IN_PROGRESS', dimension=int(board_dimension[0]))
	# game.save()
	response_data = {
		'game_id' : game_id,
		'ts' : created_at
	}
	return JsonResponse(response_data)

@csrf_exempt
def play(request, game_id, **kwargs):
	"""
	Lookup a game in progress and play a move
	args:
		game_id: id of the game being played
	"""
	game = retieve_game(game_id)
	params = dict(request.POST)

	if game == None:
		return JsonResponse(
			{'message' : 'Game {} does not exist. Please create a game before playing'.format(
				game_id)})
	if game.game_state == 'COMPLETED':
		return JsonResponse(
			{'message' : 'Game {} completed. Please create a game'.format(
				game_id)})
	print("Continuing game {} ".format(game_id))

	print("coords are  : ", params['coords'][0])	
	if not(params.get('coords') and len(params.get('coords')[0].split(',')) == 2):
		return JsonResponse(
			{'message' : 'Invalid arguments {}'.format(params)})

	coords = [int(i) for i in params.get('coords')[0].split(',')]
	ma = MoveAction(game=game, coords=coords, player=PLAYER1)
	
	if not ma.check_valid_move():
		return JsonResponse({'message' : 'Invalid move coordinates'})
	updated_board, state, winner = ma.apply_move_and_respond()
	response_data = {
		'ts' : datetime.datetime.now().time(),
		'game_id' : game_id,
		'board' : updated_board,
		'game_state' : state,
		'winner' : winner
		}
	return JsonResponse(response_data)

