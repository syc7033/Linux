
from web.session import Store
import json

class RedisStore(Store):
    def __init__(self, grds, timeout):
        self.redis = grds
        self.timeout = timeout
        
    def encode(self, session_dict):
        return json.dumps(session_dict)
    
    def decode(self, session_data):
        return json.loads(session_data)
    
    def __contains__(self, key):
        return self.redis.exists(key)
    
    def __getitem__(self, key):
        value = self.redis.get(key)
        if value:
            self.redis.expire(key, self.timeout)
            return self.decode(value)
        else:
            raise KeyError(key)
    
    def __setitem__(self, key, value):
        self.redis.setex(key, self.timeout, self.encode(value))

    def __delitem__(self, key):
        self.redis.delete(key)

    def cleanup(self, key):
        pass
