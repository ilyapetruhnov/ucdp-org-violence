#!/usr/bin/env python
# coding: utf-8

import argparse

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, sum


parser = argparse.ArgumentParser()

parser.add_argument('--input_georeferenced', required=True)
parser.add_argument('--input_candidate', required=True)
parser.add_argument('--gcs_bucket', required=True)
parser.add_argument('--output', required=True)
parser.add_argument('--output_table', required=True)

args = parser.parse_args()

input_georeferenced = args.input_georeferenced
input_candidate = args.input_candidate
gcs_bucket = args.gcs_bucket
output = args.output
output_table = args.output_table


spark = SparkSession.builder.appName('app').getOrCreate()
spark.conf.set('temporaryGcsBucket', gcs_bucket)


df_georeferenced = spark.read.parquet(input_georeferenced)
df_candidate = spark.read.parquet(input_candidate)

df_candidate_cols = [colmn.lower() for colmn in df_candidate.columns]
for col_dts in df_georeferenced.dtypes:
    col_name, dtype = col_dts
    if col_name.lower() in df_candidate_cols:
        df_candidate = df_candidate.withColumn(col_name, col(col_name).cast(dtype))
    else:
        df_candidate = df_candidate.withColumn(col_name,lit(None).cast(dtype))

df_candidate = df_candidate.select(df_georeferenced.columns)

df = df_georeferenced.unionByName(df_candidate)


cols = [
    'year','active_year','type_of_violence','conflict_name', 'side_a',
    'side_b', 'number_of_sources','source_original',
    'where_coordinates','latitude', 'longitude','country', 'region',
    'date_start', 'date_end', 'deaths_a','deaths_b','deaths_civilians', 'deaths_unknown'
]
df = df.select(cols)


conflict_type_mapping = {'1': 'state-based', 
                         '2': 'non-state', 
                         '3':'one-sided'}

df = (df.withColumn('violence',col('type_of_violence').cast('string'))
                    .replace(to_replace = conflict_type_mapping, subset=['violence'])
           )


df_result = (df.groupBy('country','year','conflict_name','violence')
            .agg(
                sum('deaths_unknown').alias('deaths_unknown'),
                sum('deaths_civilians').alias('deaths_civilians'),
                sum('deaths_a').alias('deaths_a'),
                sum('deaths_b').alias('deaths_b')
               )
            .orderBy(col('year').desc())
            )

    
df_result.coalesce(1).write.parquet(output, mode='overwrite')

(df_result.write
        .format('bigquery')
        .option('table', output_table)
        .save()
)

