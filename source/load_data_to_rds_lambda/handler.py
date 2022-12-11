import csv
import os

import pymysql

RDS_HOST = os.environ["RDS_HOST"]
RDS_USER = "admin"  ### hard coded
RDS_PASSWORD = "password"  ### hard coded
RDS_DATABASE_NAME = "rds_to_redshift_database"  ### hard coded
RDS_TABLE_NAME = "rds_cdc_table"


def lambda_handler(event, context):
    conn = pymysql.connect(
        host=RDS_HOST,
        user=RDS_USER,
        passwd=RDS_PASSWORD,
        db=RDS_DATABASE_NAME,
        connect_timeout=5,
    )
    with conn, conn.cursor() as cursor, open("txns.csv") as f:
        csv_reader = csv.reader(f)
        column_names = next(csv_reader)
        column_names = [
            column_name.replace(" ", "_").lower() for column_name in column_names
        ]
        csv_data = [tuple(row) for row in csv_reader]
        # print(csv_data)
        cursor.execute(
            "CREATE TABLE if not exists {rds_table_name} ({column_name_and_types});".format(
                rds_table_name=RDS_TABLE_NAME,
                column_name_and_types=", ".join(
                    f"{column_name} varchar(40)" for column_name in column_names
                ),
            )  # did not define a primary key
        )
        conn.commit()
        cursor.executemany(
            """
            INSERT INTO {rds_table_name} ({column_names})
            VALUES ({column_types});""".format(
                rds_table_name=RDS_TABLE_NAME,
                column_names=", ".join(column_names),
                column_types=", ".join(["%s"] * len(column_names)),
            ),
            csv_data,
        )
        conn.commit()
