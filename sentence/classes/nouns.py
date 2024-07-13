import uuid
from typing import Literal, Any
from .base import StoryMixin

class Noun(StoryMixin):

    def __str__(self):
        #TODO: this needs to consider story/sentence context and narrator
        return self.with_possession()


    # TODO: maybe replace article_type with common vs proper
    def __init__(self, word: str, is_subject: bool, article_type: Literal["general", "specific", "none"], possessed_by: Any, gender: Literal["male", "female", "none"]):
        self.id = str(uuid.uuid4())
        super().__init__()
        self.word = word
        self.is_subject = is_subject
        self.article_type = article_type or "none"
        self.possessed_by = possessed_by or None
        self.gender = gender or "none"

    def with_article(self):
        story = super(Noun, self).get_story()
        article = "the"
        if self.article_type == "none":
            return "I" if story.narrator == self else self.word
        if self.article_type == "general":
            article = "a" if self.word.startswith(vowels) else "an"
        return f"{article} {self.word}"

    def with_possession_article(self):
        story = super(Noun, self).get_story()
        if story.narrator.id == self.possessed_by.id:
            return "my " + self.word
        if self.possessed_by in story.local_context:
            article = "his" if self.possessed_by.gender == "male" else "her"
            return f"{article} {self.word}"
        return self.possessed_by.word + "'s " + self.word 
    
    def with_possession(self):
        if not self.possessed_by or self.possessed_by.gender == "none":
            return self.with_article()
        return self.with_possession_article()

