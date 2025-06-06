import json
import pandas as pd
import decimal

class RedshiftAnalysisQueries:

    START_BOLD = '\033[1m'
    END_RESET = '\033[0m'

    def __init__(self, redshift_client, ):
        self.redshift_client = redshift_client

    def analyze_count_how_many_flight_records(self):
        cursor = self.redshift_client.execute_query(
            f"""
            SELECT
                COUNT(*)
            FROM flights;
            """,
            commit=False
        )
        print(f"\n{self.START_BOLD}Contagem de quantos registros de voos.{self.END_RESET}")
        self.list_result(cursor)
    
    def analyze_which_top_10_aircraft_have_the_most_flights(self):
        cursor = self.redshift_client.execute_query(
            f"""
            SELECT 
                air.aircraft,
                SUM(f.departures) AS trips
            FROM aircraft air
            INNER JOIN flights f ON f.aircraft_code = air.aircraft_code
            GROUP BY air.aircraft
            ORDER BY trips DESC
            LIMIT 10;
            """,
            commit=False
        )
        print(f"\n{self.START_BOLD}Quais são as top 10 aeronaves com mais voos?{self.END_RESET}")
        self.list_result(cursor)

    def analyze_which_top_10_aircraft_have_the_most_flights(self):
        cursor = self.redshift_client.execute_query(
            f"""
            SELECT 
                air.aircraft,
                SUM(f.departures) AS trips
            FROM aircraft air
            INNER JOIN flights f ON f.aircraft_code = air.aircraft_code
            GROUP BY air.aircraft
            ORDER BY trips DESC
            LIMIT 10;
            """,
            commit=False
        )
        print(f"\n{self.START_BOLD}Quais são as top 10 aeronaves com mais voos?{self.END_RESET}")
        self.list_result(cursor)
    
    def analyze_what_are_the_top_10_most_popular_flights_from_las_vegas(self):
        cursor = self.redshift_client.execute_query(
            f"""
            SELECT
                airport AS airport_origin,
                to_char(SUM(passengers), '999,999,999') as passengers
            FROM vegas_flights
            GROUP BY airport
            ORDER BY SUM(passengers) DESC
            LIMIT 10;
            """,
            commit=False
        )
        print(f"\n{self.START_BOLD}Quais são os top 10 voos mais populares com destino em Las Vegas?{self.END_RESET}")
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
    