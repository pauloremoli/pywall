from Tkinter import Tk, Canvas, Frame, BOTH
from wall.jobwall import JobWall
from wall.scorewall import ScoreWall
from wall.lastfailurewall import LastFailureWall

class PyWallFrame(Frame):

	walls = []
	itWall = 0
	sec = 0

	def __init__(self, parent, views):
		Frame.__init__(self, parent)
		self.parent = parent
		self.pack(fill=BOTH, expand=1)
		self.canvas = Canvas(self, bg="black",borderwidth=0,highlightthickness=0)		
		self.canvas.pack(fill=BOTH, expand=1)
		self.createWalls(views)
		self.iterateWalls()

	def createWalls(self, views):
		jobWall = JobWall(self.canvas, views)
		scoreWall = ScoreWall(self.canvas)
		lastFailureWall = LastFailureWall(self.canvas)
		self.walls.append(jobWall)
		self.walls.append(scoreWall)
		self.walls.append(lastFailureWall)

	def iterateWalls(self):
		if(len(self.walls) == 0):
			return

		self.walls[self.itWall % len(self.walls)].show()
		self.sec += 5

		if(self.sec == 10):
			self.itWall += 1
			self.sec = 0

		self.parent.after(5000, self.iterateWalls)
