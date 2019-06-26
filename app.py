# coding:utf-8

"""
Main tornado application.
API that handles all training, testing and predicting routes.
"""

import configparser
import os

import motor.motor_tornado
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from controllers.auth_controller import AuthController
from controllers.user_controller import UserController
from core.local_configmanager import ConfigManager

CONFIG = ConfigManager('config.ini')

tornado.options.define(
    "port", default=CONFIG.api['port'], help=None, type=int
)


class Application(tornado.web.Application):
    def __init__(self):

        args = dict(
            config=CONFIG,
            db=db
        )

        handlers = [
            # Auth
            (r"/api/v1/auth/?(?P<method>[^\/]+)?",
                AuthController, args),
            (r"/api/v1/users/?(?P<model_id>[^\/]+)?",
                UserController, args)
        ]

        settings = {
            "debug": True,
            "autoreload": True,
            "static_path": os.path.abspath("static")
        }
        
        tornado.web.Application.__init__(
            self, handlers, **settings
        )


if __name__ == "__main__":
    try:
        tornado.options.parse_command_line()

        # Mongo DB
        database_string = CONFIG.mongo['connection_string']
        client = motor.motor_tornado.MotorClient(database_string)
        db = client[CONFIG.mongo['database']]

        app = tornado.httpserver.HTTPServer(Application())
        app.listen(tornado.options.options.port)

        print("Tornado Seed executando na porta {}".format(
            tornado.options.options.port))

        io_loop = tornado.ioloop.IOLoop.instance()
        io_loop.start()

    except KeyboardInterrupt:
        exit()
