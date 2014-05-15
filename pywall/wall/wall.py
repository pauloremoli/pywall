#!-*- coding: utf8 -*-
import logging

from pywall.service.jenkins_client import JenkinsClient


class Wall(object):
	canvas = 0

	def __init__(self, canvas, jenkins_url):
		self.canvas = canvas
		self.jenkins = None
		try:
			self.jenkins = JenkinsClient(jenkins_url)
		except Exception, e:
			self.error()
			logging.error(e)

	def show(self):
		raise Exception("Unimplemented Method")

	def update_info(self):
		raise Exception("Unimplemented Method")

	def clear(self, color):
		#fill background
		rect = 0, 0, self.canvas.winfo_screenwidth(), self.canvas.winfo_screenheight()
		self.canvas.create_rectangle(rect, outline='black', fill=color)

	def canvasWidth(self):
		width = self.canvas.winfo_width()
		if (width == 1):
			width = self.canvas.winfo_screenwidth()
		return width

	def canvasHeight(self):
		height = self.canvas.winfo_height()
		if (height == 1):
			height = self.canvas.winfo_screenheight()
		return height

	def error(self):
		self.clear('black')
		width = self.canvasWidth()
		height = self.canvasHeight()
		posX = width / 2
		posY = height / 2
		text_font = 'Arial 30 bold'
		message = "No connection with the server"
		self.canvas.create_text(posX, posY, text=message, font=text_font, fill='white', justify='center')