# Django core imports.
from django.core.management.base import BaseCommand
# Built-in libraries.
import os
import math
# PySpark libraries.
from pyspark.sql import SparkSession
from pyspark.mllib.recommendation import ALS, Rating


class Command(BaseCommand):
    help = 'Initialises spark based recommendation engine.'

    @staticmethod
    def get_rating_counts(id_and_ratings_tuple):
        rating_counts = len(id_and_ratings_tuple[1])
        return id_and_ratings_tuple[0], rating_counts

    def handle(self, *args, **options):
        # PATH declarations.
        os.environ['HADOOP_HOME'] = "C:\winutils"
        os.environ["SPARK_HOME"] = "C:\spark"
        os.environ["SPARK_CLASSPATH"] = "C:\spark\postgresql.jar"

        # Path for csv files for the test model.
        base_path = os.getcwd()
        full_path = (base_path +
                     "\\api_root\management\commands\dataset\\test_data.csv")

        # Database informations for the complete model.
        # db_url = "jdbc:postgresql://localhost:5432/" \
        #          "moviexplorer_service_layer?user=postgres&password=password"
        # db_table = "api_root_userratings"

        # Creates a SparkSession. No need to create a SparkContext.
        spark_session = SparkSession.builder.getOrCreate()

        # This causes some issues on Windows.
        # spark_session.sparkContext.setCheckpointDir("checkpoint")

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

        new_user_id = 0
        # The format of each line is (userID, movieID, rating)
        new_user_ratings = [
            Rating(0, 238, 5),
            Rating(0, 244786, 4.5),
            Rating(0, 77338, 5),
            Rating(0, 497, 5),
            Rating(0, 157336, 4.5),
            Rating(0, 27205, 5),
            Rating(0, 103, 4),
            Rating(0, 274, 4),
            Rating(0, 670, 4),
            Rating(0, 103663, 4)
        ]
        new_user_ratings_rdd = spark_session.sparkContext.parallelize(
            new_user_ratings
        )
        complete_data_with_new_ratings_rdd = test_data_ratings_rdd.union(
            new_user_ratings_rdd
        )

        test_model = ALS.train(
            ratings=complete_data_with_new_ratings_rdd, rank=best_rank,
            lambda_=regularization_parameter
        )

        movie_id_with_ratings_rdd = (
            complete_data_with_new_ratings_rdd.map(
                lambda row: (row[1], row[2])
            ).groupByKey()
        )
        movie_id_with_counts = movie_id_with_ratings_rdd.map(
            Command.get_rating_counts
        )

        # Gets just movie ids.
        new_user_ratings_ids = map(lambda x: x.product, new_user_ratings)

        # Keeps just those not on the id list.
        candidates = (test_data_movie_ids_rdd.filter(
            lambda x: x not in new_user_ratings_ids).map(
            lambda x: (new_user_id, x))
        )

        new_user_recommendations_rdd = test_model.predictAll(
            candidates
        )

        new_user_recommendations_rating_rdd = new_user_recommendations_rdd.map(
            lambda row: (row.product, row.rating)
        )

        new_user_recommendations_rating_count_rdd = \
            new_user_recommendations_rating_rdd.join(movie_id_with_counts)

        top_movies = new_user_recommendations_rating_count_rdd.filter(
            lambda row: row[1][1] >= 25
        ).takeOrdered(
            10, lambda row: -row[1][0]
        )

        print('TOP recommended movies (with more than 25 reviews):\n{}'.format(
            '\n'.join(map(str, top_movies)))
        )

        spark_session.stop()