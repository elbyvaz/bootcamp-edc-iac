import boto3 # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
import pandas as pd

# create a client to interact with AWS S3
s3_client = boto3.client('s3')

#                        bucket                 , s3 file path (uri)    , file path after downloaded
s3_client.download_file('datalake-elby-igti-edc', 'data/funcionario.csv', 'funcionario_downloaded.csv')

#df = pd.read_csv('data/funcionario.csv', sep=';')
df = pd.read_csv('funcionario_downloaded.csv', sep=';')
print(df)

# uploading a file
#                        file to upload             , bucket                  , destination path and new name
# s3_client.upload_file('funcionario_downloaded.csv', 'datalake-elby-igti-edc', 'data/funcionario.csv')