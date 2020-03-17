import uuid, random
import numpy as np
from .models import *
from .game_utils import *
from .players import *
from .opponent import Opponent

class MoveAction():
	def __init__(self, game, coords, player='player1'):
		self.game = game
		self.coords = coords
		self.player = player
		self.previous_moves = Moves.objects.filter(game_id=self.game.id)
		self.model = Opponent()

	def check_valid_move(self):
		"""
		Dum dum dum
		"""
		# Ensure the moves are within scope
		for axis_coord in self.coords:
			if axis_coord > self.game.dimension - 1:
				print("Invalid dimensions")
				return False

		# Ensure it's not over riding a previously tplayed on location
		
		for previous_move in self.previous_moves:
			board = previous_move.board
			if len(board) != self.game.dimension:
				return False

			if len(board[self.coords[0]]) != self.game.dimension:
				return False

			if board[self.coords[0]][self.coords[1]] != '':
				return False

		print("Checking {} moves for game {}".format(len(self.previous_moves), self.game.id))
		print("It's a valid move!")
		return True

	@staticmethod
	def check_winner(board):
		"""
		Did anyone win?
		"""
		DIM = len(board)
		winner = None
		for row in board:
			if len(set(row)) == 1 and '' not in row:
				winner = row[0]

		for row in np.transpose(board):
			print(row)
			if len(set(row)) == 1 and '' not in row:
				winner = row[0]
			print("winner is ", winner)

		left_diag = [board[i][i] for i in range(len(board))]
		if len(set(left_diag)) == 1 and '' not in left_diag:
			winner = board[0][0]

		right_diag = [board[i][len(board)-i-1] for i in range(len(board))]
		if len(set(right_diag)) == 1 and '' not in right_diag:
			winner = board[0][len(board)-1]

		winning_player = None
		if winner == 'x':
			winning_player = PLAYER1
		elif winner == 'o':
			winning_player = PLAYER2
		return winning_player

	def get_updated_board(self):
		"""
		Update the latest board setting with the current move
		"""
		ordered_moves = Moves.objects.filter(game_id=self.game.id).order_by('-ts')
		if len(ordered_moves) == 0:
			latest_board = [['' for i in range(self.game.dimension)] for j in range(self.game.dimension)]
		else:
			latest_board = ordered_moves[0].board

		updated_board = latest_board.copy()
		if self.player == PLAYER1:
			updated_board[self.coords[0]][self.coords[1]] = 'x'
		else:
			updated_board[self.coords[0]][self.coords[1]] = 'o'
		return updated_board

	def update_game(self, winner):
		"""
		Update the state of the game (if required) based on the latest move
		"""
		Games.objects.filter(id=self.game.id).update(game_state='COMPLETED', winner=winner)

	def apply_move(self):
		"""
		Generate a new move object and store the log in db
		"""
		updated_board = self.get_updated_board()
		winner = self.check_winner(updated_board)
		if winner:
			# TODO shaz: add winner to game model obj
			self.update_game(winner)
			print("Game {} Over!".format(self.game.id))
		new_move = Moves(id=uuid.uuid4(), board=updated_board, game_id=self.game.id)
		new_move.save()
		state = Games.objects.filter(id=self.game.id)[0].game_state
		return updated_board, state, winner

	def apply_move_and_respond(self):
		"""
		Generate a new move object and respond with a algorithmic move
		Store both in db
		"""
		updated_board = self.get_updated_board()
		winner = self.check_winner(updated_board)
		if winner:
			# TODO shaz: add winner to game model obj
			self.update_game(winner)
		new_move = Moves(id=uuid.uuid4(), 
			ts=str(datetime.datetime.now()),
			board=updated_board, 
			game_id=self.game.id)
		new_move.save()
		
		if not winner:
			symbol = 'o' if self.player == PLAYER1 else 'x'
			updated_board_with_response = self.model.score(updated_board, symbol)
			winner = self.check_winner(updated_board_with_response)
			if winner:
				self.update_game(winner)
			response_move = Moves(id=uuid.uuid4(), 
				board=updated_board, 
				ts=str(datetime.datetime.now()),
				game_id=self.game.id)
			response_move.save()

			state = Games.objects.filter(id=self.game.id)[0].game_state
			return updated_board_with_response, state, winner

		state = Games.objects.filter(id=self.game.id)[0].game_state
		return updated_board, state, winner


