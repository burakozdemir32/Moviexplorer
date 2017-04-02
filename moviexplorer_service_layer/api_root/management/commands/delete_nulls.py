# Django imports.
from django.core.management.base import BaseCommand
from api_root.models import (Movie, MovieActorIndex, MovieDirectorIndex,
                             Person, MovieRatings)
from django.db import transaction
# Built-in libraries.
import json
import os
# Third-party libraries.
import tmdbsimple as tmdb
import omdb
import requests.exceptions as request_exceptions


class Command(BaseCommand):
    help = 'Creates the database for api_root project'

    def handle(self, *args, **options):
        # Base path of the project.
        base_path = os.getcwd()
        # Path for 'languages.json' file.
        full_path = (base_path +
                     "\\api_root\management\commands\languages.json")
        try:
            with open(full_path, encoding="utf8") as language_file:
                language_data = json.load(language_file)
                language_dict = language_data['languages']
        except OSError:
            print("File not found.")

        tmdb.API_KEY = '700e07d6e002c4a46ec229242049b0f3'
        # Creates a TMDB movie object.
        person = tmdb.People()
        '''
        Initial movie id for the loop below.
        If the command fails, change it with latest saved movie id + 1.
        '''
        person_id = 1710284
        # Gets the latest movie in TMDB.
        latest_person_id = person.latest(timeout=10)['id']

        while person_id <= latest_person_id:
            try:
                # Creates a new TMDB movie object by id.
                person = tmdb.People(person_id)

                try:
                    # Queries TMDB information for the id above.
                    tmdb_info = person.info(
                        timeout=10
                    )

                    if tmdb_info['name'] == '' or tmdb_info['name'] is None:
                        person_id += 1
                        continue

                    if tmdb_info['biography'] == '':
                        biography = None
                    else:
                        biography = tmdb_info['biography']

                    if tmdb_info['profile_path'] == '':
                        image_path = None
                    else:
                        image_path = tmdb_info['profile_path']
                # Handles Read Timeout Error.
                except request_exceptions.ReadTimeout:
                    print('HTTP Read Timeout occurred.')
                    continue

                # Creates and saves a movie object to database.
                Person.objects.create(
                    id=person_id,
                    name=tmdb_info['name'],
                    biography=biography,
                    person_image_path=image_path,
                )

                print('Latest saved person id: {}'.format(person_id))
                person_id += 1
            # Handles 404 Not Found Error.
            except request_exceptions.HTTPError:
                print('Person not found.')
                person_id += 1

        print('Your database is up to date.')