import json
import pandas as pd
import decimal

class RedshiftAnalysisQueries:

    START_BOLD = '\033[1m'
    END_RESET = '\033[0m'

    def __init__(self, redshift_client, bucket_name, aws_iam_role):
        self.redshift_client = redshift_client
        self.bucket_name = bucket_name
        self.aws_iam_role = aws_iam_role

    def analyze_conditions_and_quantities_of_products_offered_under_each_condition(self):
        cursor = self.redshift_client.execute_query(
            f"""
            SELECT
                p.Condicao,
            COUNT(p.produto_id) AS quantidade_produtos
            FROM produtos p
            GROUP BY p.Condicao
            ORDER BY COUNT(p.produto_id) DESC;
            """,
            commit=False
        )
        print(f"\n{self.START_BOLD}Quais são as condições e as quantidades de produtos ofertados em cada condição?{self.END_RESET}")
        self.list_result(cursor)
    
    def analyze_conditions_and_average_price_of_products_in_each_condition(self):
        cursor = self.redshift_client.execute_query(
            f"""
            SELECT 
                p.Condicao, 
            AVG(p.preco) AS preco_medio
            FROM produtos p
            GROUP BY p.Condicao
            ORDER BY AVG(p.preco) DESC;
            """,
            commit=False
        )
        print(f"\n{self.START_BOLD}Quais são as condições e o preço médio dos produtos em cada condição?{self.END_RESET}")
        self.list_result(cursor)

    def analyze_conditions_and_quantities_of_products_sold_in_each_condition(self):
        cursor = self.redshift_client.execute_query(
            f"""
            SELECT
                p.Condicao,
                SUM(ip.quantidade) AS quantidade_total_vendida
            FROM itens_pedido ip
            INNER JOIN produtos p ON ip.produto_id = p.produto_id
            GROUP BY p.Condicao
            ORDER BY SUM(ip.quantidade) DESC;
            """,
            commit=False
        )
        print(f"\n{self.START_BOLD}Quais são as condições e as quantidades de produtos vendidos em cada condição?{self.END_RESET}")
        self.list_result(cursor)

    def analyze_best_selling_top_10_products_in_quantity_and_value(self):
        cursor = self.redshift_client.execute_query(
            f"""
            SELECT 
                pro.produto,
                SUM(ip.quantidade) AS quantidade_total,
                SUM(ip.valor_total) AS valor_total
            FROM itens_pedido ip
            INNER join produtos pro ON ip.produto_id = pro.produto_id
            GROUP BY pro.produto
            ORDER BY SUM(ip.valor_total) DESC
            LIMIT 10;
            """,
            commit=False
        )
        print(f"\n{self.START_BOLD}Quais são os 10 produtos mais vendidos, em quantidade e em valor?{self.END_RESET}")
        self.list_result(cursor)

    def analyze_who_are_the_best_sellers(self):
        cursor = self.redshift_client.execute_query(
            f"""
            SELECT 
                ven.nome_vendedor,
                SUM(ped.total) AS valor_total
            FROM vendedores ven
            INNER JOIN pedidos ped ON ped.vendedor_id = ven.vendedor_id
            GROUP BY ven.nome_vendedor
            ORDER BY  SUM(ped.total) DESC;
            """,
            commit=False
        )
        print(f"\n{self.START_BOLD}Quem são os melhores vendedores?{self.END_RESET}")
        self.list_result(cursor)

    def analyze_what_is_the_sales_volume_over_the_months_of_2020(self):
        cursor = self.redshift_client.execute_query(
            f"""
            SELECT 
                EXTRACT(YEAR FROM data_compra) AS ano, 
                EXTRACT(MONTH FROM data_compra) AS mes, 
                SUM(total) AS valor_total_vendas
            FROM pedidos
            WHERE 
                ano = '2020'
            GROUP BY 
                ano,
                mes
            ORDER BY 
                ano DESC, 
                mes DESC;
            """,
            commit=False
        )
        print(f"\n{self.START_BOLD}Qual é a o volume das vendas ao longo dos meses de 2020?{self.END_RESET}")
        self.list_result(cursor)

    def analyze_what_are_the_sales_figures_by_state(self):
        cursor = self.redshift_client.execute_query(
            f"""
            SELECT 
                estado,
                SUM(valor_total) AS valor_total
            FROM itens_pedido
            GROUP BY estado
            ORDER BY valor_total DESC;
            """,
            commit=False
        )
        print(f"\n{self.START_BOLD}Quais são os valores de vendas por Estado?{self.END_RESET}")
        self.list_result(cursor)

    def list_result(self, cursor):
        try:
            column_names = [desc[0] for desc in cursor.description] if cursor.description else []
    
            results = cursor.fetchall()

            if results:

                df = pd.DataFrame(results, columns=column_names)

                for col in df.columns:
                    # Se a coluna é do tipo 'object' no Pandas, pode conter strings ou outros tipos mistos.
                    # Vamos verificar se ela *realmente contém* objetos Decimal antes de converter para float.
                    if df[col].dtype == 'object':
                        # Verifica se a coluna não está vazia e se há algum Decimal nela
                        if not df[col].isnull().all() and any(isinstance(val, decimal.Decimal) for val in df[col].dropna()):
                            df[col] = df[col].astype(float)
                    # Para todas as colunas que são ou se tornaram numéricas, garanta que sejam float para JSON
                    elif pd.api.types.is_numeric_dtype(df[col]):
                        df[col] = df[col].astype(float)

                records = df.to_dict(orient='records')
                for i, record in enumerate(records):
                    # Imprime cada dicionário como um objeto JSON separado
                    print(f"Registro {i+1}:\n{json.dumps(record, indent=4, ensure_ascii=False)}")

            else:
                print("A query SELECT não retornou resultados.")

        except Exception as e:
            print(f"Ocorreu um erro ao executar ou processar a query: {e}")
    