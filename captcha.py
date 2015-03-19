__author__ = 'yleonychev'

from settings import CAPTCHA_HOST, CAPTCHA_PORT, CAPTCHA_PRIVKEY, CAPTCHA_PUBKEY
import tornado.ioloop
import tornado.web
import tornado.template
from recaptcha.client import captcha
from captchaqueue import cq


class Captcha(object):

    def __init__(self, public_key, server_key):
        self.public_key = public_key
        self.server_key = server_key

    def check(self, challenge, response, ip):
        res = captcha.submit(
            challenge,
            response,
            self.server_key,
            ip,
        )
        return res.is_valid

    def generate(self):
        return captcha.displayhtml(self.public_key)


class MainHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ['GET', 'POST']

    def initialize(self):
        self.captcha = Captcha(CAPTCHA_PUBKEY, CAPTCHA_PRIVKEY)

    def get(self):
        uuid = self.get_argument('uuid', '')
        if cq.exists(uuid):
            if cq.get_result(uuid)[0]:
                redir = cq.get_redirect(uuid)
                print('Done already for %s' % uuid)
                self.redirect(redir)
            else:
                self.render('./templates/captcha.html', captcha=self.captcha.generate(), uuid=uuid)
        else:
            print('Unexistant uuid=%s' % uuid)
            self.render('./templates/captcha.html', captcha=self.captcha.generate(), uuid=uuid)

    def post(self):
        uuid = self.get_argument('uuid', '')
        challenge = self.get_argument('recaptcha_challenge_field')
        response = self.get_argument('recaptcha_response_field')
        x_real_ip = self.request.headers.get("X-Real-IP")
        remote_ip = self.request.remote_ip if not x_real_ip else x_real_ip
        print(uuid)
        if cq.exists(uuid):
            if (self.captcha.check(challenge, response, remote_ip)):
                cq.prove_event(uuid)
                redir = cq.get_redirect(uuid)
                self.redirect(redir)
            else:
                cq.failed_event(uuid)
                self.render('./templates/captcha.html', captcha=self.captcha.generate(), uuid=uuid)
        else:
            print('Unexistant uuid=%s' % uuid)
            self.render('./templates/captcha.html', captcha=self.captcha.generate(), uuid=uuid)



if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/.*", MainHandler),
    ])
    application.listen(CAPTCHA_PORT, CAPTCHA_HOST)
    tornado.ioloop.IOLoop.instance().start()