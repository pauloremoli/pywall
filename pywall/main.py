#!-*- coding: utf8 -*-
import sys
from Tkinter import Tk
from pywallframe import PyWallFrame

if __name__ == '__main__':
	if(len(sys.argv) > 1):
		print sys.argv
		args = sys.argv
		del args[0]
		root = Tk()
		PyWallFrame(root, args)
		root.geometry("%dx%d+0+0" % root.maxsize())
		root.mainloop()