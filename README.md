MY-SMART-HOME
=============

# Controlling LIFX with FLIC smart-buttons

[![demo](doc-lifx-flic-00.png)](https://youtube.com/shorts/Z6pzKkCa6y0?feature=share)

# Controlling TASMOTA on schedule

[![demo](doc-tasmota-schedule-00.png)](https://youtu.be/ER47l3pQupE?feature=share)


# DOCKER

On Raspberry PI 4 Model B

```
docker run -d --restart unless-stopped --network host --privileged -e ARCH=aarch64 -v [YOUR_FLICDB_PATH]:/config/flicd.db -v [YOUR_LOG_PATH]:/var/log/log.out totocastaldi/my-smart-home-flicd:raspberry4b
docker run -d --restart unless-stopped --network host -v [YOUR_LOG_PATH]:/var/log/log.out -v [YOUR_CONFIG]:/config/config.json totocastaldi/my-smart-home-server:raspberry4b
docker run -d --restart unless-stopped --network host -v [YOUR_LOG_PATH]:/var/log/log.out -v [YOUR_BATCH_LOGIC]:/app/batch.py totocastaldi/my-smart-home-batch:raspberry4b
```

batch.py example

```python
import schedule
import tasmota
import lifx

def all_off():
    tasmota.power_on("192.168.100.32", 2)
    lifx.all_off()

if __name__ == '__main__':        
    schedule.every().day.at("18:44").do(all_off)
    

    while True:
        schedule.run_pending()
        time.sleep(1)

```

config.json example

```json
{
	"buttons" : [
		{
			"bd_addr" : "80:e4:da:73:a7:cd",
			"name" : "dev",
			"actions" : [
				{
					"type" : "ClickType.ButtonHold",
					"action" : "all-off-lifx"
				},
				{
					"type" : "ClickType.ButtonHold",
					"action" : "off-lifx",
					"action_id" : "LIFX A19 1234,LIFX A19 456"
				},
				{
					"type" : "ClickType.ButtonDoubleClick",
					"action" : "up-lifx",
					"action_id" : "LIFX A19 123"
				}
			]
		}
	]
}

```

# DEV

With [Flic library](https://github.com/50ButtonsEach/fliclib-linux-hci)


With [Lifxlan](https://github.com/mclarkk/lifxlan)

Start it

```bash
[FLIC_LIB_PATH]/flicd -f [FLIC_DB_PATH]
```

## PYTHON

```bash
if [ ! -d ".venv" ]
then
    pyenv install 3.9.5
    pyenv local 3.9.5 
    pip install virtualenv
    virtualenv .venv
fi
```

## SCAN

```bash
. .venv/bin/activate
pip install -r requirements.txt
python scan_wizard.py
```

## EXECUTE

```bash
. .venv/bin/activate
pip install -r requirements.txt
LOG_LEVEL=DEBUG CONFIG=[YOUR_CONFIG_PATH] python smart_home.py
```
## BATCH

```bash
. .venv/bin/activate
pip install -r requirements.txt
LOG_LEVEL=DEBUG python batch.py
```