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
export BUCKET_REGION=us-east-2
export AWS_IAM_ROLE=arn:aws:iam::101001870197:role/Redshift-Role

export AWS_ACCESS_KEY_ID= 
export AWS_SECRET_ACCESS_KEY=


Para gerar as chaves de acesso (Access Key ID e Secret Access Key) manualmente no console da AWS, siga este passo a passo detalhado:

Passo a Passo para Geração Manual de Chaves de Acesso AWS:

Acessar o Console de Gerenciamento da AWS:

Abra seu navegador e vá para o Console de Gerenciamento da AWS.
Faça login com suas credenciais (recomenda-se usar um usuário IAM, não a conta root, para maior segurança).
Navegar até o Serviço IAM:

Na barra de pesquisa na parte superior da tela, digite "IAM" e clique no serviço IAM (Identity and Access Management) que aparecerá.
Ir para "Usuários":

No painel de navegação à esquerda, clique em "Usuários" (Users).
Selecionar o Usuário IAM:

Clique no nome do usuário IAM para o qual você deseja gerar as chaves de acesso. (Se você ainda não tem um usuário IAM para uso programático, é altamente recomendado criar um primeiro, concedendo apenas as permissões mínimas necessárias, como acesso ao S3 e Redshift).
Acessar a Aba "Credenciais de segurança":

Na página de detalhes do usuário, clique na aba "Credenciais de segurança" (Security credentials).
Criar uma Nova Chave de Acesso:

Role a página para baixo até a seção "Chaves de acesso" (Access keys).
Clique no botão "Criar chave de acesso" (Create access key).
Escolher o Caso de Uso e Confirmar:

A AWS pedirá que você selecione um caso de uso para a nova chave de acesso. Para uso com scripts Python ou AWS CLI, você pode selecionar, por exemplo, "Ferramentas de linha de comando (CLI), SDKs ou APIs" (Command Line Interface (CLI), SDK, & API calls).
Marque a caixa de confirmação para reconhecer o aviso de melhores práticas.
Clique em "Criar chave de acesso".
Obter as Chaves (CRUCIAL!):

A AWS exibirá a Chave de Acesso (Access key ID) e a Chave de Acesso Secreta (Secret access key).
ATENÇÃO MÁXIMA: Esta é a ÚNICA VEZ que a Chave de Acesso Secreta será exibida no console.
Copie IMEDIATAMENTE ambas as chaves e armazene-as em um local seguro. Você pode clicar em "Download .csv file" para baixar um arquivo com elas, ou copiá-las diretamente.
Depois de fechar essa tela, a Chave de Acesso Secreta não poderá ser recuperada. Se você perdê-la, terá que excluí-la e criar uma nova.


permissao de AmazonS3FullAccess somente