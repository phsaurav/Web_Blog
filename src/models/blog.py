import uuid
import datetime
import logging

logging.basicConfig(level=logging.DEBUG)

from src.common.database import Database
from src.models.post import Post


class Blog(object):
    def __init__(self, author, title, description, author_id, _id=None):
        self.author = author
        self.title = title
        self.author_id = author_id
        self.description = description
        self._id = uuid.uuid4().hex if _id is None else _id

    def new_post(self, title, content, date=datetime.datetime.utcnow()):
        post = Post(blog_id=self._id,
                    title=title,
                    content=content,
                    author=self.author,
                    created_date=date)
        post.save_to_mon()

    def get_post(self):
        return Post.fromBlog(self._id)

    def save_to_mon(self):
        Database.insert(collection='blogs', data=self.json())

    def json(self):
        return {
            'author': self.author,
            'author_id': self.author_id,
            'title': self.title,
            'description': self.description,
            '_id': self._id
        }

    @staticmethod
    def get_from_mon(_id):
        blog_data = Database.find_one(collection='blogs',
                                      query={'_id': _id})

        return Blog(**blog_data)

    @classmethod
    def find_by_author_id(cls, author_id):
        print(author_id)
        blogs = Database.find(collection='blogs',
                              query={'author_id': author_id})
        print(blogs)
        return [cls(**blog) for blog in blogs]
