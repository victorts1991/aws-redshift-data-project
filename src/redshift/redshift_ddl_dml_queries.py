class RedshiftDdlDmlQueries:
    
    def __init__(self, redshift_client, bucket_name, aws_iam_role):
        self.redshift_client = redshift_client
        self.bucket_name = bucket_name
        self.aws_iam_role = aws_iam_role

    def create_vendedores_table_copy_csv(self):
        self.redshift_client.execute_query(
            f"""
            CREATE TABLE vendedores (
                vendedor_id INTEGER,
                nome_vendedor VARCHAR(255)
            );
            """
        )
        self.redshift_client.execute_query(
            f"""
            COPY vendedores FROM 's3://{self.bucket_name}/vendedores.csv' 
            CREDENTIALS 'aws_iam_role={self.aws_iam_role}'
            DELIMITER ','
            IGNOREHEADER 1;
            """
        )
        print("Tabela de vendedores criada.")
        
    def create_produtos_table_copy_csv(self):
        self.redshift_client.execute_query(
            f"""
            CREATE TABLE produtos (
                produto_id INTEGER,
                produto VARCHAR(255),
                preco INTEGER,
                marca VARCHAR(255),
                sku VARCHAR(50),
                Condicao VARCHAR(50)
            );
            """
        )
        self.redshift_client.execute_query(
            f"""
            COPY produtos FROM 's3://{self.bucket_name}/produtos.csv' 
            CREDENTIALS 'aws_iam_role={self.aws_iam_role}'
            DELIMITER ';'
            IGNOREHEADER 1;
            """
        )
        print("Tabela de produtos criada.")
    
    def create_pedidos_table_copy_csv(self):
        self.redshift_client.execute_query(
            f"""
            CREATE TABLE pedidos (
                pedido_id INTEGER,
                produto_id INTEGER,
                vendedor_id INTEGER,
                data_compra DATE,
                total NUMERIC(12,2)
            );
            """
        )
        self.redshift_client.execute_query(
            f"""
            COPY pedidos FROM 's3://{self.bucket_name}/pedidos.csv' 
            CREDENTIALS 'aws_iam_role={self.aws_iam_role}'
            DELIMITER ','
            IGNOREHEADER 1;
            """
        )
        print("Tabela de pedidos criada.")

    def create_itens_pedidos_table_copy_csv(self):
        self.redshift_client.execute_query(
            f"""
            CREATE TABLE itens_pedido (
                id_nf INTEGER,
                produto_id INTEGER,
                pedido_id INTEGER,
                quantidade INTEGER,
                valor_unitario NUMERIC(10,2),
                valor_total NUMERIC(10,2),
                Estado VARCHAR(5),
                frete NUMERIC(10,2)
            );
            """
        )
        self.redshift_client.execute_query(
            f"""
            COPY itens_pedido FROM 's3://{self.bucket_name}/itens_pedidos.csv' 
            CREDENTIALS 'aws_iam_role={self.aws_iam_role}'
            DELIMITER ','
            IGNOREHEADER 1;
            """
        )
        print("Tabela de itens_pedido criada.")
    