import logging

from pywall.funnycats.funnycats import FunnyCats
from pywall.funnycats.user import get_user_list_score
from wall import Wall


class ScoreWall(Wall):
	userListScore = []

	def __init__(self, canvas, jenkins_url, score_view, dbname):
		Wall.__init__(self, canvas, jenkins_url)

		self.funnycats = FunnyCats(self.jenkins, score_view, dbname)
		self.funnycats.init()

	def update_info(self):
		self.users_score = None
		try:
			if self.funnycats.is_connected() is False:
				raise Exception
			self.funnycats.update_view_score()
			self.users_score = get_user_list_score()
		except Exception, e:
			logging.error(e)
			self.error()

	def show(self):
		self.update_info()
		self.clear('#252525')

		if self.users_score is None:
			width = self.canvasWidth()
			height = self.canvasHeight()
			posX = width / 2
			posY = height / 2
			text_font = 'Arial 30 bold'
			message = "No user"
			self.canvas.create_text(posX, posY, text=message, font=text_font, fill='white', justify='center')
			return

		index = 1
		textFont = 'Arial 60 bold'
		textHeight = 90
		width = self.canvasWidth()
		height = self.canvasHeight()
		posX = width / 2

		textTotalHeight = textHeight * len(self.users_score)

		yInit = ((height - textTotalHeight) / 2) - (textHeight / 2)

		for user in self.users_score:
			nameStr = str(index) + '.    ' + user["name"]

			score = user["score"]
			scoreStr = str(score)

			posY = yInit + (index * textHeight)
			color = self.getColor(score, index, len(self.users_score))

			self.canvas.create_text(posX - 400, posY, text=nameStr, font=textFont, fill=color, justify='left',
			                        anchor='w')
			self.canvas.create_text(posX + 200, posY, text=scoreStr, font=textFont, fill=color, justify='left',
			                        anchor='w')

			index += 1

	def getColor(self, score, index, size):
		if (score < 0 or (size - index) < 3):
			return '#b30000'
		if (index == 1):
			return '#2ed800'
		return '#c6d800'