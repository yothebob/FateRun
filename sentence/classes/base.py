class StoryMixin(object):

    def __init__(self):
        self.story = None

    def get_story(self):
        return self.story

    def backlink(self, story):
        self.story = story
