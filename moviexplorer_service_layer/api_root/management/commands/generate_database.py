# Built-in libraries.
import json
import os

# Third-party libraries.
import tmdbsimple as tmdb
import omdb
import requests.exceptions as request_exceptions

# Django core imports.
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError

# Django app imports.
from api_root.models import (Movie, MovieActorIndex, MovieDirectorIndex,
                             Person, MovieRatings)


class Command(BaseCommand):
    help = 'Initialise the database for the Moviexplorer project'

    @staticmethod
    def get_person_information(person_list):
        """Creates relations between movies and actors, if any.

        :param person_list: Person list of a movie.
        :raises ReadTimeout: If the request does not response in 10 seconds.
                HTTPError: If person does not found. (Via main function)
        """
        person_info_list = []

        for person_id in person_list:
            # Creates a new TMDB person object by id.
            person = tmdb.People(person_id)

            # Queries TMDB information for the person list.
            while True:
                try:
                    person_info = person.info(
                        timeout=10
                    )
                except request_exceptions.ReadTimeout:
                    print('HTTP Read Timeout occurred.')
                    continue
                break

            if person_info['name'] == '':
                person_info['name'] = None

            if person_info['biography'] == '':
                person_info['biography'] = None

            if person_info['profile_path'] == '':
                person_info['profile_path'] = None

            person_info_list.append(person_info)

        return person_info_list

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
        movie = tmdb.Movies()
        '''
        Initial movie id for the loop below.
        If the command fails, change it with latest saved movie id + 1.
        '''
        movie_id = 147965
        # Gets the latest movie in TMDB.
        latest_movie_id = movie.latest(timeout=10)['id']
        # The maximum actor count is 10.
        max_cast_count = 10

        while movie_id <= 147965:
            # Declarations of arrays that manipulated below.
            genres = []
            keywords = []
            spoken_languages = []
            prod_countries = []
            cast = []
            crew = []
            # Certification and average rating are null by default.
            certification = None
            average_rating = None
            # We need an initial value for them.
            total_rating = 0
            rating_count = 0

            try:
                # Creates a new TMDB movie object by id.
                movie = tmdb.Movies(movie_id)

                try:
                    # Queries TMDB information for the id above.
                    tmdb_info = movie.info(
                        timeout=10,
                        append_to_response='releases,keywords,credits'
                    )
                    imdb_id = tmdb_info['imdb_id']

                    # Checks if there is an 'imdb_id' in 'tmdb_info' dict.
                    if imdb_id == '' or imdb_id is None:
                        print("No imdb id in TMDB query.")
                        movie_id += 1
                        continue

                    # Queries OMDB information by 'imdb_id'.
                    try:
                        omdb_info = omdb.imdbid(imdb_id, timeout=10,
                                                tomatoes=True)
                    except json.decoder.JSONDecodeError:
                        movie_id += 1
                        continue
                    # Imdb id should be an integer for the database.
                    imdb_id = int(imdb_id.replace('tt', ''))
                # Handles Read Timeout Error.
                except request_exceptions.ReadTimeout:
                    print('HTTP Read Timeout occurred.')
                    continue

                '''
                If release date is empty string(''), it causes an error.
                To prevent the error, a null value is assigned.
                '''
                release_date = tmdb_info['release_date'] \
                    if tmdb_info['release_date'] != '' else None

                '''
                If OMDB API returns an empty object if block will be executed
                Otherwise else block will be executed and average rating
                will be calculated.
                '''
                if not omdb_info:
                    omdb_info = {
                        'imdb_rating': None,
                        'imdb_votes': None,
                        'metascore': None,
                        'tomato_meter': None,
                        'tomato_user_meter': None,
                        'tomato_user_reviews': None,
                        'tomato_reviews': None
                    }
                else:
                    for key in omdb_info:
                        if omdb_info[key] in ['NA', 'N/A', '']:
                            omdb_info[key] = None
                        else:
                            if key == 'imdb_rating':
                                total_rating += float(omdb_info[key]) * 10
                                rating_count += 1
                            if key == 'imdb_votes':
                                omdb_info[key] = int(
                                    omdb_info[key].replace(',', '')
                                )
                            if key in ['metascore', 'tomato_meter',
                                       'tomato_user_meter']:
                                total_rating += float(omdb_info[key])
                                rating_count += 1
                    if rating_count >= 1:
                        average_rating = round(total_rating / rating_count)

                # Gets the certification for The United States.
                for cert_info in tmdb_info['releases']['countries']:
                    if cert_info['iso_3166_1'].upper() == 'US':
                        if cert_info['certification'] in ['Approved', 'G',
                                                          'NC-17', 'NR',
                                                          'PG', 'PG-13',
                                                          'R', 'UR']:
                            certification = cert_info['certification']

                '''
                Some fields in returned API calls have more than one object.
                For the array fields in the DB, these loops make them an array
                object.
                '''
                for genre_info in tmdb_info['genres']:
                    genres.append(genre_info['name'])

                for keyword_info in tmdb_info['keywords']['keywords']:
                    keywords.append(keyword_info['name'])

                for lang_info in tmdb_info['spoken_languages']:
                    spoken_language = language_dict[lang_info['iso_639_1']]
                    spoken_languages.append(spoken_language)

                for production_info in tmdb_info['production_countries']:
                    prod_countries.append(production_info['name'])

                for cast_info in tmdb_info['credits']['cast']:
                    if len(cast) < max_cast_count:
                        cast.append(cast_info['id'])

                for crew_info in tmdb_info['credits']['crew']:
                    if crew_info['job'] == 'Director':
                        crew.append(crew_info['id'])

                # This statement guarantees atomicity of the database.
                with transaction.atomic():
                    # Creates and saves a movie object to database.
                    movie = Movie.objects.create(
                        id=movie_id,
                        imdb_id=imdb_id,
                        budget=tmdb_info['budget'],
                        revenue=tmdb_info['revenue'],
                        poster_path=tmdb_info['poster_path'],
                        overview=tmdb_info['overview'],
                        genres=genres,
                        keywords=keywords,
                        certification=certification,
                        title=tmdb_info['title'],
                        spoken_languages=spoken_languages,
                        production_countries=prod_countries,
                        tagline=tmdb_info['tagline'],
                        backdrop_path=tmdb_info['backdrop_path'],
                        release_date=release_date,
                        original_title=tmdb_info['original_title'],
                        runtime=tmdb_info['runtime'],
                    )
                    # Creates and saves a rating object to database.
                    MovieRatings.objects.create(
                        movie=movie,
                        imdb_rating=omdb_info['imdb_rating'],
                        imdb_votes=omdb_info['imdb_votes'],
                        metascore=omdb_info['metascore'],
                        tomato_meter=omdb_info['tomato_meter'],
                        tomato_user_meter=omdb_info['tomato_user_meter'],
                        tomato_user_reviews=omdb_info['tomato_user_reviews'],
                        tomato_reviews=omdb_info['tomato_reviews'],
                        tmdb_vote_count=tmdb_info['vote_count'],
                        tmdb_vote_average=tmdb_info['vote_average'],
                        average_rating=average_rating
                    )
                print('Latest saved movie id: {}'.format(movie_id))

                cast_info = Command.get_person_information(cast)

                # TODO These lines below should be in a function.
                # Creates relations between movies and actors.
                for actor in cast_info:
                    try:
                        Person.objects.create(
                            id=actor['id'],
                            name=actor['name'],
                            biography=actor['biography'],
                            person_image_path=actor['profile_path']
                        )
                        print('Latest saved person id: {}'.format(actor['id']))
                    except IntegrityError:
                        print('Person already exists. Id: {}'.format(
                            actor['id'])
                        )

                    MovieActorIndex.objects.create(
                        actor_id=actor['id'],
                        movie_id=movie_id
                    )

                crew_info = Command.get_person_information(crew)

                # TODO These lines below should be in a function as well.
                # Creates relations between movies and directors.
                for director in crew_info:
                    try:
                        Person.objects.create(
                            id=director['id'],
                            name=director['name'],
                            biography=director['biography'],
                            person_image_path=director['profile_path']
                        )
                        print('Latest saved person id: {}'.format(
                            director['id'])
                        )
                    except IntegrityError:
                        print('Person already exists. Id: {}'.format(
                            director['id'])
                        )

                    MovieDirectorIndex.objects.create(
                        director_id=director['id'],
                        movie_id=movie_id
                    )

                movie_id += 1
            # Handles 404 Not Found Error.
            except request_exceptions.HTTPError:
                print('Object not found. Id: {}'.format(movie_id))
                movie_id += 1

        print('The database is up to date.')
