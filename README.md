# redshift-data-project

End-to-end AWS data pipeline: Data ETL from Amazon S3 to Amazon Redshift via Python, and performs SQL analysis, displaying Pandas-formatted results. Includes basic automation via GitHub Actions.

### Passos para Configurar o Ambiente AWS

## Criação da Role

1. Efetue o login na plataforma da AWS e acesse o menu IAM;
2. Acesse o menu Roles no menu lateral;
3. Clique no botão "Create Role";
4. No combo de Service or use case, selecione a opção "Redshift";
5. Em Use case mantenha a opção "Redshift - Customizable" marcada e clique no botão "Next";
6. Adicione as seguintes permissões: (AmazonS3FullAccess, AmazonEC2FullAccess, AmazonRedshiftFullAccess, AmazonDMSRedshiftS3Role, AmazonRedshiftDataFullAccess e AmazonRedshiftQueryEditor) e clique no botão "Next";
7. Atribua o nome e descrição a sua escolha, por exemplo no nome "Redshift-Role" e na descrição "Role created for Redshift" e após isso no final da página, clique no botão "Create role";
8. Acesse os detalhes da role criada e copie o valor do campo ARN;

## Criação da VPC

1. Acesse o menu VPC;
2. Acesse o menu "Your VPCs" no menu lateral;
3. Clique no botão "Create VPC";
4. Em "Resources to create", selecione a opção "VPC and more";
5. Em "Name tag auto-generation" digite um nome a sua escolha como por exemplo "vpc-redshift";
6. No final da página clique em "Create VPC";

## Criação Security Group

1. Volte ao menu "Your VPCs" e clique no item de menu "Security Groups" do menu lateral;
2. Clique no botão "Create security group";
3. Em "Security group name" atribua um nome e uma descrição a sua escolha como por exemplo "security-group-redshift";
4. Em "VPC" selecione a mesma que você criou;
5. Em "Inbound rules" adicione uma regra clicando em "Add rule";
6. Em "Port range" adicione o valor "5439" e em "CIDR Blocks" coloque o valor de "0.0.0.0/0";
7. Clique em "Create security group";

## Criação do Cluster do Amazon Redshift

1. Acesse o menu "Amazon Redshift"''
2. Acesse o item de menu "Provisioned clusters dashboard" através do menu lateral;
3. Clique no botão "Create cluster";
4. Em "Cluster identifier" defina um nome a sua escolha como por exemplo "redshift-cluster-meu-teste";
  4.1. Tome cuidado para atribuir um nome diferente de anteriores caso você já tenha criado antes algum cluster, pode acontecer conflitos no momento da conexão por conta de algum cache interno da AWS;
5. Em "Choose the size of the cluster" mantenha a opção "I'll choose";
6. Em "Node type", para o nosso teste selecione a opção "ra3.large", abaixo segue uma breve descrição sobre a diferença entre o ra3 e o dc2:
```
- RA3 o armazenamento acontece fora do redshift, a vantagem é que o mesmo pode crescer o armazenamento sem limites, pois é usado o S3, em contra partida é um pouco mais lento;

- DC2 tem mais performance, é executado dentro do storage SSD no próprio cluster do redshift, porém para crescer o armazenamento é necessário crescer o número de máquinas, e dependendo do escopo isso pode sair mais caro;

Observação: Se correr o risco dos dados aumentarem muito rápido é melhor o RA3, se for mais controlado, é melhor a DC2 que vai te dar mais performance;
```
7. Em "Database configurations", atribua o nome de um usuário em "Admin user name";
8. Em "Admin password" selecione a opção "Manually add the admin password" e digite uma senha no campo que aparecer;
9. Em "Cluster permissions", clique no botão "Associate IAM roles";
10. Selecione a Role que foi criada anteriormente e clique em "Associate IAM roles";
11. Em "Additional configurations" desmarque a opção "Use defaults";
12. Em "Network and security", clique no botão "Create new subnet group";
13. Na aba que se abriu, no campo Name e Description, adicione um valor a sua escolha como por exemplo "subnet-redshift";
14. Em "VPC", selecione o VPC criado anteriormente;
15. Clique no botão "Add all the subnets for this VPC";
16. Clique no botão "Create cluster subnet group";
17. Retorne na aba anterior e clique no botão onde tem uma flexa rotatória para atualizar;
18. Mais acima no mesmo bloco de informações selecione o nome da VPC criada anteriormente em "Virtual private cloud (VPC)";
19. Em "VPC security groups" adicione o mesmo criado anteriormente e demarque o default;
20. Habilite a opção "Turn on Publicly accessible";
21. Clique em "Create cluster" no final da página;
22. Aguarde alguns minutos até que a AWS tenha concluído a criação do cluster do Redshift;

## Criação do bucket do S3

1. Acesse o menu S3;
2. Clique no botão "Create bucket";
3. Em "Bucket name" atribua um nome a sua escolha como por exemplo "bucket-redshift";
4. Clique no botão "Create bucket" no final da tela;

## Criar usuário para upload de arquivos no S3

1. Acesse o menu "IAM";
2. Clique em "Users" no menu lateral;
3. Clique em "Create user";
4. Defina um nome em "User name" a sua escolha como por exemplo "s3-user" e clique no botão "Next";
5. Marque a opção "Attach policies directly" na tela que se abriu;
6. Selecione a opção "AmazonS3FullAccess" em "Permissions policies" e clique em "Next";
7. Clique em "Create user";
8. Acesse os detalhes do seu usuário e clique na aba "Security credentials";
9. No bloco de informações "Access keys" clique no botão "Create access key";
10. Marque a opção "Command Line Interface (CLI)" e clique em "Next";
11. Em "Description tag value" atribua um nome a sua escolha como por exemplo "access-key-for-upload-s3" e clique em "Create access key";
12. Copie e deixe salvo em algum lugar por enquanto o valor dos campos "Access key" e "Secret access key";
13. Após isso clique em "Done";

### Executar o pipeline de dados

## Informações de varíaveis de ambiente

1. Acesse os detalhes do cluster Redshift criado e copie o valor do campo Endpoint;
2. O valor das varíveis de ambiente deverá conforme o dicionário abaixo:
```
REDSHIFT_HOST=<Valor do campo Endpoint, remova o valor da porta e do banco do valor, o mesmo deve ficar semelhante a isso: redshift-cluster-1.cv4cutjvp7fa.us-east-2.redshift.amazonaws.com>
REDSHIFT_PORT=5439
REDSHIFT_DBNAME=dev
REDSHIFT_USER=<Nome do Usuário atribuido no campo Admin user name na criação do Redshift>
REDSHIFT_PASSWORD=<Senha do Usuário atribuido no campo Admin password na criação do Redshift>
BUCKET_NAME=<Nome do bucket criado>
AWS_ACCESS_KEY_ID=<Access key copiada na criação do usuário>
AWS_SECRET_ACCESS_KEY=<Secret access key copiada na criação do usuário>
AWS_IAM_ROLE=<Valor copiado de ARN nos detalhes da Role criada>
```

## Local

1. Crie as varíaveis de ambiente com as informações detalhadas acima;
2. Execute os comandos abaixo:
```
python3 -m venv venv

source venv/bin/activate  # Unix/macOS
# ou
venv\Scripts\activate  # Windows

pip install -r requirements.txt

python3 ./src/main_pipeline.py
```

## Github Actions

1. Faça um fork do projeto;
2. Acesse o menu Settings do seu repositório;
3. Acesse o menu Secrets and variables->Actions;
4. Cadastre as Repository secrets com as informações detalhadas acima e mais essa:
```
AWS_REGION=<região onde seu ambiente foi montado, por exemplo: us-east-2>
```
5. Qualquer commit feito na branch main fará com que o pipeline do Github Actions seja executado;

