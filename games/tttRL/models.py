from django.db import models
from django.db.models import CharField, TextField, DateTimeField, PositiveIntegerField
# from django.contrib.postgres.fields import *
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
import uuid
import datetime

# Create your models here.

class Games(models.Model):
	id = CharField(max_length=200, default=str(uuid.uuid4()), primary_key=True)
	ts = CharField(max_length=50, default=str(datetime.datetime.now()))
	game_state = CharField(max_length=20, default='IN_PROGRESS')
	winner = CharField(max_length=20, default='None')
	dimension = PositiveIntegerField(default=3)
	def __str__(self):
		return "Created game id : {} {} {} {} {}".format(
			self.id,
			self.ts,
			self.game_state,
			self.winner,
			self.dimension
			)

	class Meta:
		db_table = 'games'

class Moves(models.Model):
	id = CharField(max_length=200, default=str(uuid.uuid4()), primary_key=True)
	ts = CharField(max_length=50, default=str(datetime.datetime.now()))
	board = ArrayField(
		ArrayField(
			models.CharField(max_length=1),
			size=3,
			default=list,
			blank=True
			),
		size=3
		)
	game = models.ForeignKey(Games, on_delete=models.CASCADE)

	def __str__(self):
		return "{} {} {} {}".format(
			str(self.id),
			str(self.ts),
			str(self.game),
			str(self.board)
			)

	class Meta:
		db_table = 'moves'