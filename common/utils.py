import json
from rq.job import Job
import requests
from redis import Redis
from rq import Queue

r = Redis(host='localhost', port=6379, decode_responses=True)
q = Queue("generate", connection=r)
generate_endpoint = "http://localhost:11434/api/generate"

def queued_generate(stringified_data, uuid):
    res = requests.post(generate_endpoint, data=stringified_data)
    res_json = res.json()
    r.set(uuid.encode("utf8"), res_json["response"].encode("utf8"))

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

    def queue_generation(self, uuid):
        data = {
            "model": "llama3",
            "prompt": self.generate_prompt(),
            "stream": False
        }
        q.enqueue(queued_generate, args=(json.dumps(data), uuid))
        return True

    
