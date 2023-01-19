import os
import time

import boto3

redshift_data_client = boto3.client("redshift-data")
# aws_redshift.CfnCluster(...).attr_id (for cluster name) is broken, so using endpoint address instead
REDSHIFT_CLUSTER_NAME = os.environ["REDSHIFT_ENDPOINT_ADDRESS"].split(".")[0]
REDSHIFT_USER = os.environ["REDSHIFT_USER"]
REDSHIFT_DATABASE_NAME = os.environ["REDSHIFT_DATABASE_NAME"]
REDSHIFT_SCHEMA_NAME_FOR_DYNAMODB_CDC = os.environ[
    "REDSHIFT_SCHEMA_NAME_FOR_DYNAMODB_CDC"
]
REDSHIFT_TABLE_NAME_FOR_DYNAMODB_CDC = os.environ[
    "REDSHIFT_TABLE_NAME_FOR_DYNAMODB_CDC"
]


def execute_sql_statement(sql_statement: str) -> None:
    response = redshift_data_client.execute_statement(
        ClusterIdentifier=REDSHIFT_CLUSTER_NAME,
        Database=REDSHIFT_DATABASE_NAME,
        DbUser=REDSHIFT_USER,
        Sql=sql_statement,
    )
    time.sleep(1)
    while True:
        response = redshift_data_client.describe_statement(Id=response["Id"])
        status = response["Status"]
        if status == "FINISHED":
            print(f"Finished executing the following SQL statement: {sql_statement}")
            return
        elif status in ["SUBMITTED", "PICKED", "STARTED"]:
            time.sleep(1)
        elif status == "FAILED":
            print(response)
            raise  ### figure out useful message in exception
        else:
            print(response)
            raise  ### figure out useful message in exception


def lambda_handler(event, context) -> None:
    sql_statements = [
        f'CREATE SCHEMA IF NOT EXISTS "{REDSHIFT_SCHEMA_NAME_FOR_DYNAMODB_CDC}";',
        f"""CREATE TABLE IF NOT EXISTS "{REDSHIFT_SCHEMA_NAME_FOR_DYNAMODB_CDC}"."{REDSHIFT_TABLE_NAME_FOR_DYNAMODB_CDC}" (
            id varchar(30) UNIQUE NOT NULL,
            details super,
            price float,
            shares integer,
            ticker varchar(10),
            ticket varchar(10),
            time super
        );""",  # hard coded columns
    ]
    for sql_statement in sql_statements:
        execute_sql_statement(sql_statement=sql_statement)
