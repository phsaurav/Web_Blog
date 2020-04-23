import uuid

from src.common.database import Database
import datetime


class Post(object):
    def __init__(self, blog_id, title, content, author, created_date=datetime.datetime.utcnow(), _id=None):
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.author = author
        self.created_date = created_date
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mon(self):
        Database.insert(collection='posts', data=self.json())

    def json(self):
        return {
            'id': self._id,
            'blog_id': self.blog_id,
            'author': self.author,
            'title': self.title,
            'created_date': self.created_date,
            'content': self.content
        }

    @classmethod
    def from_mon(cls, _id):
        post_data = Database.find_one(collection='posts',
                                      query={'id': _id})

        return cls(**post_data)

    @staticmethod
    def fromBlog(_id):
        return [post for post in Database.find(collection="posts", query={'blog_id': _id})]
