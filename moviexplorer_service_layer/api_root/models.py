from django.db import models
from django.contrib.postgres.fields import ArrayField


class MovieRatings(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.OneToOneField('Movie', on_delete=models.CASCADE)
    imdb_votes = models.IntegerField(null=True, blank=True)
    imdb_rating = models.FloatField(null=True, blank=True)
    metascore = models.FloatField(null=True, blank=True)
    tomato_meter = models.FloatField(null=True, blank=True)
    tomato_user_meter = models.FloatField(null=True, blank=True)
    tomato_user_reviews = models.IntegerField(null=True, blank=True)
    tomato_reviews = models.IntegerField(null=True, blank=True)
    tmdb_vote_count = models.IntegerField(null=True, blank=True)
    tmdb_vote_average = models.FloatField(null=True, blank=True)
    average_rating = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return 'IMDb Id: {} Average Rating: {}'.format(
            self.rating_id, self.average_rating
        )


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    imdb_id = models.IntegerField(null=True, blank=True)
    budget = models.FloatField(null=True, blank=True)
    revenue = models.FloatField(null=True, blank=True)
    poster_path = models.CharField(max_length=100, null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    genres = ArrayField(models.CharField(max_length=30), null=True, blank=True)
    keywords = ArrayField(models.CharField(max_length=150), null=True,
                          blank=True)
    certification = models.CharField(max_length=30, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    spoken_languages = ArrayField(models.CharField(max_length=30), null=True,
                                  blank=True)
    production_countries = ArrayField(models.CharField(max_length=40),
                                      null=True, blank=True)
    tagline = models.TextField(null=True, blank=True)
    backdrop_path = models.CharField(max_length=100, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    original_title = models.CharField(max_length=200, null=True, blank=True)
    runtime = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return 'Movie Id: {} Movie Title: {} '.format(
            self.id, self.title.encode('utf-8')
        )


class Person(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    person_image_path = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return 'Person Id: {}, Person Name: {}'.format(
            self.id, self.name.encode('utf-8')
        )


class MovieDirectorIndex(models.Model):
    director_id = models.IntegerField()
    movie_id = models.IntegerField()

    def __str__(self):
        return 'Director Id: {}, Movie Id: {}'.format(
            self.director_id, self.movie_id
        )


class MovieActorIndex(models.Model):
    actor_id = models.IntegerField()
    movie_id = models.IntegerField()

    def __str__(self):
        return 'Actor Id: {}, Movie Id: {}'.format(
            self.actor_id, self.movie_id
        )


class UserRatings(models.Model):
    user_id = models.IntegerField()
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    rating = models.FloatField()

    def __str__(self):
        return 'User Id: {}, Movie Id: {}, Rating: {]'.format(
            self.user_id, self.movie, self.rating
        )