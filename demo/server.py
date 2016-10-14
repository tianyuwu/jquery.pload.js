#!/usr/bin/env python
# coding=utf8

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        p = self.get_argument('p',1)
        self.render("index.html", p=int(p))


def main():
    tornado.options.parse_command_line()
    settings = dict(debug=True,static_path=os.path.join(os.path.dirname(__file__), "js"),)
    application = tornado.web.Application(
        [
            (r"/", MainHandler),
        ],**settings
    )
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
