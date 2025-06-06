import os
from dotenv import load_dotenv
from redshift.redshift_client import RedshiftClient
from redshift.redshift_ddl_dml_queries import RedshiftDdlDmlQueries
from redshift.redshift_analysis_queries import RedshiftAnalysisQueries

load_dotenv()

class DataPipeline:

    def __init__(self):
         
        self.redshift_host = os.getenv('REDSHIFT_HOST')
        self.redshift_port = int(os.getenv('REDSHIFT_PORT', 5439))
        self.redshift_dbname = os.getenv('REDSHIFT_DBNAME')
        self.redshift_user = os.getenv('REDSHIFT_USER') 
        self.redshift_password = os.getenv('REDSHIFT_PASSWORD')
        self.bucket_name = os.getenv('BUCKET_NAME')
        self.aws_iam_role = os.getenv('AWS_IAM_ROLE')

        self.redshift_client = RedshiftClient(
            host=self.redshift_host, 
            port=self.redshift_port, 
            dbname=self.redshift_dbname, 
            user=self.redshift_user, 
            password=self.redshift_password
        )

    def run_pipeline(self):
        print("Starting AWS Redshift Data Pipeline...")
        
        ddlDmlQueries = RedshiftDdlDmlQueries(
            self.redshift_client, 
            self.bucket_name, 
            self.aws_iam_role
        )

        ddlDmlQueries.create_vendedores_table_copy_csv()
        ddlDmlQueries.create_produtos_table_copy_csv()
        ddlDmlQueries.create_pedidos_table_copy_csv()
        ddlDmlQueries.create_itens_pedidos_table_copy_csv()

        print("Finish AWS Redshift Data Pipeline...")

    def run_analysis_queries(self):
        print("Starting AWS Redshift Analysis Queries...")

        analysisQueries = RedshiftAnalysisQueries(
            self.redshift_client, 
            self.bucket_name, 
            self.aws_iam_role
        )
        
        analysisQueries.analyze_conditions_and_quantities_of_products_offered_under_each_condition()
        analysisQueries.analyze_conditions_and_average_price_of_products_in_each_condition()
        analysisQueries.analyze_conditions_and_quantities_of_products_sold_in_each_condition()
        analysisQueries.analyze_best_selling_top_10_products_in_quantity_and_value()
        analysisQueries.analyze_who_are_the_best_sellers()
        analysisQueries.analyze_what_is_the_sales_volume_over_the_months_of_2020()
        analysisQueries.analyze_what_are_the_sales_figures_by_state()

        print("\nFinish AWS Redshift Analysis Queries...")

if __name__ == "__main__":
    pipeline = DataPipeline()
    # pipeline.run_pipeline()
    pipeline.run_analysis_queries()