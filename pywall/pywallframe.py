from Tkinter import Canvas, Frame, BOTH

from wall.jobwall import JobWall
from wall.scorewall import ScoreWall
from wall.lastfailurewall import LastFailureWall
from service import jenkins_client


class PyWallFrame(Frame):
	walls = []
	itWall = 0
	sec = 0

	def __init__(self, parent, wall_views, score_view, dbname, jenkins_url):
		Frame.__init__(self, parent)
		self.parent = parent
		self.pack(fill=BOTH, expand=1)
		self.canvas = Canvas(self, bg="black", borderwidth=0, highlightthickness=0)
		self.canvas.pack(fill=BOTH, expand=1)
		self.jenkins = jenkins_client.get_jenkins(jenkins_url)
		self.create_walls(wall_views, score_view, dbname)
		self.iterate_walls()

	def create_walls(self, wall_views, score_view, dbname):
		if wall_views:
			jobWall = JobWall(self.canvas, self.jenkins, wall_views)
			self.walls.append(jobWall)
		if score_view and dbname:
			scoreWall = ScoreWall(self.canvas, self.jenkins, score_view, dbname)
			self.walls.append(scoreWall)
		lastFailureWall = LastFailureWall(self.canvas, self.jenkins)
		self.walls.append(lastFailureWall)

	def iterate_walls(self):
		if (len(self.walls) == 0):
			return

		self.walls[self.itWall % len(self.walls)].show()
		self.sec += 5

		if (self.sec == 10):
			self.itWall += 1
			self.sec = 0

		self.parent.after(5000, self.iterate_walls)
