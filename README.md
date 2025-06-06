# redshift-data-project

End-to-end AWS data pipeline: Provides infrastructure with Terraform, performs data ETL from Amazon S3 to Amazon Redshift via Python, and performs SQL analysis, displaying Pandas-formatted results directly in GitHub Actions.

# Deploy local
Após executar o git clone execute os comandos abaixo na raiz do projeto:

```
python3 -m venv venv

source venv/bin/activate  # Unix/macOS
# ou
venv\Scripts\activate  # Windows

pip install -r requirements.txt

python3 ./src/main_pipeline.py
```


TO DO:

1. Acrescentar a subida dos arquivos no S3;
2. Criar Terraform para interagir com o Redshift e S3;
3. Criar Github Actions;
4. Criar documentação (explicar que o create table dos voos pode demorar um 2 minutos ou mais pois tem 93 milhoes de registros);

export REDSHIFT_HOST=redshift-cluster-2.cv4cutjvp7fa.us-east-2.redshift.amazonaws.com 
export REDSHIFT_PORT=5439
export REDSHIFT_DBNAME=dev
export REDSHIFT_USER=fiap
export REDSHIFT_PASSWORD=Fiap2025
export BUCKET_NAME=bucket-fiap-redshift-victor
export AWS_IAM_ROLE=arn:aws:iam::101001870197:role/Redshift-Role
