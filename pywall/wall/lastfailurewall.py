#!-*- coding: utf8 -*-
from datetime import datetime
import logging

import pytz

from wall import Wall


class LastFailureWall(Wall):
	lastFailureInfo = []

	def __init__(self, canvas, jenkins):
		Wall.__init__(self, canvas, jenkins)


	def update_info(self):
		if self.jenkins is None:
			return False
		try:
			self.lastFailureInfo = self.jenkins.get_last_failure()
		except Exception, e:
			logging.error(e)
			return False

		return True

	def show(self):
		if self.update_info():
			self.clear('#252525')
			broken_jobs = self.lastFailureInfo['broken_jobs']
			culprits = self.lastFailureInfo['culprits']

			if (broken_jobs):
				self.paint_broken_jobs(broken_jobs, culprits)
			else:
				last_failed = self.lastFailureInfo['last_failed']
				self.paint_last_failure(last_failed, culprits)
		else:
			self.error()

	def paint_broken_jobs(self, broken_jobs, culprits):
		message = 'PROJETO(S) COM ERRO:'
		for job in broken_jobs:
			message += '\n' + job

		if(len(culprits) != 0):
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