__author__ = 'yleonychev'

PORT = 8080
CAPTCHA_HOST = '127.0.0.1'
CAPTCHA_PORT = PORT + 1
CAPTCHA_PROBABILITY = 0.1
CAPTCHA_PRIVKEY = '6LfKjQMTAAAAAMGW-qDb6_-eMAEe_0V6M433foOF'
CAPTCHA_PUBKEY = '6LfKjQMTAAAAACerh3MOKShs_t3qfrERlLVuifNh'
REDIS_QUEUE = {'host': '127.0.0.1', 'db': 4}
REDIS_PREFIX = 'pywaf'
METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEAD']