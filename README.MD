# GRTS

> Granular real-time sensor reader

## Getting started

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
pip install --editable . 
```

## Commands

### `sensors`

To get current sensor readings, use the sensor command:

```
$ sensors -s temp0
temp0: 21.812

$ sensors --list-all
temp0: 21.812
liquid0: 0.0

```

### `server`

To run the API server on port 5000 and start polling sensors:

```
server
```
