import json
import pandas as pd

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

    
    
    #-- Quais são as condições e as quantidades de produtos vendidos em cada condição?

    #-- Quais são os produtos mais vendidos, em quantidade e em valor? 

    #-- Nas vendas da nossa loja online existe alguma condição de produtos que mais se destaca?

    #-- Quem são os melhores vendedores?

    #-- Qual é a o volume das vendas ao longo dos meses?

    #-- Quais são os valores de vendas por Estado?

    def list_result(self, cursor):
        try:
            column_names = [desc[0] for desc in cursor.description] if cursor.description else []
    
            results = cursor.fetchall()

            if results:

                df = pd.DataFrame(results, columns=column_names)
                records = df.to_dict(orient='records')
                for i, record in enumerate(records):
                    # Imprime cada dicionário como um objeto JSON separado
                    print(f"Registro {i+1}:\n{json.dumps(record, indent=4, ensure_ascii=False)}")

            else:
                print("A query SELECT não retornou resultados.")

        except Exception as e:
            print(f"Ocorreu um erro ao executar ou processar a query: {e}")
    