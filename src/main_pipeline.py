import sys
import os
from dotenv import load_dotenv

from redshift.redshift_client import RedshiftClient
from s3.s3_upload import S3Upload
from scenario_virtual_store.data_pipeline import VirtualStoreDataPipeline
from scenario_flights.data_pipeline import FlightsDataPipeline

load_dotenv()

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

if __name__ == "__main__":

    redshift_host = os.getenv('REDSHIFT_HOST')
    redshift_port = int(os.getenv('REDSHIFT_PORT', 5439))
    redshift_dbname = os.getenv('REDSHIFT_DBNAME')
    redshift_user = os.getenv('REDSHIFT_USER') 
    redshift_password = os.getenv('REDSHIFT_PASSWORD')
    bucket_name = os.getenv('BUCKET_NAME')
    aws_iam_role = os.getenv('AWS_IAM_ROLE')
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    redshift_client = RedshiftClient(
        host=redshift_host, 
        port=redshift_port, 
        dbname=redshift_dbname, 
        user=redshift_user, 
        password=redshift_password
    )

    s3_upload = S3Upload(bucket_name)

    virtual_store_data_pipeline = VirtualStoreDataPipeline(redshift_client, s3_upload, bucket_name, aws_iam_role, aws_access_key_id, aws_secret_access_key)
    flights_data_pipeline = FlightsDataPipeline(redshift_client, aws_iam_role)

    # Run Virtual Store Pipeline
    virtual_store_data_pipeline.run_pipeline()
    virtual_store_data_pipeline.run_analysis_queries()

    # Run Flights Pipeline
    flights_data_pipeline.run_pipeline()
    flights_data_pipeline.run_analysis_queries()

