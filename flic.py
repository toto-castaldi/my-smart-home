import fliclib
import utils

logger = utils.init_log()
client = fliclib.FlicClient("localhost")
the_callback = None

def got_button(bd_addr):
	def on_button_single_or_double_click_or_hold(channel, click_type, was_queued, time_diff):
		bd_addr = channel.bd_addr
		c_type = str(click_type)
		the_callback(bd_addr, c_type)

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

def listen(button_callback):
    global the_callback
    client.get_info(got_info)
    the_callback = button_callback
    client.on_new_verified_button = got_button
    client.handle_events()