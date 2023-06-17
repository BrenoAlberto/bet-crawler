BOT_NAME = "estrelabet"

SPIDER_MODULES = ["estrelabet.spiders"]
NEWSPIDER_MODULE = "estrelabet.spiders"

# LOG_LEVEL = 'CRITICAL'

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

ROBOTSTXT_OBEY = False

SPLASH_URL = 'http://localhost:8050'
# CRAWLERA_ENABLED= False
# DOWNLOADER_MIDDLEWARES = {
#     'scrapy_splash.SplashCookiesMiddleware': 723,
#     'scrapy_splash.SplashMiddleware': 725,
#     'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
# }
COOKIES_ENABLED = True
COOKIES_DEBUG = True
SPLASH_COOKIES_DEBUG = True

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
