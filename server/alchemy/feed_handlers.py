import tornado.web
import logging
import requests
import json
import re
from dateutil.relativedelta import relativedelta
from alchemy.setup import *
from alchemy.base_handlers import BaseHandler

logger = logging.getLogger("pyserver")

def CreateRepeatingItems(item, repeat):
    endoftime = dTime("2017-02-01") # CHANGE THIS DATE TO SOMETIME, FAR IN THE FUTURE
    def newItem(t):
        i = Item(feed_id=item.feed_id, title=item.title, creator=item.creator, description=item.description, location=item.location, repeat=item.repeat, start=(item.start+t), end=(item.end+t))
        i = addOrUpdate(i)

    if repeat == "Yearly": # every year on the same date
        p = 1
        t = relativedelta(years=p)
        while item.start + t <= endoftime:
            newItem(t)
            p = p+1
            t = relativedelta(years=p)
        return

    for d in range(1, (endoftime - item.start).days+1):
        t = datetime.timedelta(days=d)
        if repeat == "Daily": # every day
            newItem(t)
        elif repeat == "Weekday": # every weekday
            weekday = (item.start+t).weekday()
            if weekday >= 0 and weekday <= 4:
                newItem(t)
        elif repeat == "Weekly": # every week
            if t.days%7 == 0:
                newItem(t)
        elif repeat == "Alternateweekly": # every other week
            if t.days%14 == 0:
                newItem(t)
        elif repeat == "Monthly": # first same day of the week every month
            weekday = (item.start+t).weekday()
            day = (item.start + t).day
            if weekday == item.start.weekday() and day > item.start.day-7 and day < item.start.day+7:
                newItem(t)
        elif repeat == "Daymonthly": # same date of every month
            day = (item.start + t).day
            if day == item.start.day:
                newItem(t)

def DeleteRepeatingItems(item):
    for i in query_by_field(Item, "feed_id", item.feed_id):
        if i.title == item.title and i.description == item.description and i.location == item.location and i.repeat == item.repeat and i.creator == item.creator and (i.updated_at - item.updated_at).seconds < 5:
            if i != item:
                logger.debug(i.to_json())
                delete_thing(i)

class ListUserFeedsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = self.current_user
        feeds = query_by_field(Feed, "owner", user.wwuid)
        self.write(json.dumps([f.to_json() for f in feeds]))

class FeedHandler(BaseHandler):
    def get(self, id):
        feed = query_by_id(Feed, id)
        if not feed:
            return self.write({'error':'feed does not exist'})
        self.write({'feed':feed.to_json()})

    @tornado.web.authenticated
    def put(self):
        title = self.get_argument("title", None)
        description = self.get_argument("description", None)
        private = self.get_argument("private", True)
        user = self.current_user
        if not title:
            return self.write({'error':'you must give us a title'})
        administrators = self.get_argument("administrators", None)
        feed = Feed(title=title,owner=user.wwuid,administrators=administrators,description=description,private=private)
        feed = addOrUpdate(feed)
        self.write({'feed': feed.to_json()})

    @tornado.web.authenticated
    def post(self, id):
        title = self.get_argument("title", None)
        description = self.get_argument("description", None)
        private = self.get_argument("private", True)
        user = self.current_user
        if not title:
            return self.write({'error':'you must give us a title'})
        feed = query_by_id(Feed, id)
        if not feed:
            return self.write({'error':'feed does not exist'})
        if feed.owner != user.wwuid and user.wwuid not in feed.administrators.split(","):
            return self.write({'error':'insufficient permissions'})
        administrators = self.get_argument("administrators", None)
        feed.title = title
        feed.description = description
        feed.private = private
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
        title = self.get_argument("title", None)
        start = dTime(self.get_argument("start", None))
        end = dTime(self.get_argument("end", None))
        user = self.current_user
        if not title or not start or not end:
            return self.write({'error':'you must give us a title and a start and an end'})
        description = self.get_argument("description", None)
        location = self.get_argument("location", None)
        repeat = self.get_argument("repeat", None)
        item = Item(feed_id=feed_id,title=title,creator=user.wwuid,description=description,location=location,repeat=repeat,start=start,end=end)
        item = addOrUpdate(item)

        repeat = self.get_argument("repeat", None)
        if repeat and repeat != "Once":
            CreateRepeatingItems(item, repeat)

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
        title = self.get_argument("title", None)
        start = dTime(self.get_argument("start", None))
        end = dTime(self.get_argument("end", None))
        user = self.current_user
        if not title or not start or not end:
            return self.write({'error':'you must give us a title and a start and an end'})
        description = self.get_argument("description", None)
        location = self.get_argument("location", None)
        repeat = self.get_argument("repeat", None)

        DeleteRepeatingItems(item)

        item.feed_id = feed_id
        item.title = title
        item.description = description
        item.location = location
        item.repeat = repeat
        item.start = start
        item.end = end
        item = addOrUpdate(item)

        repeat = self.get_argument("repeat", None)
        if repeat and repeat != "Once":
            CreateRepeatingItems(item, repeat)

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
        DeleteRepeatingItems(item)
        delete_thing(item)
        self.write(json.dumps("success"))

class ListFeedItemsHandler(BaseHandler):
    def get(self, id):
        feed = query_by_id(Feed, id)
        if not feed:
            return self.write({'error':'feed does not exist'})
        items = query_by_field(Item, "feed_id", id)
        self.write(json.dumps([i.to_json() for i in items]))

class ListFeedItemsByDateTimeHandler(BaseHandler):
    def get(self, id, start, end):
        start = dTime(start)
        end = dTime(end)
        feed = query_by_id(Feed, id)
        if not feed:
            return self.write({'error':'feed does not exist'})
        self.write(json.dumps([i.to_json() for i in query_items_by_datetime(id,start,end)]))

class ListUserItemsByDateTimeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, start, end):
        user = self.current_user
        start = dTime(start)
        end = dTime(end)
        self.write(json.dumps([i.to_json() for i in query_user_items_by_datetime(user.wwuid,start,end)]))
