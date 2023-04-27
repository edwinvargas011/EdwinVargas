import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1682593173435 = glueContext.create_dynamic_frame.from_catalog(
    database="database_news",
    table_name="headlines",
    transformation_ctx="AWSGlueDataCatalog_node1682593173435",
)

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1682593153205 = glueContext.write_dynamic_frame.from_catalog(
    frame=AWSGlueDataCatalog_node1682593173435,
    database="database_news",
    table_name="database_test_headlines_",
    transformation_ctx="AWSGlueDataCatalog_node1682593153205",
)

job.commit()
