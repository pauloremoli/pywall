#!-*- coding: utf8 -*-
class Wall(object):
	canvas = 0

	def __init__(self, canvas):
		self.canvas = canvas

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
