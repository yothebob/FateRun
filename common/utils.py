import os
import base64
import json
import random
from common.models import Tag
from .varz import GENERATE_ENDPOINT, STATIC_HOSTNAME, STATIC_MUSIC_PATH, STORY_PROMPTS, DIALOG_FOLDER


def get_song_genre_intermissions(setting):
    song_type = Tag.objects.filter(prompt=setting).first()
    return [f"{STATIC_MUSIC_PATH}{song_type}/{name}" for name in os.listdir(f"{STATIC_MUSIC_PATH}{song_type.prompt}")]
            

def build_final_fstack(dialog_fnames, song_intermissions):
    res = []
    is_every_other = False
    for fname in dialog_fnames:
        # add a rando
        if not is_every_other:
            res.append(fname)
        else:
            res.append(song_intermissions[random.randint(0, (len(song_intermissions) - 1))])
            res.append(fname)
        is_every_other = not is_every_other
    return res

def combine_short_dialogs(dialog_list): #TODO: clean up
    min_limit = 200
    res_list = []
    current_res_index = 0
    for d in dialog_list:
        if len(d) < min_limit:
            if len(res_list) <= current_res_index:
                res_list.append(d)
            else:
                res_list[current_res_index] = res_list[current_res_index] + " " + d
        else:
            res_list.append(d)
            current_res_index += 1
    return res_list
