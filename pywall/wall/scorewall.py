import operator
from wall import Wall
from service.client import get_user_list_score

class ScoreWall(Wall):
	
	userListScore = []

	def __init__(self, canvas):
		Wall.__init__(self, canvas)
		
	def updateInfo(self):
		self.usersListScore = get_user_list_score()
		self.usersListScore.sort(key=operator.itemgetter('score'), reverse=True)

	def show(self):
		self.updateInfo()
		self.clear('#252525')

		index = 1
		textFont = 'Arial 60 bold'
		textHeight = 90
		width = self.canvasWidth()
		height = self.canvasHeight()
		posX = width / 2

		textTotalHeight = textHeight * len(self.usersListScore)

		yInit = ((height - textTotalHeight) / 2) - (textHeight / 2)

		for user in self.usersListScore:
			nameStr = str(index) + '.    ' + str(user["name"])
			score = user["score"]
			scoreStr = str(score)

			posY = yInit + (index * textHeight)
			color = self.getColor(score, index, len(self.usersListScore))

			self.canvas.create_text(posX - 400, posY, text=nameStr, font= textFont, fill=color, justify='left', anchor='w')
			self.canvas.create_text(posX + 200, posY, text=scoreStr, font= textFont, fill=color, justify='left', anchor='w')

			index += 1

	def getColor(self, score, index, size):
		if(score < 0 or (size - index) < 3):
			return '#b30000'
		if(index == 1):
			return '#2ed800'
		return '#c6d800'