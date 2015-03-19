__author__ = 'yleonychev'

from settings import PORT, CAPTCHA_HOST, CAPTCHA_PORT, CAPTCHA_PROBABILITY, REDIS_QUEUE, REDIS_PREFIX, METHODS
import tornado.ioloop
import tornado.web
import random
import uuid
from captchaqueue import cq
from learningqueue import lq


class Feature(object):

    def __init__(self, l):
        self.l = l

    def count_factor(self, request):
        return self.l(request)


def MethodFeature(request):
    return METHODS.index(request.method)


def UriLengthFeature(request):
    return len(request.uri)


def ParamCountFeature(request):
    return len(request.arguments)


def HeadersCount(request):
    return len(request.headers)


Features = [Feature(MethodFeature), Feature(UriLengthFeature), Feature(ParamCountFeature), Feature(HeadersCount)]
FeaturesCount = len(Features)

class MainHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = METHODS
    _learning = True

    def initialize(self):
        random.seed()

    def count_features(self):
        res = []
        for f in Features:
            res.append(f.count_factor(self.request))
        return res

    def is_learning(self):
        return self._learning

    def get_uuid(self):
        return str(uuid.uuid4())

    def redirect_to_captcha(self, uuid):
        self.set_status(302)
        self.set_header('Content-Type', 'text/html')
        self.set_header('Location', 'http://' + CAPTCHA_HOST + ':' + str(CAPTCHA_PORT) + '/?uuid=' + uuid)
        self.set_header('X-ForwardToUser-Y', '1')
        self.flush()

    def passthrough(self):
        self.set_status(200)
        self.set_header('Content-Type', 'text/html')
        self.flush()

    def get(self):
        self.parse_request()

    def post(self):
        self.parse_request()

    def put(self):
        self.parse_request()

    def delete(self):
        self.parse_request()

    def options(self):
        self.parse_request()

    def head(self):
        self.parse_request()

    def extract_factors(self):
        return []

    def save_factors(self, uuid, factors):
        return

    def parse_request(self):
        print(self.request)
        if (random.random() <= CAPTCHA_PROBABILITY) and self.is_learning:
            event_uuid = self.get_uuid()
            lq.save_features(event_uuid, self.count_features())
            print('Go to captcha with uuid=%s!' % event_uuid)
            self.save_factors(event_uuid, self.extract_factors())
            cq.check_event(event_uuid, "%s://%s%s" % (self.request.protocol, self.request.host, self.request.uri))
            self.redirect_to_captcha(event_uuid)
        else:
            print('Passthrough!')
            self.passthrough()



if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/.*", MainHandler),
    ])
    application.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()