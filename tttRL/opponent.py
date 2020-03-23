from .players import *
import random

class Opponent():

	def __init__(self, strategy='RANDOM'):
		self.strategy = strategy

	def random_scorer(self, board, symbol):
		empty_slots = []
		for i in range(len(board)):
			for j in range(len(board)):
				if board[i][j] == "":
					empty_slots.append((i,j))
		print(empty_slots)
		idx = random.randint(0, len(empty_slots))
		fill_x = empty_slots[idx][0]
		fill_y = empty_slots[idx][1]
		board[fill_x][fill_y] = symbol
		return board

	def score(self, board, symbol):
		# Insert awesome strategy here
		if self.strategy == 'RANDOM':
			return self.random_scorer(board, symbol)
