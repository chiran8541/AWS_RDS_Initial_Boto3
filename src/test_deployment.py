from src.client_factory import RDSClient
from src.rds import RDS

def get_rds():
    rds_client = RDSClient().get_client()
    rds = RDS(rds_client)
    return rds

def deploy_resources():
    rds_client = RDSClient().get_client()
    rds = RDS(rds_client)

    rds.create_postgresql_instance()
    print('creating RDS instances')


def describe_RDS():
    print(str(get_rds().describe_rds()))


def stop_database_instance():
    get_rds().stop_rds('mypostgresql')
    print('rds is stopped')

def db_snapshot():
    tags = [{'Key': 'Name', 'Value': 'db_snapshot'}]
    get_rds().take_backup_of_db('mypostgresql', 'myfirstsnapshot', tags)

def restore_snapshot():
    get_rds().restore_db_from_backup('mypostgresql', 'rds:mypostgresql-2021-09-10-21-30')

def delete_RDS_instances():
    get_rds().terminate_db_instance('mypostgresql')

if __name__ == '__main__':
    #deploy_resources()
    describe_RDS()
    #stop_database_instance()
    #db_snapshot()
    #restore_snapshot()
    #delete_RDS_instances()


