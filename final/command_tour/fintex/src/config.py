import json

# key format a.b.c => ./a.json -> "b" -> "c"
import os


def get(key):
    try:
        keys = key.split('.')
        config = json.load(open('./%s.json' % keys[0]))
        cur = config
        for k in keys[1:]:
            cur = cur[k]

        return cur
    except (IOError, json.JSONDecodeError, KeyError):
        return None


def set(key, value):
    keys = key.split('.')
    try:
        config = json.load(open('./%s.json' % keys[0]))
    except (IOError, json.JSONDecodeError, KeyError):
        config = dict()

    cur = config
    for k in keys[1:-1]:
        cur = cur[k]
    cur[keys[-1]] = value
    open('./%s.json' % keys[0], 'w+').write(json.dumps(config))


def clear(key):
    try:
        os.remove('./%s.json' % key)
    except OSError:
        pass
