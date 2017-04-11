# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-11 17:59
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('imdb_id', models.IntegerField(blank=True, null=True)),
                ('budget', models.FloatField(blank=True, null=True)),
                ('revenue', models.FloatField(blank=True, null=True)),
                ('poster_path', models.CharField(blank=True, max_length=100, null=True)),
                ('overview', models.TextField(blank=True, null=True)),
                ('genres', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=30), blank=True, null=True, size=None)),
                ('keywords', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=150), blank=True, null=True, size=None)),
                ('certification', models.CharField(blank=True, max_length=30, null=True)),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('spoken_languages', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=30), blank=True, null=True, size=None)),
                ('production_countries', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=40), blank=True, null=True, size=None)),
                ('tagline', models.TextField(blank=True, null=True)),
                ('backdrop_path', models.CharField(blank=True, max_length=100, null=True)),
                ('release_date', models.DateField(blank=True, null=True)),
                ('original_title', models.CharField(blank=True, max_length=200, null=True)),
                ('runtime', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MovieActorIndex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actor_id', models.IntegerField()),
                ('movie_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MovieDirectorIndex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('director_id', models.IntegerField()),
                ('movie_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MovieRatings',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('imdb_votes', models.IntegerField(blank=True, null=True)),
                ('imdb_rating', models.FloatField(blank=True, null=True)),
                ('metascore', models.FloatField(blank=True, null=True)),
                ('tomato_meter', models.FloatField(blank=True, null=True)),
                ('tomato_user_meter', models.FloatField(blank=True, null=True)),
                ('tomato_user_reviews', models.IntegerField(blank=True, null=True)),
                ('tomato_reviews', models.IntegerField(blank=True, null=True)),
                ('tmdb_vote_count', models.IntegerField(blank=True, null=True)),
                ('tmdb_vote_average', models.FloatField(blank=True, null=True)),
                ('average_rating', models.IntegerField(blank=True, null=True)),
                ('movie', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api_root.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('biography', models.TextField(blank=True, null=True)),
                ('person_image_path', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]