#!-*- coding: utf8 -*-

from Tkinter import Tk

import click
from pywallframe import PyWallFrame


@click.command()
@click.option('--jenkins_url', required=True, help='Jenkins server URL')
@click.option('--wall_views', help='Views to be displayed in wall', multiple=True)
@click.option('--score_view', help='Views to be displayed in wall')
@click.option('--dbname', help='Database name')
def pywall(jenkins_url, wall_views, score_view, dbname):
	root = Tk()
	PyWallFrame(root, wall_views, score_view, dbname, jenkins_url)
	root.geometry("%dx%d+0+0" % root.maxsize())
	root.mainloop()


if __name__ == '__main__':
	pywall()
