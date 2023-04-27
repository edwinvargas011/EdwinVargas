import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
## @type: DataSource
## @args: [database = "database_news", table_name = "headlines", transformation_ctx = "datasource0"]
## @return: datasource0
## @inputs: []
datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "database_news", table_name = "headlines", transformation_ctx = "datasource0")
## @type: ApplyMapping
## @args: [mapping = [("col0", "long", "col0", "long"), ("col1", "string", "col1", "string"), ("col2", "string", "col2", "string"), ("col3", "string", "col3", "string"), ("col4", "string", "col4", "string"), ("partition_0", "string", "partition_0", "string"), ("periodico", "string", "periodico", "string"), ("year", "string", "year", "string"), ("month", "string", "month", "string"), ("day", "string", "day", "string")], transformation_ctx = "applymapping1"]
## @return: applymapping1
## @inputs: [frame = datasource0]
applymapping1 = ApplyMapping.apply(frame = datasource0, mappings = [("col0", "long", "col0", "long"), ("col1", "string", "col1", "string"), ("col2", "string", "col2", "string"), ("col3", "string", "col3", "string"), ("col4", "string", "col4", "string"), ("partition_0", "string", "partition_0", "string"), ("periodico", "string", "periodico", "string"), ("year", "string", "year", "string"), ("month", "string", "month", "string"), ("day", "string", "day", "string")], transformation_ctx = "applymapping1")
## @type: ResolveChoice
## @args: [choice = "make_cols", transformation_ctx = "resolvechoice2"]
## @return: resolvechoice2
## @inputs: [frame = applymapping1]
resolvechoice2 = ResolveChoice.apply(frame = applymapping1, choice = "make_cols", transformation_ctx = "resolvechoice2")
## @type: DropNullFields
## @args: [transformation_ctx = "dropnullfields3"]
## @return: dropnullfields3
## @inputs: [frame = resolvechoice2]
dropnullfields3 = DropNullFields.apply(frame = resolvechoice2, transformation_ctx = "dropnullfields3")
## @type: DataSink
## @args: [catalog_connection = "Conexion_RDS_", connection_options = {"dbtable": "headlines", "database": "database_test"}, transformation_ctx = "datasink4"]
## @return: datasink4
## @inputs: [frame = dropnullfields3]
datasink4 = glueContext.write_dynamic_frame.from_jdbc_conf(frame = dropnullfields3, catalog_connection = "Conexion_RDS_", connection_options = {"dbtable": "headlines", "database": "database_test"}, transformation_ctx = "datasink4")
job.commit()