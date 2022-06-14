import lifx
import flic
import utils

logger = utils.init_log()

def button_event(bd_addr, click_type):
	logger.debug(f"{bd_addr} -> {click_type}")
	if bd_addr == "80:a3:d1:13:34:12":
		if click_type == "ClickType.ButtonHold":
			lifx.toggle("LIFX A19 1234")

flic.listen(button_event)