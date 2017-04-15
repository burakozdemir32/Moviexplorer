# Built-in libraries.
import csv
import os
# Django core imports.
from django.core.management.base import BaseCommand
from django.db import IntegrityError
# Django app imports.
from api_root.models import (UserRatings)


class Command(BaseCommand):
    help = 'Reads movie lens user ratings and saves them to the database.'

    def handle(self, *args, **options):
        # Base path of the project.
        base_path = os.getcwd()
        # Path for csv files.
        full_path = (base_path +
                     "\\api_root\management\commands\ml-latest-small")

        try:
            with open(full_path + '\\ratings.csv') as ratings_file, \
                    open(full_path + '\links.csv') as links_file:
                ratings = csv.DictReader(ratings_file)
                links = csv.DictReader(links_file)

                links_dict = dict(
                    (link['movieId'], link['tmdbId']) for link in links
                )

                for rating in ratings:
                    # Gets tmdbId for the database.
                    movie_id = links_dict[rating['movieId']]

                    if movie_id is not None and movie_id != '':
                        try:
                            UserRatings.objects.create(
                                user_id=int(rating['userId']),
                                movie_id=int(movie_id),
                                rating=float(rating['rating'])
                            )
                            print(
                                'Latest saved rating with User id: {}, '
                                'Movie id: {}'.format(
                                    rating['userId'], movie_id
                                )
                            )
                        except IntegrityError:
                            print(
                                'User rating could not be saved. Movie id {} '
                                'is not present in the movie table'.format(
                                    movie_id
                                )
                            )
        except OSError:
            print("File not found.")


