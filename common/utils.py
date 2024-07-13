import os
import base64
import json
import random
from common.models import Tag, Song, Dialog
from .varz import GENERATE_ENDPOINT, STATIC_HOSTNAME, STATIC_MUSIC_PATH, STORY_PROMPTS, DIALOG_FOLDER

def create_dialog_list(final_file_stack):
    res = []
    for item in final_file_stack:
        if isinstance(item, Dialog):
            res.append({
                "index": item.index,
                "url": item.url
            })
        else:
            res.append({
                "url": item.url,
                "name": item.name,
                "author": item.author,
                "image": item.image
            })
    return res

def get_song_genre_intermissions(setting):
    song_type = Tag.objects.filter(prompt=setting).first()
    songs = Song.objects.filter(tags=song_type).all()
    return songs
    # return [f"{STATIC_MUSIC_PATH}{song_type.name}/{name}" for name in os.listdir(f"{STATIC_MUSIC_PATH}{song_type.name}")]
            

def build_final_fstack(dialog_fnames, song_intermissions):
    res = []
    song_intermissions = list(song_intermissions)
    song_intermission_copy = list(song_intermissions)
    is_every_other = False
    for fname in dialog_fnames:
        if not is_every_other:
            res.append(fname)
        else:
            chosen_song = None
            if len(song_intermissions) > 1:
                chosen_song = song_intermissions.pop(random.randint(0, (len(song_intermissions) - 1)))
            else:
                song_intermissions = list(song_intermission_copy)
                if len(song_intermissions) > 0:
                    chosen_song = song_intermissions.pop(random.randint(0, (len(song_intermissions) - 1)))
            if chosen_song:
                res.append(chosen_song)
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
