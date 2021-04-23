import json


def update_redis(redis, state):
    for key, value in state.items():
        # print(key, value, redis.get(key))
        redis.set(key, json.dumps(value))


def get_state_data(redis, state_keys):
    r = {}
    for key in state_keys:
        val = redis.get(key)
        try:
            val = json.loads(val)
        except ValueError:
            pass
        r[key] = val
    return r
