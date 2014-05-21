# -*- coding: utf-8 -*-
import logging

from wall import Wall


class JobWall(Wall):
	views = []
	itView = 0
	jobs = []
	default_offset = 5
	jobWidth = 0
	jobHeight = 0

	def __init__(self, canvas, jenkins_url, views):
		Wall.__init__(self, canvas, jenkins_url)
		self.views = views

	def update_info(self):
		if (self.jenkins is None):
			self.error()
			return
		try:
			view_index = self.itView % len(self.views)
			self.jobs = self.jenkins.get_view_status(self.views[view_index])
			self.itView += 1
		except Exception, e:
			logging.error(e)

	def show(self):
		self.update_info()
		self.clear('black')
		self.draw_jobs(self.jobs)

	def paintJob(self, job, rect):
		name = job['project']
		buildNumber = job['last_build']
		status = job['status']
		previousBuildStatus = job['previousBuildStatus']

		#Choose color for each build status
		color = '#3c3c3c'
		buildNumberColor = '#559758'

		if (job['last_build'] is None or job['status'] == 'ABORTED'):
			color = '#3c3c3c'
			buildNumberColor = '#979797'
		elif (job['status'] == 'SUCCESS'):
			color = '#006500'
		elif (job['status'] == 'FAILURE'):
			color = '#8d1000'
			buildNumberColor = '#fa8b87'
		elif (job['status'] == 'BUILDING'):
			if (previousBuildStatus == 'FAILURE'):
				color = '#8d1000'
			else:
				color = '#002f00'

		#Creates the rect
		self.canvas.create_rectangle(rect, outline='black', fill=color)
		posX = rect[0] + (self.jobWidth / 2)
		posY = rect[1] + (self.jobHeight / 2)

		nameFont = 'Arial 40 bold'
		buildNumberFont = 'Arial 20 bold'

		if (status == 'BUILDING'):
			color = '#006500'
			completeRate = job['completeRate']
			rectWidth = (self.jobWidth * completeRate) / 100
			completeRateText = 'Building... ' + str(int(round(completeRate))) + '%'
			self.canvas.create_rectangle(rect[0], rect[1], rect[0] + rectWidth, rect[3], outline='black', fill=color)
			self.canvas.create_text(posX, posY - (self.jobHeight / 2) + 30, text=completeRateText, font=buildNumberFont,
			                        fill='white', justify='center')

		if (buildNumber is not None):
			buildNumber = '#' + str(buildNumber)
			xCorner = posX - (self.jobWidth / 2) + 10
			yCorner = posY + (self.jobHeight / 2) - 20
			self.canvas.create_text(xCorner, yCorner, text=buildNumber, font=buildNumberFont, fill=buildNumberColor,
			                        anchor='w')

		self.canvas.create_text(posX + 3, posY + 3, text=name, font=nameFont, fill='black', justify='center',
		                        width=self.jobWidth)
		self.canvas.create_text(posX, posY, text=name, font=nameFont, fill='white', justify='center',
		                        width=self.jobWidth)


	def draw_jobs(self, jobs):
		if jobs is None or len(jobs) is 0:
			self.error()
			return
		if (len(jobs) >= 4):
			sizeColumns = 4
		else:
			sizeColumns = len(jobs)

		sizeLines = int((len(jobs) / 4))

		if (len(jobs) % 4 != 0):
			sizeLines += 1

		#Rect dimension
		self.jobWidth = (self.canvasWidth() - (sizeColumns * self.default_offset) ) / sizeColumns
		self.jobHeight = (self.canvasHeight() - (sizeLines * self.default_offset) ) / sizeLines

		counter = 0
		line = 0
		offsetX = 0
		offsetY = 0
		temp = 0

		for job in jobs:
			#Limits of 4 jobs per line 	
			if (counter != 0 and counter % 4 == 0):
				line += 1
				offsetX = 0
				offsetY += self.default_offset
				temp = 0

			#Calculate position rect position
			x = temp * self.jobWidth
			y = line * self.jobHeight
			offsetX += self.default_offset

			#Applies offset to separate the rects
			rect = x + offsetX, y + offsetY, x + offsetX + self.jobWidth, y + offsetY + self.jobHeight

			self.paintJob(job, rect)

			temp += 1
			counter += 1