import uuid
from typing import Literal, Type, Any, List
from .nouns import Noun
from .verbs import Verb
# from sentence.utils import capitalize

class CliffHanger:
    story_format = ["introduction", "rise", "climax", "cliffhanger"]

    def make_introduction(self, story):
        """
        As I sprint through the dense underbrush, my armor clanking against the trees, I can feel the weight of the cursed forest bearing down on me. The villagers called it \"Wychwood's Wrath\" – a place where the very land itself seemed to conspire against those who dared enter.

        My name is Edwin, and I'm a Knight of St. Michael's Order. Our order has been tasked with uncovering the source of the dark magic plaguing our lands. Legends speak of an ancient sorcerer, Azrael, who once dwelled within these woods, wielding powers beyond mortal comprehension. Some say he still walks among the trees, seeking revenge on those who would seek to undo his work.

        """
        pass

    def make_rise(self, story):
        """
        I've heard whispers of a hidden temple deep within Wychwood's Wrath, where Azrael's most powerful artifacts lie in wait. My mission is to find it before the forces of darkness do.

        As I burst through a thicket of blackthorn, a figure emerges from the shadows – a hooded woman, her eyes burning with an otherworldly intensity. She speaks in hushed tones, warning me of the dangers ahead: \"Turn back now, Edwin, while you still can.\"

        But I'm driven by duty and a hint of curiosity. The forest seems to grow darker, the air thickening with malevolent energy. I push on, following a narrow path that winds deeper into the woods.
        """

    def make_climax(self, story):
        """
        Suddenly, the trees part, revealing a clearing bathed in an eerie, pulsing light. In its center stands a massive stone statue of Azrael himself, his eyes aglow with an unholy power. The woman's words echo in my mind: \"This is where the cursed forest begins.\"

        """
        pass

    def make_cliffhanger(self, story):
        """
        I charge forward, sword drawn, as the statue's eyes begin to flash with malevolent energy. A dark, swirling vortex erupts from its base, pulling me toward some unseen abyss...
        """
        pass
    
class Tragedy:
    story_format = ["introduction", "rise", "climax", "fall", "catastrophe"]

    
class Story:
    #TODO: this will store story arc, noun ambitions, tenses, story context & sentence context and etc
    # ^ the story will basically be generating all these things
    def __init__(self, narrator: Type[Noun], nouns: List[Noun], word_length: int =300):
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
        sentence = f"{subject.__str__()} {sentance_verb} {optional_noun_adj}. "
        self.story_update([subject], sentence)
        return sentence
