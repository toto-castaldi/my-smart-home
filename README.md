MY-SMART-HOME
=============

# Controlling LIFX with FLIC smart-buttons

[![demo](lifx-flic.png)](https://youtube.com/shorts/Z6pzKkCa6y0?feature=share)


# DOCKER

## FLICD

```
docker build . -f ./Dockerfile-flicd -t flicd
docker run -d --restart unless-stopped --network host --privileged -v [YOUR_FLICDB_PATH]:/config/flicd.db -v [YOUR_LOG_PATH]:/var/log/flicd.out flicd
```

## SMART_HOME

```
docker build . -f ./Dockerfile-smart_home -t smart_home
docker run -d --restart unless-stopped --network host -v [YOUR_LOG_PATH]:/var/log/smart_home.out -v [YOUR_CONFIG]:/config/config.json smart_home
```

# DEV

With [Flic library](https://github.com/50ButtonsEach/fliclib-linux-hci)

Start it

```bash
nohup ./flicd-deamon.sh [FLIC_LIB_PATH]/flicd [FLIC_DB_PATH] &
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
python scan_wizard.py
```

## EXECUTE

```bash
. .venv/bin/activate
pip install -r requirements.txt
LOG_LEVEL=DEBUG CONFIG=[YOUR_CONFIG_PATH] python smart_home.py
```

# RASPBERRY

Tested on a Raspberry PI 4 Model B

restarting deamons
```bash
kill -9 `ps -ef | grep -P "python smart_home.py" | head -n 1 | awk '{print $2}'`
kill -9 `ps -ef | grep -P "flicd -f" | head -n 1 | awk '{print $2}'`
```

At 02:00.

0 2 * * * kill -9 `ps -ef | grep -P "python smart_home.py" | head -n 1 | awk '{print $2}'`

