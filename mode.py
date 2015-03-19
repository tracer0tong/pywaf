__author__ = 'yleonychev'

from settings import REDIS_QUEUE, REDIS_PREFIX
import redis

MODE_LEARN = 0 #  Collect events
MODE_MEASURE = 1 #  Measure of classifier mistakes
MODE_CHECK = 2 # Production


class Mode(object):
    ModePrefix = 'mode'

    def __init__(self, host, db, prefix, mode=MODE_LEARN):
        self.host = host
        self.db = db
        self.prefix = prefix + self.ModePrefix
        self.redis = redis.StrictRedis(self.host, db=self.db)
        self.set_mode(mode)

    def get_mode(self):
        mode = self.redis.get(self.prefix)
        if mode:
            return int(mode)
        else:
            self.set_mode(MODE_LEARN)
            return MODE_LEARN

    def set_mode(self, mode):
        if mode in [MODE_LEARN, MODE_CHECK, MODE_MEASURE]:
            self.redis.set(self.prefix, mode)


m = Mode(REDIS_QUEUE['host'], REDIS_QUEUE['db'], REDIS_PREFIX)