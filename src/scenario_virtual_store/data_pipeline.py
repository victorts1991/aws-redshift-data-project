import os
from scenario_virtual_store.redshift.redshift_ddl_dml_queries import RedshiftDdlDmlQueries
from scenario_virtual_store.redshift.redshift_analysis_queries import RedshiftAnalysisQueries

class VirtualStoreDataPipeline:

    def __init__(self, redshift_client, s3_upload, bucket_name, aws_iam_role, aws_access_key_id, aws_secret_access_key):

        self.redshift_client = redshift_client
        self.bucket_name = bucket_name
        self.aws_iam_role = aws_iam_role
        self.s3_upload = s3_upload
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

    def run_pipeline(self):
        print("Starting AWS Redshift Virtual Store Data Pipeline...")

        file_path = os.path.abspath(os.path.join('data/vendedores.csv', '.'))
        self.s3_upload.handle_s3(
            file_path,
            self.aws_access_key_id,
            self.aws_secret_access_key,
            'upload',
            'vendedores.csv'
        )
        file_path = os.path.abspath(os.path.join('data/produtos.csv', '.'))
        self.s3_upload.handle_s3(
            file_path,
            self.aws_access_key_id,
            self.aws_secret_access_key,
            'upload',
            'produtos.csv'
        )
        file_path = os.path.abspath(os.path.join('data/pedidos.csv', '.'))
        self.s3_upload.handle_s3(
            file_path,
            self.aws_access_key_id,
            self.aws_secret_access_key,
            'upload',
            'pedidos.csv'
        )
        file_path = os.path.abspath(os.path.join('data/itens_pedidos.csv', '.'))
        self.s3_upload.handle_s3(
            file_path,
            self.aws_access_key_id,
            self.aws_secret_access_key,
            'upload',
            'itens_pedidos.csv'
        )
        
        ddlDmlQueries = RedshiftDdlDmlQueries(
            self.redshift_client, 
            self.bucket_name, 
            self.aws_iam_role
        )

        ddlDmlQueries.create_vendedores_table_copy_csv()
        ddlDmlQueries.create_produtos_table_copy_csv()
        ddlDmlQueries.create_pedidos_table_copy_csv()
        ddlDmlQueries.create_itens_pedidos_table_copy_csv()

        print("Finish AWS Redshift Virtual Store Data Pipeline...")

    def run_analysis_queries(self):
        print("Starting AWS Redshift Virtual Store Analysis Queries...")

        analysisQueries = RedshiftAnalysisQueries(self.redshift_client)
        
        analysisQueries.analyze_conditions_and_quantities_of_products_offered_under_each_condition()
        analysisQueries.analyze_conditions_and_average_price_of_products_in_each_condition()
        analysisQueries.analyze_conditions_and_quantities_of_products_sold_in_each_condition()
        analysisQueries.analyze_best_selling_top_10_products_in_quantity_and_value()
        analysisQueries.analyze_who_are_the_best_sellers()
        analysisQueries.analyze_what_is_the_sales_volume_over_the_months_of_2020()
        analysisQueries.analyze_what_are_the_sales_figures_by_state()

        print("\nFinish AWS Redshift Virtual Store Analysis Queries...")
