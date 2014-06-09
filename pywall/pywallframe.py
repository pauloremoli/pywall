from Tkinter import Canvas, Frame, BOTH
import logging

from pywall.service.jenkins_client import JenkinsClient
from wall.jobwall import JobWall
from wall.funnycatswall import FunnyCatsWall
from wall.lastfailurewall import LastFailureWall


class PyWallFrame(Frame):
	walls = []
	itWall = 0
	sec = 0

	def __init__(self, parent, wall_views, score_view, dbname, jenkins_url):
		Frame.__init__(self, parent)
		self.parent = parent
		self.pack(fill=BOTH, expand=1)
		self.canvas = Canvas(self, bg="black", borderwidth=0, highlightthickness=0)
		self.jenkins_url = jenkins_url
		self.canvas.pack(fill=BOTH, expand=1)
		if self.create_walls(wall_views, score_view, dbname):
			self.iterate_walls()


	def create_walls(self, wall_views, score_view, dbname):
		jenkins = self.get_client()

		if wall_views:
			jobWall = JobWall(self.canvas, jenkins, wall_views)
			self.walls.append(jobWall)
		if score_view and dbname:
			scoreWall = FunnyCatsWall(self.canvas, jenkins, score_view, dbname)
			self.walls.append(scoreWall)
		lastFailureWall = LastFailureWall(self.canvas, jenkins)
		self.walls.append(lastFailureWall)

		return True

	def iterate_walls(self):
		if (len(self.walls) == 0):
			return

		wall = self.walls[self.itWall % len(self.walls)]
		wall.show()
		self.sec += 5

		if (self.sec == 10):
			self.itWall += 1
			self.sec = 0

		self.parent.after(5000, self.iterate_walls)


	def get_client(self):
		try:
			return JenkinsClient(self.jenkins_url)
		except Exception, e:
			logging.error(e)
			return None