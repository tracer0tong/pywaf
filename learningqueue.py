__author__ = 'yleonychev'

from settings import REDIS_QUEUE, REDIS_PREFIX
import redis
import pickle


class LearningQueue(object):
    LearningQueuePrefix = 'lq'

    def __init__(self, host, db, prefix):
        self.host = host
        self.db = db
        self.prefix = prefix + self.LearningQueuePrefix
        self.redis = redis.StrictRedis(self.host, db=self.db)

    def save_features(self, uuid, features):
        print("Save features %s for %s" % (uuid, pickle.dumps(features)))

    def load_features(self, uuid):
        return []


lq = LearningQueue(REDIS_QUEUE['host'], REDIS_QUEUE['db'], REDIS_PREFIX)