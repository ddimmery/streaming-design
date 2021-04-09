import json


def update_redis(redis, state):
    for key, value in state.items():
        print(key, value, redis.get(key))
        redis.set(key, json.dumps(value))


def get_state_data(redis, state_keys):
    r = {}
    for key in state_keys:
        val = redis.get(key)
        if isinstance(val, str):
            val = json.loads(val)
        r[key] = val
    return r
