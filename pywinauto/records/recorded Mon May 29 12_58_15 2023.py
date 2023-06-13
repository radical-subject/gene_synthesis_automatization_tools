# encoding: utf-8

from pywinauto_recorder.player import *


with UIPath(u"Program Manager||Pane"):
	with UIPath(u"Desktop||List"):
		double_click(u"New Text Document.txt||ListItem")

with UIPath(u"New Text Document.txt - Notepad||Window"):
	with UIPath(u"||TitleBar"):
		click(u"Close||Button")
