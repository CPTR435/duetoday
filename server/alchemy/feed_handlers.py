import tornado.web
import logging
import requests
import json
import re
from alchemy.setup import *
from alchemy.base_handlers import BaseHandler

logger = logging.getLogger("pyserver")

class FeedHandler(BaseHandler):
    def get(self, id):
        feed = query_by_id(Feed, id)
        if not feed:
            return self.write({'error':'feed does not exist'})
        self.write({'feed':feed.to_json()})

    @tornado.web.authenticated
    def put(self):
        name = self.get_argument("name", None)
        user = self.current_user
        if not name:
            return self.write({'error':'you must give us a name'})
        administrators = self.get_argument("administrators", None)
        feed = Feed(name=name,owner=user.wwuid,administrators=administrators)
        feed = addOrUpdate(feed)
        self.write({'feed': feed.to_json()})

    @tornado.web.authenticated
    def post(self, id):
        name = self.get_argument("name", None)
        user = self.current_user
        if not name:
            return self.write({'error':'you must give us a name'})
        feed = query_by_id(Feed, id)
        if not feed:
            return self.write({'error':'feed does not exist'})
        if feed.owner != user.wwuid and user.wwuid not in feed.administrators.split(","):
            return self.write({'error':'insufficient permissions'})
        administrators = self.get_argument("administrators", None)
        feed.name = name
        feed.administrators = administrators
        feed = addOrUpdate(feed)
        self.write({'feed': feed.to_json()})

    @tornado.web.authenticated
    def delete(self, id):
        user = self.current_user
        feed = query_by_id(Feed, id)
        if not feed:
            return self.write({'error':'feed does not exist'})
        if feed.owner != user.wwuid:
            return self.write({'error':'insufficient permissions'})
        for item in query_by_field(Item, "feed_id", id):
            delete_thing(item)
        delete_thing(feed)
        self.write(json.dumps("success"))


class ItemHandler(BaseHandler):
    def get(self, id):
        item = query_by_id(Item, id)
        if not item:
            return self.write({'error':'item does not exist'})
        self.write({'item':item.to_json()})

    @tornado.web.authenticated
    def put(self):
        user = self.current_user
        feed_id = self.get_argument("feed_id", None)
        feed = query_by_id(Feed, feed_id)
        if not feed:
            return self.write({'error':'feed does not exist'})
        if feed.owner != user.wwuid and user.wwuid not in feed.administrators.split(","):
            return self.write({'error':'insufficient permissions'})
        name = self.get_argument("name", None)
        start_time = self.get_argument("start_time", None)
        end_time = self.get_argument("end_time", None)
        user = self.current_user
        if not name or not start_time or not end_time:
            return self.write({'error':'you must give us a name and a start_time and an end_time'})
        description = self.get_argument("description", None)
        item = Item(feed_id=feed_id,name=name,creator=user.wwuid,description=description,start_time=start_time,end_time=end_time)
        item = addOrUpdate(item)
        self.write({'item': item.to_json()})

    @tornado.web.authenticated
    def post(self, id):
        user = self.current_user
        item = query_by_id(Item, id)
        if not item:
            return self.write({'error':'item does not exist'})
        feed_id = self.get_argument("feed_id", None)
        feed = query_by_id(Feed, feed_id)
        if not feed:
            return self.write({'error':'feed does not exist'})
        if feed.owner != user.wwuid and user.wwuid not in feed.administrators.split(","):
            return self.write({'error':'insufficient permissions'})
        name = self.get_argument("name", None)
        start_time = self.get_argument("start_time", None)
        end_time = self.get_argument("end_time", None)
        user = self.current_user
        if not name or not start_time or not end_time:
            return self.write({'error':'you must give us a name and a start_time and an end_time'})
        description = self.get_argument("description", None)

        item.feed_id = feed_id
        item.name = name
        item.description = description
        item.start_time = start_time
        item.end_time = end_time
        item = addOrUpdate(item)
        self.write({'item': item.to_json()})

    @tornado.web.authenticated
    def delete(self, id):
        user = self.current_user
        item = query_by_id(Item, id)
        if not item:
            return self.write({'error':'item does not exist'})
        feed = query_by_id(Feed, item.feed_id)
        if not feed:
            return self.write({'error':'feed does not exist'})
        if feed.owner != user.wwuid and user.wwuid not in feed.administrators.split(","):
            return self.write({'error':'insufficient permissions'})
        delete_thing(item)
        self.write(json.dumps("success"))
