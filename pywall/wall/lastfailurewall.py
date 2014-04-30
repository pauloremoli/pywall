#!-*- coding: utf8 -*-
from datetime import datetime

import pytz
from wall import Wall
from service.client import get_last_failure


class LastFailureWall(Wall):
	lastFailureInfo = []

	def __init__(self, canvas, jenkins):
		Wall.__init__(self, canvas)
		self.jenkins = jenkins

	def update_info(self):
		self.lastFailureInfo = get_last_failure(self.jenkins)

	def show(self):
		self.update_info()
		self.clear('#252525')
		broken_jobs = self.lastFailureInfo['broken_jobs']
		culprits = self.lastFailureInfo['culprits']

		if (broken_jobs):
			self.paint_broken_jobs(broken_jobs, culprits)
		else:
			last_failed = self.lastFailureInfo['last_failed']
			self.paint_last_failure(last_failed, culprits)

	def paint_broken_jobs(self, broken_jobs, culprits):
		message = 'PROJETO(S) COM ERRO:'
		for job in broken_jobs:
			message += '\n' + job

		message += '\n'
		message += '\nPOSSÍVEIS CULPADOS:'

		for culprit in culprits:
			message += '\n'
			message += culprit

		width = self.canvasWidth()
		height = self.canvasHeight()
		posX = width / 2
		posY = height / 2
		text_font = 'Arial 60 bold'
		self.canvas.create_text(posX, posY, text=message, font=text_font, fill='red', justify='center')

	def paint_last_failure(self, last_failure, culprits):
		without_failure = datetime.now(pytz.utc) - last_failure
		days = without_failure.days
		message = ''
		if (days > 0):
			message += str(days) + ' DIA(S) '
		hours = without_failure.seconds / 3600
		if (hours > 0):
			if (message):
				message += ', '
			message += str(hours) + ' HORA(S) '
		minutes = without_failure.seconds / 60 % 60
		if (minutes > 0):
			if (message):
				message += 'E '
			message += str(minutes) + ' MINUTO(S) '

		message = 'ESTAMOS HÁ\n' + message + '\nSEM FALHAS'

		width = self.canvasWidth()
		height = self.canvasHeight()
		posX = width / 2
		posY = height / 2
		text_font = 'Arial 70 bold'
		self.canvas.create_text(posX, posY, text=message, font=text_font, fill='green', justify='center')