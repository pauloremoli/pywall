# -*- coding: utf-8 -*-
from Tkinter import Tk, Canvas, Frame, BOTH
from client import  get_view_status
import sys


class Wall(Frame):

	view = 0
	views = []

	def __init__(self, parent, views):
		Frame.__init__(self, parent)   		 
		self.parent = parent
		self.pack(fill=BOTH, expand=1)
		self.canvas = Canvas(self, bg="black",borderwidth=0,highlightthickness=0)		
		self.canvas.pack(fill=BOTH, expand=1)		
		self.views = views
		self.update_view()
		

	def clear_wall(self):
		#fill background
		rect = 0, 0, self.width, self.height 
		self.canvas.create_rectangle(rect, outline='black', fill='black' ) 			
		
	def draw_jobs(self, jobs):
		
			if(len(jobs) >= 4):
				sizeColumns = 4
			else:
				sizeColumns = len(jobs)
			
			sizeLines = int((len(jobs) / 4) + 1)
			
			#Rect dimension
			default_offset = 2
			size_w = (self.width - (sizeColumns * default_offset) ) / sizeColumns
			size_h = (self.height - (sizeLines * default_offset) ) / sizeLines			
			
			counter = 0 		
			line = 0
			offsetX = 0
			offsetY = 0
			temp = 0			
			
			self.clear_wall()
			
			for job in jobs:				
				#Choose color for each build status
				color = 'white'
				if(job['last_build'] == None):
					color = 'grey50'
				elif(job['status'] == 'SUCCESS'):
					color = 'SpringGreen4'
				elif(job['status'] == 'FAILURE'):
					color = 'red'
				elif(job['status'] == 'ABORTED'):
					color = 'dark sea green'
				elif(job['status'] == 'BUILDING'):
					color = 'dark green'
					
				#Limits of 4 jobs per line 	
				if(counter != 0 and counter % 4 == 0):
					line += 1			
					offsetX = 0
					offsetY += default_offset
					temp = 0
				
				#Calculate position rect position
				x = temp * size_w
				y = line * size_h
				offsetX += default_offset	
				
				#Applies offset to separate the rects
				rect = x + offsetX, y + offsetY, x + offsetX + size_w, y + offsetY + size_h
				
				#Creates the rect
				self.canvas.create_rectangle(rect, outline='black', fill=color )	
				
				posX = x + offsetX + (size_w / 2)
				posY = y + offsetY+ (size_h / 2)
				
				self.canvas.create_text(posX, posY, text=job['project'], font= 'Arial 20 bold', fill='white')  
  				
				
				temp += 1
				counter += 1

	def update_view(self):

		jobs = get_view_status(self.views[self.view % len(self.views)])
		self.view = self.view + 1
		self.width = self.parent.winfo_width()
		self.height = self.parent.winfo_height()
		if(self.width == 1 and self.height == 1):
			self.width = self.parent.winfo_screenwidth()
			self.height = self.parent.winfo_screenheight()
		if(jobs):
			self.draw_jobs(jobs)
		self.parent.after(5000, self.update_view)


if __name__ == '__main__':

	if(len(sys.argv) > 1):
		print sys.argv
		args = sys.argv
		del args[0]
		root = Tk()
		Wall(root, args)
		w, h = root.winfo_screenwidth(), root.winfo_screenheight()
		root.geometry("%dx%d+0+0" % (w, h))
		root.mainloop()
