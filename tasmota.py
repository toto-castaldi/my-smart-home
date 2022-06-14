import utils
import requests

logger = utils.init_log()

def power_on(ip:str, output_number:int):
    url = f"http://{ip}/cm?cmnd=Power{output_number}%20On"
    logger.debug(url)
    r = requests.get(url)
    text_response = r.content.decode('UTF-8')
    logger.debug(text_response)
    if r.status_code == 200:
        logger.debug("OK")
        return True
    else:
        logger.debug("KO")
        return None


