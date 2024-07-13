import uuid
from .base import StoryMixin

class Adjective(StoryMixin):

    def __str__(self):
        self.id = str(uuid.uuid4())
        return self.word


    def __init__(self, word):
        super().__init__()
        self.word = word

