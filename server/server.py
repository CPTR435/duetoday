
import os
import logging
import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.autoreload
from tornado.options import define, options

from alchemy.base_handlers import *
from alchemy.feed_handlers import *

define("port", default=8888, help="run on the given port", type=int)
define("log_name", default="pyserver", help="name of the logfile")
define("auth_url", default="/auth")

class Application(tornado.web.Application):
    def __init__(self):
        settings = {
            "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            "login_url": "/",
        }

        handlers = [
            (r"/item", ItemHandler),
            (r"/item/(.*)", ItemHandler),
            (r"/feed", FeedHandler),
            (r"/feed/(.*)", FeedHandler),
            (r"/feed_items/(.*)", ListFeedItemsHandler),
            (r"/user_feeds", ListUserFeedsHandler),
            (r"/items_by_datetime/(.*)/(.*)/(.*)", ListFeedItemsByDateTimeHandler),
            (r"/user_items_by_datetime/(.*)/(.*)", ListUserItemsByDateTimeHandler),
            (r"/login", LoginHandler),
            (r"/", IndexHandler),
            (r"/(.*)", tornado.web.StaticFileHandler, {'path': '../'}),
        ]

        self.options = options
        logger = logging.getLogger("pyserver")
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler("etc/logs/"+options.log_name+".log")
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter("{'timestamp': %(asctime)s, 'loglevel' : %(levelname)s %(message)s }")
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        tornado.web.Application.__init__(self, handlers, **settings)
        logger.info("Application started on port " + str(options.port))


if __name__ == "__main__":
    config = tornado.options.parse_command_line()
    if len(config) == 0:
        conf_name = "default"
    else:
        conf_name = config[0]
    io_loop = tornado.ioloop.IOLoop.instance()
    tornado.options.parse_config_file("etc/conf/"+conf_name+".conf")
    application = Application()
    application.listen(options.port)
    tornado.autoreload.start()
    io_loop.start()
