from django.core.management.base import BaseCommand

import os

from pyspark import SparkContext
from pyspark.sql import SQLContext


class Command(BaseCommand):
    help = 'Initialises spark based recommendation engine.'

    def handle(self, *args, **options):
        os.environ["SPARK_HOME"] = "C:\spark"
        os.environ["SPARK_CLASSPATH"] = "C:\spark\postgresql.jar"

        sc = SparkContext("local[*]", "<JOBNAME>")
        sqlContext = SQLContext(sc)

        df = sqlContext.read.format('jdbc').options(
            url="jdbc:postgresql://localhost:5432/moviexplorer_service_layer?user=postgres&password=password",
            dbtable="api_root_movieratings", driver="org.postgresql.Driver"
        ).load()
        a = df.count()
        print(a)
        sc.stop()

