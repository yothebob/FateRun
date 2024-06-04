
"generate a first person point of view story approximately 300 words long in a futuristic scifi space setting, the reader will be running while reading so please give occasional story motivations to run. Please ONLY generate the story."


class Prompt:

    templates = []
    motivation_multiplier = ["None", "low", "medium", "high"]
    
    def __init__(self, setting: str, story_length: int, motivation_freq: str):
        self.perspective = "first person point of view"
        self.motivation = self.motivation_multiplier.index(motivation_freq)
        self.setting = setting
        self.story_length = story_length

    def generate_prompt(self):
        motivation_times = "tbd"
        return f"Generate a {self.perspective} story approximately {self.story_length} words long in a {self.setting} setting, the reader will be running while reading so please give occasional story motivations to run. Please ONLY generate the story."


    
