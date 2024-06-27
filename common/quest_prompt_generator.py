import base64
import json
from rq.job import Job
import requests
from redis import Redis
from rq import Queue
from pyt2s.services import stream_elements
from .varz import GENERATE_ENDPOINT, STATIC_HOSTNAME, STATIC_MUSIC_PATH, STORY_PROMPTS, DIALOG_FOLDER
from common.models import Quest, DialogList
import os
import random
import django_rq
from common.utils import build_final_fstack, combine_short_dialogs

r = Redis(host='127.0.0.1', port=6379, decode_responses=True)
q = django_rq.get_queue('generate')

class QuestPrompt():

    song_type_map = {
        "medieval": "medieval",
        "scifi": "scifi"
    }
    
    def __init__(self, setting="medieval"):
        self.setting = setting
        self.song_type_map = {
            "medieval": ["feudal","medieval","gothic","chivalric","knightly","dark ages","middle ages","arthurian","norman","byzantine","legendary","mythical","sorcery","enchanted","epic","heroic","dragon","quest","castle","magical","elven"],
            "scifi": ["futuristic","scifi", "speculative","space","cyberpunk","alien","dystopian","extraterrestrial","steampunk","technological","post-apocalyptic","intergalactic","time travel","artificial intelligence","robot","spaceship","virtual reality","utopian","astrobiology","terraforming","quantum"],
            "western": ["frontier","western","cowboy","wild west","prairie","outlaw","desert","pioneer","rodeo","ranch","gold rush","cattle drive","saloon","homestead","lasso","posse","wagon train","spur","sheriff","six-shooter","horseback"]
        }
        
    def qp_get_song_genre_intermissions(self):
        # for 
        song_type = "medieval"# self.song_type_map.get(self.setting, "medieval")
        return [f"{STATIC_MUSIC_PATH}{song_type}/{name}" for name in os.listdir(f"{STATIC_MUSIC_PATH}{song_type}")]

    
def get_song_genre_intermissions(setting):
    qp = QuestPrompt(setting)
    return qp.qp_get_song_genre_intermissions()
            

def queued_generate(stringified_data, uuid, setting):
    res = requests.post(GENERATE_ENDPOINT, data=stringified_data)
    res_json = res.json()
    obj = stream_elements.StreamElements()
    found_quest = Quest.objects.filter(uuid=uuid).first() # for now lets just assume this will be ok
    response_list = list(filter(lambda i: i, res_json["response"].split("\n")))
    found_quest.name = response_list.pop(0).replace('\"','')
    found_quest.save()
    response_list = combine_short_dialogs(response_list)
    tts_responses = {}
    for idx, dialog in enumerate(response_list):
        cleaned_name = STATIC_MUSIC_PATH + DIALOG_FOLDER + f"{uuid[:10]}-{found_quest.name.replace(' ', '')}-{idx}" + ".mp3"
        tts_responses[cleaned_name] = dialog
    for fname, dialog in tts_responses.items():
        # Custom Voice
        data = obj.requestTTS(dialog, 'Matthew')
        with open(fname, '+wb') as file:
            file.write(data)
    song_intermissions = get_song_genre_intermissions(setting)
    final_file_stack = build_final_fstack(tts_responses.keys(), song_intermissions)
    for idx, filename in enumerate(final_file_stack):
        url = filename.replace(STATIC_MUSIC_PATH,STATIC_HOSTNAME)
        new_dialog = DialogList(quest=found_quest, index=idx, url=url)
        new_dialog.save()
    return True
    


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
        selected_prompt = random.choice(STORY_PROMPTS)
        return selected_prompt.format(self.perspective, self.story_length, self.setting)
    
    def queue_generation(self, uuid):
        data = {
            "model": "llama3",
            "prompt": self.generate_prompt(),
            "stream": False
        }
        q.enqueue(queued_generate, json.dumps(data), uuid, self.setting)
        return True


    
