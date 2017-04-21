from django.core.management.base import BaseCommand

import os, math

from pyspark.sql import SparkSession
from pyspark.mllib.recommendation import ALS, Rating


class Command(BaseCommand):
    help = 'Initialises spark based recommendation engine.'

    def handle(self, *args, **options):
        # PATH declarations.
        os.environ['HADOOP_HOME'] = "C:\winutils"
        os.environ["SPARK_HOME"] = "C:\spark"

        base_path = os.getcwd()
        # Path for csv files.
        full_path = (base_path +
                     "\\api_root\management\commands\ml-latest-small\\test.csv")

        spark_session = SparkSession.builder.getOrCreate()

        # This causes some issues on Windows.
        # spark_session.sparkContext.setCheckpointDir("checkpoint")

        df = spark_session.read.option("header", "true").csv(full_path)

        data = df.rdd.map(lambda row: Rating(int(row["user_id"]), int(row["movie_id"]), float(row["rating"])))

        ranks = [2, 4, 8, 12, 20, 40, 100]
        errors = [0, 0, 0, 0, 0, 0, 0]
        err = 0
        min_error = float('Inf')
        best_rank = -1

        train, cv, test = data.randomSplit(weights=[6.0, 2.0, 2.0])

        validation_for_predict = cv.map(lambda row: (row.user, row.product))

        for rank in ranks:
            model = ALS.train(ratings=train, rank=rank, lambda_=0.1)

            predictions = model.predictAll(validation_for_predict).map(lambda row: ((row.user, row.product), row.rating))

            rates_and_preds = cv.map(
                lambda row: ((int(row.user), int(row.product)), float(row.rating))).join(
                predictions)
            error = math.sqrt(
                rates_and_preds.map(lambda r: (r[1][0] - r[1][1]) ** 2).mean())
            errors[err] = error
            err += 1
            print('For rank %s the RMSE is %s' % (rank, error))
            if error < min_error:
                min_error = error
                best_rank = rank

        print('The best model was trained with rank %s' % best_rank)
