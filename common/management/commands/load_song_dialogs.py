import os
from django.core.management.base import BaseCommand
from common.models import Song, Tag
from django.conf import settings

class Command(BaseCommand):
    help = "Load new songs in the static folders as dialog objects in db"

    def add_arguments(self, parser):
        parser.add_argument("path", type=str)

    def handle(self, *args, **options):
        ignore_folders = ["dialogs", "admin", "rest_framework"]
        song_folder = os.listdir(options["path"])
        for tag_type in song_folder:
            if tag_type not in ignore_folders:
                found_tag = Tag.objects.filter(name=tag_type).first()
                if not found_tag:
                    found_tag = Tag(name=tag_type, prompt=tag_type)
                    found_tag.save()
                    print(f"make new tag {tag_type}")
                for song in os.listdir(f"{options['path']}/{tag_type}"):
                    found_song = Song.objects.filter(fname=song).first()
                    if not found_song:
                        found_song = Song(
                            url = settings.STATIC_HOSTNAME + tag_type + "/" + song,
                            fname = song,
                            name = song,
                            author = "na",
                            image = "na",
                            tags = found_tag
                        )
                        found_song.save()
