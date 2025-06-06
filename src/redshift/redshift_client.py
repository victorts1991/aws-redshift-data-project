import redshift_connector 
import os

class RedshiftClient:
    """
    Gerencia a conexão e a execução de queries SQL no Amazon Redshift.
    """
    def __init__(self, host, port, dbname, user, password):
        """
        Inicializa o cliente Redshift com os parâmetros de conexão.

        Args:
            host (str): Endpoint do cluster Redshift.
            port (int): Porta de conexão (geralmente 5439).
            dbname (str): Nome do banco de dados no Redshift.
            user (str): Usuário do banco de dados.
            password (str): Senha do usuário do banco de dados.
        """
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.conn = None

        if not self.user or not self.password:
            raise ValueError("User and password must be provided for traditional authentication.")

        print(f"RedshiftClient inicializado para '{self.user}@{self.host}:{self.port}/{self.dbname}'.")

    def connect(self):
        """
        Estabelece a conexão com o Redshift.
        """
        if self.conn is None or self.conn.closed:
            try:
                self.conn = redshift_connector.connect(
                    host=self.host,
                    port=self.port,
                    database=self.dbname,
                    user=self.user,
                    password=self.password
                )
                print("Conexão com Redshift (User/Pass) estabelecida com sucesso.")
                
            except Exception as e:
                print(f"Erro ao conectar ao Redshift: {e}")
                raise 

    def close(self):
        """
        Fecha a conexão com o Redshift se estiver aberta.
        """
        if self.conn: 
            self.conn.close()
            print("Conexão com Redshift encerrada.")
    
    def execute_query(self, query, params=None, commit=True):
        """
        Executa uma única query SQL no Redshift.
        """
        if not self.conn:
            self.connect() 

        try:
            with self.conn.cursor() as cur:
                if params:
                    cur.execute(query, params)
                else:
                    cur.execute(query)

                if commit:
                    self.conn.commit()
                
                return cur
        except Exception as e:
            if self.conn:
                self.conn.rollback() 
            print(f"Erro ao executar query: {e}")
            raise 
