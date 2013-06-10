# -*- coding: utf-8 -*-
from Tkinter import Tk, Canvas, Frame, BOTH
from jenkinsapi.api import Jenkins
from jenkinsapi.build import Build
from jenkinsapi.job import Job
from client import get_jobs_status
import math
import threading



class Wall(Frame):
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
		
	def draw_jobs(self, jobs):
		
			if(len(jobs) >= 4):
				sizeColumns = 4
			else:
				sizeColumns = len(jobs)
			
			sizeLines = int((len(jobs) / 4) + 1)
			
			#Rect dimension
			default_offset = 10
			size_w = (self.parent.winfo_screenwidth() - (sizeColumns * 10) ) / sizeColumns
			size_h = (self.parent.winfo_screenheight() - (sizeLines * 10) ) / sizeLines			
			
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
				
				self.canvas.create_text(posX, posY, text=job['project'], font= 'Arial 38 bold', fill='white')  
				
				
				temp += 1
				counter += 1

	def update_view(self):
		jobs = get_jobs_status()
		if(jobs):
			self.draw_jobs(jobs)
		self.parent.after(60000, self.update_view)

	
def main():
	root = Tk()
	Wall(root)
	w, h = root.winfo_screenwidth(), root.winfo_screenheight()
	root.geometry("%dx%d+0+0" % (w, h))
	root.mainloop()

if __name__ == '__main__':
	main()