import os

import pymysql

RDS_HOST = os.environ["RDS_HOST"]
RDS_USER = os.environ["RDS_USER"]
RDS_PASSWORD = os.environ["RDS_PASSWORD"]
RDS_DATABASE_NAME = os.environ["RDS_DATABASE_NAME"]


def lambda_handler(event, context) -> None:
    """Currently only works with MySQL variant of RDS"""
    with pymysql.connect(
        host=RDS_HOST,
        user=RDS_USER,
        passwd=RDS_PASSWORD,
        db=RDS_DATABASE_NAME,
        connect_timeout=5,
        autocommit=True,  # needs be True for the statements to run successfully
    ) as conn, conn.cursor() as cursor:
        cursor.execute("call mysql.rds_show_configuration;")
        print("original `binlog retention hours`:", cursor.fetchone())

        cursor.execute("call mysql.rds_set_configuration('binlog retention hours', 24);")
        cursor.execute("""call mysql.rds_show_configuration;""")
        print("new `binlog retention hours`:", cursor.fetchone())
