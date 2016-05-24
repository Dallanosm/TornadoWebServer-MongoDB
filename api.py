from pymongo import MongoClient

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
import ast

from tornado.options import define, options

define("port", default=XXXXX, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/json", UploadJSONHandler),
	    (r"/photo", UploadPhotoHandler)
        ]

        settings = dict(
            autoescape=None,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        self.con = MongoClient()
        self.database = self.con["NAME"]


class UploadJSONHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello from uploadJson")
    def post(self):
        db = self.application.database
        data = json.loads(self.request.body.decode('utf-8'))
	d = ast.literal_eval(str(data))
        db.COLLECTION.insert(d)
	print type(d)
        print('JSON data:', d)
        self.write("200")

class UploadPhotoHandler(tornado.web.RequestHandler):
    def get(self):
	self.write("Hello from uploadPhoto")
    def post(self):
	picture_file = self.request.files['picture'][0]
	fname = picture_file['filename']
        output_file = open( fname, 'w')
        output_file.write(picture_file['body'])

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
