import random
import uuid
from .base import StoryMixin

vowels = ("a", "e", "i", "o", "u")

auxiliaries = {
    "past": ["has been", "did", "had"],
    "present": ["be", "being", "can", "do", "may", "must", "should", "ought", "shall", "would", "has"],
    "future": ["will", "may", "shall", "would", "will", "could"]
}


class Verb(StoryMixin):
    
    def __init__(self, word):
        super().__init__()
        self.id = str(uuid.uuid4())
        self.word = word
        
    def simple_past(self):
        return self.word + "ed" # this is NOT going to work for long.. I think I need a text indexing system

    def simple_present(self):
        return self.word

    def simple_future(self):
        return random.choice(auxiliaries["future"]) + " " + self.word # this is sketchy

