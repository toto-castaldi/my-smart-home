import fliclib
import lifx
import utils
import config
import lifxlan
import lifx
import traceback

logger = utils.init_log()
c = config.get_config()
ligths_lan = lifxlan.LifxLAN(None)
client = fliclib.FlicClient("localhost")
MAX_POWER = 65535
devices_cache = {

}

def toggle_lifx(device):
	current_power = device.get_power()
	device.set_power(0 if current_power == MAX_POWER else MAX_POWER, rapid=True)

def down_lifx(device):
	current_brightness = device.get_color()[2]
	device.set_brightness(current_brightness - 12000 if current_brightness >= 12000 else 0, rapid=True)

def up_lifx(device):
	current_brightness = device.get_color()[2]
	logger.debug(current_brightness)
	device.set_brightness(current_brightness + 12000 if current_brightness < (MAX_POWER - 12000) else MAX_POWER, rapid=True)

def off_lifx(device):
	device.set_power(0, rapid=True)

def wrap_lifx(callback, targets):
	try:
		for target in targets.split(","):
			device = None
			if target in devices_cache:
				device = devices_cache[target]
			else:
				logger.info(f"search for device {target}")
				device = ligths_lan.get_device_by_name(target)
				if device:
					devices_cache[target] = device

			if device:
				callback(device)
			else:
				logger.warning(f"unknow device by name {target}")
	except:
		traceback.print_exc()

wrapped_actions = {
	"toggle-lifx" : toggle_lifx,
	"down-lifx" : down_lifx,
	"up-lifx" : up_lifx,
	"off-lifx" : off_lifx
}

direct_actions = {
	"all-off-lifx" : lifx.all_off
}

def on_button_single_or_double_click_or_hold(channel, click_type, was_queued, time_diff):
	bd_addr = channel.bd_addr
	c_type = str(click_type)
	logger.debug(f"{bd_addr} -> {c_type}")
	button = config.search_button(bd_addr)
	if button is not None:
		configured_action = config.search_action(button, c_type)
		if configured_action is not None:
			logger.info(configured_action)
			c_a_action = configured_action["action"]
			if c_a_action in wrapped_actions:
				wrap_lifx(wrapped_actions[c_a_action], configured_action["action_id"])
			elif c_a_action in direct_actions:
				direct_actions[c_a_action]()
			else:
				logger.warning(f"can't find {c_a_action} handler")		
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
	devices_cache[device.get_label()] = device
	logger.debug(device)


client.get_info(got_info)

client.on_new_verified_button = got_button

client.handle_events()
