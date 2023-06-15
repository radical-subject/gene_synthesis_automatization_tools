# encoding: utf-8
import os
from datetime import datetime

from loguru import logger as lgl
from pywinauto_recorder.player import *

PWD_LOG_FILES = r"."
SLEEP_TIME = 10
CURRENT_PORTION_SCALE_A = "29"
CURRENT_PORTION_SCALE_B = "29"


dt_mark = datetime.now().strftime("%c").replace(":", "_")

lgl.add(os.path.join(PWD_LOG_FILES, f"logged {dt_mark}.log"))

with UIPath("Taskbar||Pane"):
    with UIPath("Running applications||ToolBar"):
        lgl.debug("Clicking an app")
        click("Dr. Oligo||Button")

        lgl.debug(f"Waiting {SLEEP_TIME} seconds")
        time.sleep(SLEEP_TIME)

        lgl.debug("Sending keys: log-pass")
        send_keys("Administrator" "{VK_TAB}" "Admin1" "{ENTER}")

        lgl.debug(f"Logging done, waiting {SLEEP_TIME} seconds")
        time.sleep(SLEEP_TIME)

        lgl.debug("Chosing the inline-stated configuration file")
        send_keys(
            "{VK_TAB}"
            "{VK_TAB}"  # choosing list of files
            "{VK_DOWN}"
            "{VK_DOWN}"  # moving the selector tp the perticular one
            "{ENTER}"  # choosing the particular one
            "{VK_TAB}"
            "{VK_TAB}"  # going back to an 'Accept' button
            "{ENTER}"  # finally making the decision and closing form
        )

        lgl.debug(f"Done with configuration file, waiting {SLEEP_TIME * 2} seconds")
        time.sleep(SLEEP_TIME * 2)

        lgl.debug("Selecting 'Synth params' form")
        send_keys(
            "{VK_TAB}"
            "{VK_TAB}"
            "{VK_TAB}"
            "{VK_TAB}"
            "{VK_TAB}"  # long way of switches untill the correct panel 'Auto Synthesis Operation'
            "{VK_DOWN}"  # switch the selection frame to the correct panel when the selector is aimed
            "{VK_TAB}"
            "{VK_TAB}"  # switching between buttons
            "{ENTER}"  # chosing the form
        )

        lgl.debug("Filling up the form")
        send_keys(
            "{VK_TAB}"
            "{VK_TAB}"
            "{VK_TAB}"
            "{VK_TAB}"
            "{VK_TAB}"
            "{VK_TAB}"
            "{VK_TAB}"
            "{VK_TAB}"  # chosing the 'Scale A' line
        )
        lgl.debug(f"Setting 'Scale A' as {CURRENT_PORTION_SCALE_A} from a variable")
        send_keys(CURRENT_PORTION_SCALE_A)
        send_keys("{VK_TAB}")  # switching to 'Scale B'

        lgl.debug(f"Setting 'Scale B' as {CURRENT_PORTION_SCALE_B} from a variable")
        send_keys(CURRENT_PORTION_SCALE_B)
        send_keys(
            "{VK_TAB}"
            "{VK_TAB}"
            "{VK_TAB}"
            "{VK_TAB}"
            "{VK_TAB}"
            "{VK_TAB}"
            "{VK_TAB}"
            "{VK_TAB}"  # switching to 'Apply' button
            "{ENTER}"  # press down
        )
        lgl.debug("Form 'Synth params' is done")

        lgl.debug("Selecting 'Select protocol file' form")
        send_keys(
            "{VK_TAB}"
            "{VK_TAB}"
            "{VK_TAB}"
            "{VK_TAB}"
            "{VK_TAB}"
            "{VK_TAB}"  # selecting the 'Select protocol' line
            "{ENTER}"  # press down
        )

        lgl.debug("Filling up the form")
        send_keys(
            "{VK_TAB}"  # choose the frame with a list
            "{VK_LEFT}"  # don't know why we need this
            "{VK_DOWN}"
            "{VK_DOWN}"
            "{VK_DOWN}"  # chosing the inline-stated protocol file
            "{ENTER}"  # press down
        )
        lgl.debug("Form 'Select protocol' is done")

        lgl.debug(
            f"Done with run configuration, waiting {SLEEP_TIME * 2} seconds untill 'Select Oligos appear"
        )
        time.sleep(SLEEP_TIME * 2)

        lgl.debug("Selecting 'Select oligos' form")
        send_keys(
            "{VK_TAB}"
            "{VK_TAB}"
            "{VK_TAB}"
            "{VK_TAB}"
            "{VK_TAB}"
            "{VK_TAB}"
            "{VK_TAB}"
            "{VK_TAB}"  # selecting the button
            "{ENTER}"  # press down
        )

        lgl.debug("Inside 'Select Oligos' frame")
        lgl.debug("Selecting 'Select' button")
        send_keys("{VK_TAB}" "{ENTER}")  # simple switch

        lgl.success("Done!")

exit()
