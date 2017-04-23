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

    def handle(self, *args, **options):
        # PATH declarations.
        os.environ['HADOOP_HOME'] = "C:\winutils"
        os.environ["SPARK_HOME"] = "C:\spark"

        # Path for csv files.
        base_path = os.getcwd()
        full_path = (base_path +
                     "\\api_root\management\commands\dataset\\test_data.csv")

        spark_session = SparkSession.builder.getOrCreate()

        # This causes some issues on Windows.
        # spark_session.sparkContext.setCheckpointDir("checkpoint")

        data_frame = spark_session.read.option("header", "true").csv(
            full_path
        ).cache()

        data = data_frame.rdd.map(
            lambda row: Rating(int(row["user_id"]), int(row["movie_id"]),
                               float(row["rating"]))
        )

        ranks = [2, 4, 8, 12, 20, 40, 100]
        errors = [0, 0, 0, 0, 0, 0, 0]
        err = 0
        min_error = float('Inf')
        best_rank = -1
        regularization_parameter = 0.1

        # Splits the dataset into 3 different parts.
        train, validation, test = data.randomSplit(weights=[6.0, 2.0, 2.0])

        validation_for_predict = validation.map(
            lambda row: (row.user, row.product)
        )
        test_for_predict = test.map(
            lambda row: (row.user, row.product)
        )

        # Iterates over ranks and selects the best.
        for rank in ranks:
            model = ALS.train(ratings=train, rank=rank,
                              lambda_=regularization_parameter)

            predictions = model\
                .predictAll(validation_for_predict)\
                .map(lambda row: ((row.user, row.product), row.rating))

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

        print('The best model was trained with rank {}'.format(best_rank))

        # Retrains the model with the best rank.
        model = ALS.train(ratings=train, rank=best_rank, lambda_=0.1)

        predictions = model.predictAll(test_for_predict)\
            .map(
            lambda row: ((row.user, row.product), row.rating)
        )

        rates_and_preds = test.map(
            lambda row: (
                (int(row.user), int(row.product)), float(row.rating))
        ).join(
            predictions
        )

        error = math.sqrt(
            rates_and_preds.map(
                lambda row: (row[1][0] - row[1][1]) ** 2
            ).mean()
        )

        print('For testing data the RMSE is {}'.format(error))
