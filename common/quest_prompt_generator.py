import base64
import json
from rq.job import Job
import requests
from redis import Redis
from rq import Queue
from pyt2s.services import stream_elements
from .varz import GENERATE_ENDPOINT, STATIC_HOSTNAME, STATIC_MUSIC_PATH, STORY_PROMPTS, DIALOG_FOLDER
from common.models import Quest, DialogList, Dialog
import os
from django.conf import settings
import random
import django_rq
from openai import OpenAI
from common.utils import build_final_fstack, combine_short_dialogs, get_song_genre_intermissions, create_dialog_list

r = Redis(host='127.0.0.1', port=6379, decode_responses=True)
q = django_rq.get_queue('generate')

        
def queued_generate(stringified_data, uuid, setting, voice, use_openai=False):
    res = requests.post(GENERATE_ENDPOINT, data=stringified_data)
    res_json = res.json()
    obj = stream_elements.StreamElements() if not use_openai else OpenAI(api_key=settings.OPENAI_KEY)
    found_quest = Quest.objects.filter(uuid=uuid).first() # for now lets just assume this will be ok
    response_list = list(filter(lambda i: i, res_json["response"].split("\n")))
    found_quest.name = response_list.pop(0).replace('\"','')
    # idk about storing the result thats alot of data
    found_quest.save()
    response_list = combine_short_dialogs(response_list)
    tts_responses = {}
    new_dialog_list = []
    for idx, dialog in enumerate(response_list):
        cleaned_name = STATIC_MUSIC_PATH + DIALOG_FOLDER + f"{uuid[:10]}-{found_quest.name.replace(' ', '')}-{idx}" + ".mp3"
        tts_responses[cleaned_name] = dialog
    for fname, dialog in tts_responses.items():
        # Custom Voice
        if not use_openai:
            response = obj.requestTTS(dialog, voice)
            with open(fname, '+wb') as file:
                file.write(response)
        else:
            response = obj.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=dialog,
            )
            response.stream_to_file(fname)
        url = fname.replace(STATIC_MUSIC_PATH,STATIC_HOSTNAME)
        new_dialog = Dialog(quest=found_quest, index=len(new_dialog_list), url=url, tags=found_quest.tags)
        new_dialog.save()
        new_dialog_list.append(new_dialog)
    song_intermissions = get_song_genre_intermissions(setting) #TODO: create a django command to load songs in.
    final_file_stack = build_final_fstack(new_dialog_list, song_intermissions)
    dlist_json = create_dialog_list(final_file_stack)
    quest_dlist = DialogList(quest=found_quest, dlist=json.dumps(dlist_json))
    quest_dlist.save()
    return True
    


class Prompt:

    templates = []
    motivation_multiplier = ["None", "low", "medium", "high"]
    voice_options = {
        "local": ["Brian",
                  "Amy",
                  "Emma",
                  "Geraint",
                  "Russell",
                  "Nicole",
                  "Joey",
                  "Justin",
                  "Matthew",
                  "Ivy",
                  "Joanna",
                  "Kendra",
                  "Kimberly",
                  "Salli",
                  "Raveena"
                  ],
        "openai": ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    }
    
    def __init__(self, setting: str, story_length: int, motivation_freq: str, ai_tool = "local", voice = "Matthew"):
        self.perspective = "first person point of view"
        self.motivation = self.motivation_multiplier.index(motivation_freq)
        self.setting = setting
        self.story_length = story_length
        self.ai_tool = ai_tool or "local"
        self.voice = voice or "Matthew"
        if self.voice not in self.voice_options[self.ai_tool]:
            raise Exception("Voice not supported for that generation tool.")

    def generate_prompt(self):
        motivation_times = "tbd"
        selected_prompt = random.choice(STORY_PROMPTS)
        return selected_prompt.format(self.perspective, self.story_length, self.setting)
    
    def queue_generation(self, uuid):
        if self.ai_tool == "local":
            data = {
                "model": "llama3",
                "prompt": self.generate_prompt(),
                "stream": False
            }
        else: # TODO: integrate openai prompt res
            data = {
                "model": "llama3",
                "prompt": self.generate_prompt(),
                "stream": False
            }
        q.enqueue(queued_generate, json.dumps(data), uuid, self.setting, self.voice, self.ai_tool == "openai")
        return True


    
