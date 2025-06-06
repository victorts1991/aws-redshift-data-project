import boto3
from botocore.exceptions import NoCredentialsError

class S3Upload:
    """
    Gerencia o upload de arquivos para um bucket Amazon S3.
    """
    def __init__(self, bucket_name):
        """
        Inicializa o S3Upload.

        Args:
            bucket_name (str): O nome do bucket S3 de destino.
        """
        self.bucket_name = bucket_name

    def handle_s3(self, file_name, access_key, secret_key, action, object_name=None, prefix=None):
        """
        file_name: Caminho completo do arquivo a ser enviado ou deletado'
        access_key: AWS Access Key ID.
        secret_key: AWS Secret Access Key.
        action: 'upload' para enviar o arquivo, 'delete' para deletar o arquivo do bucket, 'list' para ver os arquivos do bucket
        object_name: Nome do objeto no bucket S3. Se None, file_name.
        prefix: se voce deseja que o arquivo tenha prefixo no S3, usar.
        True se a ação foi realizada com sucesso, False caso contrário.
        """
        session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        s3_client = session.client('s3')

        try:
            if action == 'upload':
                if object_name is None:
                    object_name = file_name.split('/')[-1]
                if prefix:
                    object_name = f"{prefix}/{object_name}"
                s3_client.upload_file(file_name, self.bucket_name, object_name)
            elif action == 'delete':
                if object_name is None or prefix:
                    raise ValueError("Para deletar um objeto, o 'object_name' deve ser especificado e 'prefix' deve ser None ou vazio.")
                s3_client.delete_object(Bucket=self.bucket_name, Key=object_name)
            elif action == 'list':
                paginator = s3_client.get_paginator('list_objects_v2')
                for page in paginator.paginate(Bucket=self.bucket_name, Prefix=prefix):
                    for obj in page.get('Contents', []):
                        print(obj['Key'])
            else:
                print(f"Ação '{action}' não reconhecida.")
                return False
            print(f"Arquivo {object_name} processado com a ação {action} concluído com sucesso.")
        except NoCredentialsError:
            print("As credenciais não estão disponíveis")
            return False
        except ValueError as ve:
            print(ve)
            return False
        except Exception as e:
            print(f"Erro ao realizar ação '{action}' no arquivo: {e}")
            return False

        return True

    