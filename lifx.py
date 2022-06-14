import string
import requests
import utils
import lifxlan

logger = utils.init_log()
ligths_lan = lifxlan.LifxLAN(None)
MAX_POWER = 65535
devices_cache = {

}

debug_devices = ligths_lan.get_lights()
for device in debug_devices:
	devices_cache[device.get_label()] = device
	logger.debug(device)


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

def all_off():
    ligths_lan.set_power_all_lights("off", rapid=True)

def toggle(device_id:string):
    def c(device):
        current_power = device.get_power()
        device.set_power(0 if current_power == MAX_POWER else MAX_POWER, rapid=True)

    wrap_lifx(c, device_id)

def down(device_id):
    def c(device):
        current_brightness = device.get_color()[2]
        device.set_brightness(current_brightness - 12000 if current_brightness >= 12000 else 0, rapid=True)

    wrap_lifx(c, device_id)

def up(device_id):
    def c(device):
        current_brightness = device.get_color()[2]
        logger.debug(current_brightness)
        device.set_brightness(current_brightness + 12000 if current_brightness < (MAX_POWER - 12000) else MAX_POWER, rapid=True)
    
    wrap_lifx(c, device_id)
	
def off(device_id):
    def c(device):
        device.set_power(0, rapid=True)

    wrap_lifx(c, device_id)

def api_list_lights(api_token:string):
    headers = {
        "Authorization": "Bearer %s" % api_token,
    }
    logger.debug(api_token)
    response = requests.get("https://api.lifx.com/v1/lights/all", headers=headers)
    logger.debug(response.json())

def api_toggle(device_id:string, api_token:string):
    headers = {
        "Authorization": "Bearer %s" % api_token,
    }
    logger.debug(api_token)
    response = requests.post(f"https://api.lifx.com/v1/lights/{device_id}/toggle", headers=headers)
    logger.debug(response.json())

def api_state_delta(device_id:string, api_token:string, brightness = None):
    headers = {
        "Authorization": "Bearer %s" % api_token,
    }
    payload = {

    }
    if brightness is not None:
        payload["brightness"] = brightness
    response = requests.post(f"https://api.lifx.com/v1/lights/{device_id}/state/delta", data=payload, headers=headers)
    logger.debug(response.json())