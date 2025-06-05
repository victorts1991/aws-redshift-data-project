# redshift-data-project

A project to provision Amazon Redshift with Terraform, load data from CSVs, and perform analytics with SQL. Includes Python scripts for orchestration and using GitHub Actions for CI/CD.

Após executar o git clone execute os comandos abaixo na raiz do projeto:

```
python3 -m venv venv

source venv/bin/activate  # Unix/macOS
# ou
venv\Scripts\activate  # Windows

pip install -r requirements.txt

python3 ./python_scripts/run_queries.py
```


TO DO:

1. Executar queries analíticas
2. Acrescentar a subida dos arquivos no S3;
3. Criar Terraform para interagir com o Redshift e S3;
4. Criar Github Actions;
5. Criar documentação;

export REDSHIFT_HOST=redshift-cluster-2.cv4cutjvp7fa.us-east-2.redshift.amazonaws.com 
export REDSHIFT_PORT=5439
export REDSHIFT_DBNAME=dev
export REDSHIFT_USER=fiap
export REDSHIFT_PASSWORD=Fiap2025
