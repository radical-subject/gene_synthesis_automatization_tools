# encoding: utf-8

import time

from pywinauto_recorder.player import *


with UIPath(u"Taskbar||Pane"):
	with UIPath(u"Running applications||ToolBar"):
		click(u"Dr. Oligo||Button")

		print("-" * 30, "SLEEPING")
		time.sleep(5)

		send_keys("{VK_SHIFT down}""{A down}""{VK_SHIFT up}""{a up}dministrator""{tab}""{VK_SHIFT down}""{A down}""{VK_SHIFT up}""{a up}dmin1")

with UIPath(u"Dr. Oligo Log on...||Window"):
	click(u"")

with UIPath(u"Configuration File Selection...||Window"):
	double_click(u"")

with UIPath(u"Dr. Oligo Control System v6.1.0.66, S/N BLP-XLC-5088, Administrator ||Window"):
	click(u"")
	drag_and_drop(u"", u"")
	drag_and_drop(u"", u"")
	click(u"")
	click(u"")

with UIPath(u"||Pane#[0,0]"):
	double_click(u"")

with UIPath(u"Dr. Oligo Control System v6.1.0.66, S/N BLP-XLC-5088, Administrator ||Window"):
	click(u"")
	click(u"")
	drag_and_drop(u"", u"")
	click(u"")
	click(u"")
	click(u"")
	send_keys("{VK_SHIFT down}""{VK_SHIFT down}""{VK_SHIFT down}""{VK_SHIFT down}""{VK_SHIFT down}""{VK_SHIFT down}""{VK_SHIFT down}""{VK_SHIFT down}""{VK_SHIFT down}""{VK_SHIFT down}""{VK_SHIFT down}""{VK_SHIFT down}""{VK_SHIFT down}""{VK_SHIFT down}""{VK_SHIFT down}""{VK_SHIFT}""{VK_SHIFT down}""{P down}""{L down}""{P up}""{VK_SHIFT up}""{l up}a""{t down}""{e down}""{t up}""{e up}""{VK_SHIFT down}_""{VK_SHIFT up}a")
	send_keys("{VK_SHIFT down}""{backspace}""{A down}""{VK_SHIFT up}""{a up}")
	click(u"")

with UIPath(u"Non-Standard Base Assignment||Window"):
	click(u"")
	click(u"")

with UIPath(u"Dr. Oligo Control System v6.1.0.66, S/N BLP-XLC-5088, Administrator ||Window"):
	click(u"")
	send_keys("{VK_SHIFT down}OVFF""{VK_SHIFT up}")
	send_keys("364.txt""{ENTER}")

with UIPath(u"||Window"):
	click(u"")
	send_keys("{VK_SHIFT down}OVFF""{VK_SHIFT up}")

with UIPath(u"Store Synthesis Run file as: \n(.txt extension added automatically)||Window"):
	click(u"")
	click(u"OK||Button")

with UIPath(u"Dr. Oligo Control System v6.1.0.66, S/N BLP-XLC-5088, Administrator ||Window"):
	click(u"")

with UIPath(u"||Window"):
	click(u"")
	click(u"")
