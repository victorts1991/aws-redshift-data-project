import sys
import os
from dotenv import load_dotenv

from redshift.redshift_client import RedshiftClient
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

    redshift_client = RedshiftClient(
        host=redshift_host, 
        port=redshift_port, 
        dbname=redshift_dbname, 
        user=redshift_user, 
        password=redshift_password
    )

    virtual_store_data_pipeline = VirtualStoreDataPipeline(redshift_client, bucket_name, aws_iam_role)
    flights_data_pipeline = FlightsDataPipeline(redshift_client, aws_iam_role)

    # Run Virtual Store Pipeline
    virtual_store_data_pipeline.run_pipeline()
    virtual_store_data_pipeline.run_analysis_queries()

    # Run Flights Pipeline
    flights_data_pipeline.run_pipeline()
    flights_data_pipeline.run_analysis_queries()

