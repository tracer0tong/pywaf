__author__ = 'yleonychev'

from settings import REDIS_QUEUE, REDIS_PREFIX
import redis


class CaptchaQueue(object):
    CaptchaQueuePrefix = 'cq'
    RedirectsPrefix = 'r'
    ProvesPrefix = 'p'
    AttemptsRefix = 'a'

    def __init__(self, host, db, prefix):
        self.host = host
        self.db = db
        self.prefix = prefix + self.CaptchaQueuePrefix
        self.redis = redis.StrictRedis(self.host, db=self.db)

    def check_event(self, uuid, redirect_to):
        pipe = self.redis.pipeline()
        pipe.set(self.prefix + self.RedirectsPrefix + uuid, redirect_to)
        pipe.set(self.prefix + self.AttemptsRefix + uuid, 0)
        pipe.set(self.prefix + self.ProvesPrefix + uuid, 0)
        pipe.execute()

    def prove_event(self, uuid):
        pipe = self.redis.pipeline()
        pipe.incr(self.prefix + self.AttemptsRefix + uuid)
        pipe.set(self.prefix + self.ProvesPrefix + uuid, 1)
        pipe.execute()

    def failed_event(self, uuid):
        pipe = self.redis.pipeline()
        pipe.incr(self.prefix + self.AttemptsRefix + uuid)
        pipe.set(self.prefix + self.ProvesPrefix + uuid, 0)
        pipe.execute()

    def delete_check(self, uuid):
        pipe = self.redis.pipeline()
        pipe.delete(self.prefix + self.RedirectsPrefix + uuid)
        pipe.delete(self.prefix + self.AttemptsRefix + uuid)
        pipe.delete(self.prefix + self.ProvesPrefix + uuid)
        pipe.execute()

    def get_redirect(self, uuid):
        return self.redis.get(self.prefix + self.RedirectsPrefix + uuid)

    def get_result(self, uuid):
        if int(self.redis.get(self.prefix + self.ProvesPrefix + uuid)) == 0:
            res = False
        else:
            res = True
        return res, int(self.redis.get(self.prefix + self.AttemptsRefix + uuid))

    def exists(self, uuid):
        return self.redis.exists(self.prefix + self.ProvesPrefix + uuid)


cq = CaptchaQueue(REDIS_QUEUE['host'], REDIS_QUEUE['db'], REDIS_PREFIX)