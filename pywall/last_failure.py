# -*- coding: utf-8 -*-
from Tkinter import Tk, Canvas, Frame, BOTH
from client import get_last_failure
from datetime import datetime	

class LastFailure(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)   		 
		self.parent = parent
		self.pack(fill=BOTH, expand=1)
		self.canvas = Canvas(self, bg="black",borderwidth=0,highlightthickness=0)	
		self.canvas.pack(fill=BOTH, expand=1)
		self.update_view()
	
	def clear_wall(self):
		#fill background
		rect = 0, 0, self.parent.winfo_screenwidth(), self.parent.winfo_screenheight() 
		self.canvas.create_rectangle(rect, outline='black', fill='black' ) 			
					 	
	def broken_jobs(self, broken_jobs, culprits):
		self.clear_wall()
		message = 'PROJETO(S) COM ERRO: '
		for job in broken_jobs:
			message += '\n' + job.name.upper()
		
		width = self.width
		height = self.height
		posX = width / 2
		posY = height / 2 - 100
		text_font= 'Arial 50 bold'
		self.canvas.create_text(posX, posY, text=message, font = text_font, fill='white')
			
	def last_failure(self, last_failure, culprits):
		
		self.clear_wall()
		
		without_failure = datetime.now() - last_failure		
		
		message = ''
		days = without_failure.days	
		if(days > 0):
			message += str(days) + ' DIA(S) '
		hours = without_failure.seconds / 3600
		if(hours > 0):
			if(message):
				message += 'E '
			message += str(hours) + ' HORA(S) '
		minutes = without_failure.seconds / 60 % 60
		if(minutes > 0):
			if(message):
				message += 'E '
			message += str(minutes) + ' MINUTO(S) ' 
		message_p1 = 'ESTAMOS HÁ'
		message_p2 = message
		message_p3 = 'SEM FALHAS'
		
		posX = self.width / 2
		posY = self.height / 2 - 100
		text_font = 'Arial 40 bold'
		self.canvas.create_text(posX, posY, text=message_p1, font= text_font, fill='white')
		self.canvas.create_text(posX, posY + 100, text=message_p2, font=text_font, fill='white')
		self.canvas.create_text(posX, posY + 200, text=message_p3, font=text_font, fill='white')  
		
		
	def update_view(self):
		self.width = self.parent.winfo_width()
		self.height = self.parent.winfo_height()
		if(self.width == 1 and self.height == 1):
			self.width = self.parent.winfo_screenwidth()
			self.height = self.parent.winfo_screenheight()
			
		result = get_last_failure()
		broken_jobs = result['broken_jobs']
		culprits = result['culprits']
		if(broken_jobs):
				self.broken_jobs(broken_jobs, culprits)
		else:
			last_failed = result['last_failed']
			self.last_failure(last_failed, culprits)
		self.parent.after(30000, self.update_view)
		
		
def main():
	root = Tk()
	root.overrideredirect(1)
	LastFailure(root)
	w, h = root.winfo_screenwidth(), root.winfo_screenheight()
	root.geometry("%dx%d+0+0" % (w, h))
	root.mainloop()

if __name__ == '__main__':
	main() 	