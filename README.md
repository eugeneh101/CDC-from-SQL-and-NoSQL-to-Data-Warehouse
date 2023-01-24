* try restarting DMS migration task, check to see DMS task continues to run: yes
    * check to see if DMS runs given different RDS flavors
* check to see S3 expired files are deleted: yes
* set MySQL binary log retention hours: yes, used Trigger
* mysql -h cdcstack-rdsservicerdstocdctoredshiftf398d7a0-gvhlj93xg4n.c6ivt0xhpth.us-east-1.rds.amazonaws.com -u admin -p
    * mysql> call mysql.rds_show_configuration;
    * mysql> call mysql.rds_set_configuration("binlog retention hours", 24);
* connect to MySQL database in MySQL Workbench
* can connect with Redshift cluster with psycopg2
* It's possible to create the table 1 time for Redshift and RDS: yes, used Trigger
    * Can also consider using AwsCustomResource
* appears that "rds-data" API in boto3 is only for Aurora Serverless V1. Connecting to RDS endpoint is the standard approach. It appears you could use IAM authentication token
* Can turn off Publicly Accessible if put everything in VPC
* In real deployment, figure out VPC and use Secrets Manager 

* Redshift can copy directly from DynamoDB table
* DynamoDB can use Kinesis stream instead of DynamoDB stream
* AWS data pipeline and Glue are other ways to do CDC outside of DMS
* Redshift Spectrum serverless in S3, like Athena

* https://github.com/aws-samples/aws-dms-cdc-data-pipeline and https://github.com/aws-samples/aws-cdk-examples/tree/master/python
* https://github.com/miztiik/redshift-demo
