# encoding: utf-8

from pywinauto_recorder.player import *


with UIPath(u"Taskbar||Pane"):
	with UIPath(u"Running applications||ToolBar"):
		click(u"Dr. Oligo||Button")
		send_keys("{VK_SHIFT down}""{VK_SHIFT down}""{VK_SHIFT down}""{VK_SHIFT down}""{VK_SHIFT down}""{A down}""{VK_SHIFT up}""{a up}dministrator""{tab}""{VK_SHIFT down}""{A down}""{VK_SHIFT up}""{a up}dmin1""{ENTER}""{tab}""{tab}""{down}""{down}""{ENTER}""{tab}""{tab}""{ENTER}""{tab}""{tab}""{tab}""{tab}""{tab}""{down}""{tab}""{tab}""{ENTER}""{tab}""{tab}""{tab}""{tab}""{tab}""{up}""{tab}""{tab}""{tab}28""{tab}28""{tab}""{tab}""{tab}""{tab}""{tab}""{tab}""{tab}""{tab}""{tab}""{tab}""{ENTER}""{tab}""{tab}""{tab}""{tab}""{tab}""{tab}""{ENTER}""{tab}""{left}""{down}""{down}""{down}""{ENTER}""{tab}""{tab}""{tab}""{tab}""{tab}""{tab}""{tab}""{tab}""{ENTER}""{tab}""{ENTER}""{VK_CONTROL down}""{VK_MENU}""{VK_LWIN}""{VK_CONTROL up}")
