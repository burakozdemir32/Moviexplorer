# Built-in libraries.
import os
import math
# PySpark libraries.
from pyspark.sql import SparkSession
from pyspark.mllib.recommendation import ALS, Rating, MatrixFactorizationModel
# Django core imports.
from django.core.management.base import BaseCommand
# Django app imports.
from api_root.models import (UserRatings, Recommendations)


class Command(BaseCommand):
    help = 'Initialises spark based recommendation engine.'

    @staticmethod
    def get_rating_counts(movie_id_with_ratings_rdd):
        movie_id_with_ratings_dict = dict()
        for item in movie_id_with_ratings_rdd:
            movie_id = item[0]
            rating_counts = len(item[1])
            movie_id_with_ratings_dict[movie_id] = rating_counts

        return movie_id_with_ratings_dict

    def handle(self, *args, **options):
        # Path for csv files for the test model.
        base_path = os.getcwd()
        full_path = (base_path +
                     "\\api_root\management\commands\dataset\\test_data.csv")
        model_path = (base_path +
                      "\\api_root\management\commands\models")

        # Database informations for the complete model.
        # db_url = "jdbc:postgresql://localhost:5432/" \
        #          "moviexplorer_service_layer?user=postgres&password=password"
        # db_table = "api_root_userratings"

        # Creates a SparkSession. No need to create a SparkContext.
        spark_session = SparkSession.builder.getOrCreate()
        spark_context = spark_session.sparkContext
        spark_context.setCheckpointDir("checkpoint")

        test_data = spark_session.read.option("header", "true").csv(
            full_path
        ).cache()

        test_data_ratings_rdd = test_data.rdd.map(
            lambda row: Rating(int(row.user_id), int(row.movie_id),
                               float(row.rating))
        ).cache()
        test_data_movie_ids_rdd = test_data.select(
            'movie_id'
        ).distinct().rdd.map(
            lambda row: int(row.movie_id)
        ).cache()

        ranks = [2, 4, 8, 10, 12, 20, 40, 80, 100]
        errors = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        err = 0
        min_error = float('Inf')
        best_rank = -1
        regularization_parameter = 0.1

        # Splits the test dataset into 2 different parts.
        training, validation = test_data_ratings_rdd.randomSplit(
            weights=[8.0, 2.0]
        )

        validation_for_predict = validation.map(
            lambda row: (row.user, row.product)
        )

        # Iterates over ranks and selects best.
        for rank in ranks:
            test_model = ALS.train(ratings=training, rank=rank,
                                   lambda_=regularization_parameter)

            predictions = test_model.predictAll(
                validation_for_predict
            ).map(
                lambda row: ((row.user, row.product), row.rating)
            )

            rates_and_preds = validation.map(
                lambda row: ((int(row.user), int(row.product)),
                             float(row.rating))
            ).join(
                predictions
            )

            error = math.sqrt(
                rates_and_preds.map(
                    lambda row:  (row[1][0] - row[1][1]) ** 2
                ).mean()
            )
            errors[err] = error
            err += 1

            print('For rank {} the RMSE is {}'.format(rank, error))

            if error < min_error:
                min_error = error
                best_rank = rank
        print('For the validation data the RMSE is {}'.format(error))
        print('The test model was trained with rank {}'.format(best_rank))

        # All the user ids who rated a movie.(Local users, not MovieLens's)
        user_ids = UserRatings.objects.values_list(
            'user_id', flat=True
        ).distinct()

        # The format of each line is (user_id, movie_id, rating)
        user_ratings = UserRatings.objects.all()
        user_ratings = list(
            map(lambda row: Rating(row.user_id, row.movie_id, row.rating),
                user_ratings)
        )

        user_ratings_rdd = spark_context.parallelize(
            user_ratings
        )
        complete_data_with_user_ratings_rdd = test_data_ratings_rdd.union(
            user_ratings_rdd
        ).cache()

        test_model = ALS.train(ratings=complete_data_with_user_ratings_rdd,
                               rank=best_rank, lambda_=regularization_parameter
                               )
        # Saves the model.
        # test_model.save(spark_context, model_path)

        movie_id_with_ratings_rdd = (
            complete_data_with_user_ratings_rdd.map(
                lambda row: (row[1], row[2])
            ).groupByKey()
        )
        movie_id_with_counts = Command.get_rating_counts(
            movie_id_with_ratings_rdd.collect()
        )

        for user_id in user_ids:
            # Gets just movie ids for user_id.
            user_movies = list(
                map(lambda row: row.product, user_ratings)
            )

            # Keeps just those not on the id list.
            candidates = test_data_movie_ids_rdd.filter(
                lambda x: x not in user_movies
            ).map(lambda x: (user_id, x))

            new_user_recommendations_rdd = test_model.predictAll(candidates)
            new_user_recommendations_rating_rdd = new_user_recommendations_rdd.map(
                lambda row: (row.user, row.product, row.rating,
                             movie_id_with_counts[row.product])
            )

            top_recommendations = new_user_recommendations_rating_rdd.filter(
                lambda row: row[3] >= 50
            ).takeOrdered(10, lambda row: -row[2])

            print('TOP 10 recommended movies (with more than 50 reviews):')
            for recommendation in top_recommendations:
                print('User id: {} Movie id: {}'.format(
                    recommendation[0], recommendation[1])
                )
                Recommendations.objects.get_or_create(user_id=recommendation[0],
                                                      movie_id=recommendation[1])

        spark_session.stop()
