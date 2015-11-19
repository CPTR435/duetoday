import tornado.web
import logging
import requests
import json
import re
from alchemy.setup import *

logger = logging.getLogger("pyserver")


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    def get_current_user(self):
        wwuid = self.get_secure_cookie("wwuid")
        user = query_user(str(wwuid))
        return user


class VerifyHandler(BaseHandler):
    def get(self):
        user = self.current_user
        if user:
            self.write(str(user.wwuid))
        else:
            self.write("Not logged in")

class IndexHandler(BaseHandler):
    def get(self):
        self.render("../../index.html")

class LoginHandler(BaseHandler):
    def get(self):
        self.write({'error': 'You must login to access that content'})

    def post(self):
        logger.debug("'class':'LoginHandler','method':'post', 'message': 'invoked'")
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)

        if username and password:
            try:
                r = requests.post(self.application.options.auth_url, data = {'username': username, 'password': password}, verify=False)
                o = json.loads(r.text)
                if 'user' in o:
                    o = o['user']
                    logger.debug(o)
                    user = query_user(o["wwuid"])
                    if not user:
                        # Note to Brock: o["photo"] gives a "LoginHandler exception: photo"
                        user = User(wwuid=o["wwuid"], name=o["full_name"], mask_photo="") #o["photo"])
                        user = addOrUpdate(user)
                    self.set_secure_cookie("wwuid", str(o['wwuid']), expires_days=30)
                    logger.info("LoginHandler: success")
                    self.write(user.to_json())
                else:
                    logger.info("LoginHandler: error")
                    self.write({'error':'invalid login credentials'})
            except Exception as e:
                logger.debug("LoginHandler exception: "+ str(e.message)+ ", " + str(type(e)) )
                self.write({'error': str(e.message)})
        else:
            logger.error("LoginHandler: invalid post parameters")
            self.write({'error':'invalid post parameters'})
