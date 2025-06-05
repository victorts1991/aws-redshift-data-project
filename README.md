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
