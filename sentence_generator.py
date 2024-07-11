import uuid
import random
from typing import Literal, Type, Any, List
from dataclasses import dataclass

vowels = ("a", "e", "i", "o", "u")
auxiliaries = ["be", "being", "been", "can", "do", "may", "must", "could", "should", "ought", "shall", "will", "would", "has", "have", "had"]

def capitalize(word_str: str):
    return word_str.capitalize()

class StoryMixin(object):

    def __init__(self):
        self.story = None

    def get_story(self):
        return self.story

    def backlink(self, story):
        # print("setting self.story to", story)
        self.story = story

class Adjective(StoryMixin):

    def __str__(self):
        self.id = str(uuid.uuid4())
        return self.word


    def __init__(self, word):
        super().__init__()
        self.word = word


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
        return random.choice(auxiliaries) + " " + self.word # this is sketchy


    
class Noun(StoryMixin):

    def __str__(self):
        #TODO: this needs to consider story/sentence context and narrator
        return self.with_possession()
    
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
        if self in story.local_context:
            article = "his" if self.possessed_by.gender == "male" else "her"
            return f"{article} {self.word}"
        return self.possessed_by.word + "'s " + self.word 
    
    def with_possession(self):
        if not self.possessed_by or self.possessed_by.gender == "none":
            return self.with_article()
        return self.with_possession_article()

class Story:
    #TODO: this will store story arc, noun ambitions, tenses, story context & sentence context and etc
    # ^ the story will basically be generating all these things
    def __init__(self, narrator: Type[Noun], nouns: List[Noun]):
        self.id = str(uuid.uuid4())
        self.perspective = "first"
        self.narrator = narrator
        self.global_context = []
        self.local_context = []
        self.nouns = nouns
        self.theme = None
        self.full_story = ""
        self.fullfill_backlinks()

    def show_story(self):
        return self.full_story
        
    def fullfill_backlinks(self):
        if self.narrator:
            super(Noun, self.narrator).backlink(self)
        for n in self.nouns:
            super(Noun, n).backlink(self)

    def story_update(self, used_nouns: List[Type[Noun]], sentence: str):
        "flush out nouns that were not used in the last sentence, save sentence to story"
        # TODO: later to control tone and adjectives and etc for coming sentence...
        self.local_context = used_nouns
        self.full_story += sentence
        
    def generate_indepentant_clause(self, subject: Type[Noun], verb: Type[Verb], tense: Literal["past", "present", "future"], optional_noun_adj=None):
        sentance_verb = verb.simple_present()
        if tense == "past":
            sentance_verb = verb.simple_past()
        if tense == "future":
            sentance_verb = verb.simple_future()
        sentence = f"{capitalize(subject.__str__())} {sentance_verb} {optional_noun_adj}. "
        self.story_update([subject], sentence)
        return sentence


narrator = Noun("Brandon Brodrick", False, "none", None, "male")
bobalina = Noun("Bobalina", False, "none", None, "female")
subject = Noun("cat", True, "specific", narrator, "none")
jump = Verb("jump")
adj = Adjective("high")
sty = Story(narrator, [narrator, subject, bobalina])
print(sty.generate_indepentant_clause(narrator, jump, "present", adj))
print(sty.generate_indepentant_clause(subject, jump, "past", adj))
print(sty.generate_indepentant_clause(bobalina, jump, "future", adj))
# print(sty.show_story())

