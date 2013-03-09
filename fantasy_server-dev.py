#-*- coding: utf-8 -*-
import os.path
import tornado.auth
import tornado.escape
import tornado.gen
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import motor
import json
import codecs

from bson import SON
from bson import json_util
from motor import MotorClient
from md5 import md5
from tornado.options import define, options
define("port", default=8080, help="run on the given port", type=int)
define("api_key", default="1000000a1", help="insert api_key")

#DocumntRoot_v1 = options.api_key + "/v1/"
#DocumntRoot_v2 = options.api_key + "/v2/"

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/", MainHandler),
            (r"/game/start",Start_GameHandler),
            (r"/store/list",MainHandler),
            (r"/store/buy",MainHandler),
            (r"/user/item/list",MainHandler),
            (r"/user/friend/list",MainHandler)
        ]
        settings = {
            'template_path': os.path.join(os.path.dirname(__file__), "templates"),
            'static_path': os.path.join(os.path.dirname(__file__), "static"),
            'debug': True,
            'autoescape': None,
            'db_conn': MotorClient('127.0.0.1',27017).open_sync()
        }
        tornado.web.Application.__init__(self, handlers, **settings)
        
        
class BaseHandler(tornado.web.RequestHandler):
     def get(self):
         return


class MainHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        self.render("index.html",data="none")

class Start_GameHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        username = self.get_argument("username","")
        
        find_str = {}
        find_str["user.account"] = username
                
        db = self.settings['db_conn'].userdb
        
        cursor = db.user.find(find_str)
        query = yield motor.Op(cursor.to_list)        
        data = json.dumps(query,default=json_util.default)
        
        self.render("user_info.html",data=data)        
        

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
    
