import os
from dotenv import load_dotenv
from redshift_client import RedshiftClient
from redshift_ddl_dml_queries import RedshiftDdlDmlQueries

load_dotenv()

class DataPipeline:

    def __init__(self):
         
        self.redshift_host = os.getenv('REDSHIFT_HOST')
        self.redshift_port = int(os.getenv('REDSHIFT_PORT', 5439))
        self.redshift_dbname = os.getenv('REDSHIFT_DBNAME')
        self.redshift_user = os.getenv('REDSHIFT_USER') 
        self.redshift_password = os.getenv('REDSHIFT_PASSWORD')

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
            'bucket-fiap-redshift-victor', 
            'arn:aws:iam::101001870197:role/Redshift-Role'
        )

        ddlDmlQueries.create_vendedores_table_copy_csv()
        ddlDmlQueries.create_produtos_table_copy_csv()
        ddlDmlQueries.create_pedidos_table_copy_csv()
        ddlDmlQueries.create_itens_pedidos_table_copy_csv()

        print("Finish AWS Redshift Data Pipeline...")

if __name__ == "__main__":
    pipeline = DataPipeline()
    pipeline.run_pipeline()