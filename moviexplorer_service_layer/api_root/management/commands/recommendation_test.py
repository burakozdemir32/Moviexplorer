from django.core.management.base import BaseCommand

import os

from pyspark import SparkContext
from pyspark.sql import SQLContext


class Command(BaseCommand):
    help = 'Initialises spark based recommendation engine.'

    def handle(self, *args, **options):
        # Adds spark home and the required jar file to the path.
        os.environ["SPARK_HOME"] = "C:\spark"
        os.environ["SPARK_CLASSPATH"] = "C:\spark\postgresql.jar"

        # Database informations
        db_url = "jdbc:postgresql://localhost:5432/" \
                 "moviexplorer_service_layer?user=postgres&password=password"
        db_table = "api_root_movieratings"

        sc = SparkContext("local[*]", "<JOBNAME>")
        sqlContext = SQLContext(sc)

        df = sqlContext.read.format('jdbc').options(
            url=db_url,
            dbtable=db_table, driver="org.postgresql.Driver"
        ).load()
        a = df.count()
        print(a)
        sc.stop()

