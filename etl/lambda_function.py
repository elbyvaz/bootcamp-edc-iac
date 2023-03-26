import boto3

# a funcao handler eh obrigatoria
def handler(event, context):
    """
    Lambda function that starts a job flow in EMR.
    """
    client = boto3.client('emr', region_name='us-east-2')

    cluster_id = client.run_job_flow( #cria um cluster emr
        Name='EMR-Elby-IGTI-delta',
        ServiceRole='EMR_DefaultRole',
        JobFlowRole='EMR_EC2_DefaultRole',
        VisibleToAllUsers=True,
        LogUri='s3://datalake-elby-igti-edc-tf/emr-logs',
        ReleaseLabel='emr-6.3.0',
        Instances={
            'InstanceGroups': [
                {
                    'Name': 'Master nodes',
                    'Market': 'SPOT',
                    'InstanceRole': 'MASTER'
                    'InstanceType': 'm5.xlarge',
                    'InstanceCount': 1,
                },
                {
                    'Name': 'Worker nodes',
                    'Market': 'SPOT',
                    'InstanceRole': 'CORE'
                    'InstanceType': 'm5.xlarge',
                    'InstanceCount': 1,
                }
            ],
            'Ec2KeyName': 'elby-igti-teste', # criar manualmente no EC2
            'KeepJobFlowAliveWhenNoSteps': True,
            'TerminationProtected': False,


            # para a subnet abaixo, ir no EMR na AWS / clusters / clica no cluster / verifica a subnet id q o cluster foi criado / copia e cola
            'Ec2SubnetId': 'subnet-065783d773bff6d7f'


        },

        Applications=[
            {'Name': 'Spark'},
            {'Name': 'Hive'},
            {'Name': 'Pig'},
            {'Name': 'Hue'},
            {'Name': 'JupyterHub'},
            {'Name': 'JupyterEnterpriseGateway'},
            {'Name': 'Livy'},
        ],

        Configurations=[{
            "Classification": "spark-env",
            "Properties": {},
            "Configurations": [{
                "Classification": "export",
                "Properties": {
                    "PYSPARK_PYTHON": "/usr/bin/python3",
                    "PYSPARK_DRIVER_PYTHON": "usr/bin/python3"
                }
            }]
        },
            {
                "Classification": "spark-hive-site",
                "Properties": {
                    "hive.metastore.client.factory.class": "com.amazonaws.glue.catalog.metastore"
                }
            },
            {
                "Classification": "spark-defaults",
                "Properties": {
                    "spark.submit.deployMode": "cluster",
                    "spark.speculation": "false",
                    "spark.sql.adaptive.enabled": "true",
                    "spark.serializer": "org.apache.spark.serializer.kryoSerializer"
                }
            },
            {
                "Classification": "spark",
                "Properties": {
                    "maximizeResourceAllocation": "true"
                }
            }
        ],

        StepConcurrencyLevel=1, # nao tem concorrencia; se > 1, os steps sao executados ao msm tempo

        Steps=[{
            'Name': 'Delta insert do ENEM',
            'ActionOnFailure': 'CONTINUE',
            'HadoopJarStep': {
                'Jar': 'command-runner.jar',
                'Args': ['spark-submit',
                         '--packages', 'io.delta:delta-core_2.12:1.0.0',
                         '--conf', 'spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension',
                         '--conf', 'spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog',
                         '--master', 'yarn',
                         '--deploy-mode', 'cluster',
                         's3://datalake-elby-igti-edc-tf/emr-code/pyspark/01_delta_spark_insert.py'
                        ]
            }
        },
        {
            'Name': 'Simulacao e upsert do ENEM',
            'ActionOnFailure': 'CONTINUE',
            'HadoopJarStep': {
                'Jar': 'command-runner.jar',
                'Args': ['spark-submit',
                         '--packages', 'io.delta:delta-core_2.12:1.0.0',
                         '--conf', 'spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension',
                         '--conf', 'spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog',
                         '--master', 'yarn',
                         '--deploy-mode', 'cluster',
                         's3://datalake-elby-igti-edc-tf/emr-code/pyspark/02_delta_spark_upsert.py'
                        ]
            }
        }],
    )

    return {
        'statusCode': 200,
        'body': f"Started job flow {cluster_id['JobFlowId']}"
    }