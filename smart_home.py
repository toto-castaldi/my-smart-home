import fliclib
import lifx
import utils
import config
import lifxlan
import traceback

logger = utils.init_log()
c = config.get_config()
ligths_lan = lifxlan.LifxLAN(None)
client = fliclib.FlicClient("localhost")
MAX_POWER = 65535
devices = {

}

def wrapped_toggle_lifx(action_id):
	try:
		device = None
		if action_id in devices:
			device = devices[action_id]
		else:
			device = ligths_lan.get_device_by_name(action_id)
		if device:
			devices[action_id] = device
			current_power = device.get_power()
			device.set_power(0 if current_power == MAX_POWER else MAX_POWER, rapid=True)
		else:
			logger.warning(f"unknow device by name {action_id}")
	except:
		traceback.print_exc()

def wrapped_down_lifx(action_id):
	try:
		device = None
		if action_id in devices:
			device = devices[action_id]
		else:
			device = ligths_lan.get_device_by_name(action_id)
		if device:
			devices[action_id] = device
			current_brightness = device.get_color()[2]
			logger.debug(current_brightness)
			device.set_brightness(current_brightness - 12000 if current_brightness >= 12000 else 0, rapid=True)
		else:
			logger.warning(f"unknow device by name {action_id}")
	except:
		traceback.print_exc()

def wrapped_up_lifx(action_id):
	try:
		device = None
		if action_id in devices:
			device = devices[action_id]
		else:
			device = ligths_lan.get_device_by_name(action_id)
		if device:
			device = ligths_lan.get_device_by_name(action_id)
			current_brightness = device.get_color()[2]
			logger.debug(current_brightness)
			device.set_brightness(current_brightness + 12000 if current_brightness < (MAX_POWER - 12000) else MAX_POWER, rapid=True)
		else:
			logger.warning(f"unknow device by name {action_id}")
	except:
		traceback.print_exc()

actions = {
	"toggle-lifx" : wrapped_toggle_lifx,
	"down-lifx" : wrapped_down_lifx,
	"up-lifx" : wrapped_up_lifx
}

def on_button_single_or_double_click_or_hold(channel, click_type, was_queued, time_diff):
	bd_addr = channel.bd_addr
	c_type = str(click_type)
	logger.info(f"{bd_addr} -> {c_type}")
	button = config.search_button(bd_addr)
	if button is not None:
		action = config.search_action(button, c_type)
		if action is not None:
			logger.debug(action)
			actions[action["action"]](action["action_id"])
		else:
			logger.warning(f"unknow {c_type} action on button {bd_addr}")	
	else:
		logger.warn(f"unknow {bd_addr} button")

def got_button(bd_addr):
	cc = fliclib.ButtonConnectionChannel(bd_addr)
	cc.on_button_single_or_double_click_or_hold = on_button_single_or_double_click_or_hold
	cc.on_connection_status_changed = \
		lambda channel, connection_status, disconnect_reason: \
			logger.info(channel.bd_addr + " " + str(connection_status) + (" " + str(disconnect_reason) if connection_status == fliclib.ConnectionStatus.Disconnected else ""))
	client.add_connection_channel(cc)

def got_info(items):
	logger.debug(items)
	for bd_addr in items["bd_addr_of_verified_buttons"]:
		got_button(bd_addr)




debug_devices = ligths_lan.get_lights()
labels = []
for device in debug_devices:
	logger.debug(device)


client.get_info(got_info)

client.on_new_verified_button = got_button

client.handle_events()
