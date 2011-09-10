from google.appengine.ext import db
from pili.db import Model2
import time,datetime,re

from pili import lite
lite.init(globals())

"""
This file describe 
"""

class BloggerApi(object):
    list_item_num = 20

    def __init__(self):
        pass

    def createBlog(self, blog_id, owner, blog_name, **kwds):
        if not re.match(r"^[a-z]\w+$", blog_id):
            return False
        if BlogMeta.get_by_key_name(blog_id) is not None:
            return False
        blog = BlogMeta(key_name=blog_id, blog_id=blog_id, owner=owner, blog_name=blog_name)
        blog.put()
        return True

    def listBlogs(self, owner, page=1):
        return BlogMeta.all().filter('owner =',owner).fetch(
            self.list_item_num, (page-1)*self.list_item_num)

# model

class BlogMeta(db.Model):
    blog_id = db.StringProperty(required=True, indexed=False)
    owner = db.UserProperty(required=True)
    blog_name = db.StringProperty(required=True, indexed=False)

class BlogPost(db.Model):
    auto_key_name = lambda: ":".join([self.post_no])
    post_no = db.IntegerProperty(indexed=False, required=True, default=0)
    slug = db.StringProperty()
    labels = db.StringListProperty()
    cdatetime=db.DateTimeProperty(auto_now=True)
    status = db.IntegerProperty(required=True)
    udatetime=db.DateTimeProperty(default=datetime.datetime.fromtimestamp(time.time()))
    # indexed: blog_no, status, udatetime

class BlogPostLebel(db.Model):
    auto_key_name = lambda: ":".join([self.blog_no, self.label_name])
    post_id = db.StringProperty(required=True)
    blog_no = db.IntegerProperty(required=True)
    udatetime = db.DateTimeProperty(indexed=False)
    # indexed: blog_no, label_no, udatetime

class BlogLabel(db.Model):
    auto_key_name = lambda: ":".join([self.blog_id, self.label_name])
    label_no = db.IntegerProperty(required=True)
    label_name = db.StringProperty(required=True)

