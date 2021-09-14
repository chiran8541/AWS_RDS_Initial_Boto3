from src.client_factory import EC2Client
from src.ec2 import EC2
RDS_DB_SUBNET_NAME = 'my-rds-subnet-group'
class RDS:
    def __init__(self, client):
        self._client = client
        """ :type : pyboto3.rds """

    def create_postgresql_instance(self):
        print("Creating Amazon RDS PostgreSQL DB Instances...")

        security_group_id= self.create_db_security_group_and_add_rules()

        #create subnet
        self.create_db_subnet_group()
        print('creating DB subnet group')

        self._client.create_db_instance(
            DBName='MyPostgreSqlDB',
            DBInstanceIdentifier='mypostgresql',
            MasterUsername='postgresql',
            MasterUserPassword='postgresqlpassword',
            DBInstanceClass='db.t2.micro',
            StorageType='gp2',
            Engine='postgres',
            EngineVersion='9.6.9',
            Port=5432,
            AllocatedStorage=20,
            MultiAZ=False,
            PubliclyAccessible=True,
            VpcSecurityGroupIds=[security_group_id],
            DBSubnetGroupName=RDS_DB_SUBNET_NAME,
            Tags=[
                {
                    'Key': 'Name',
                    'Value': 'My_RDS_Postgres_Instance'
                }
            ]
        )

    def describe_rds(self):
        print('describing RDS instances')
        return self._client.describe_db_instances()
    # stopping the instance
    def stop_rds(self, db_identifier):
        print('stopping the instance')
        return self._client.stop_db_instance(DBInstanceIdentifier=db_identifier)

    #taking backup

    def take_backup_of_db(self, db_identifier, db_snapshot_identifier, tags):
        print('taking backup of our RDS instance')
        return self._client.create_db_snapshot(
            DBInstanceIdentifier=db_identifier,
            DBSnapshotIdentifier=db_snapshot_identifier,
            Tags=tags
        )
    # restoring db snapshot
    def restore_db_from_backup(self, db_identifier, db_snapshot_identifier):
        print('restoring db from snapshot')
        return self._client.restore_db_instance_from_db_snapshot(
            DBInstanceIdentifier=db_identifier,
            DBSnapshotIdentifier=db_snapshot_identifier
        )
    # terminating(deleting) the RDS db instance
    def terminate_db_instance(self, db_identifier):
        print('terminating the db instance')
        return self._client.delete_db_instance(
            DBInstanceIdentifier=db_identifier,
            SkipFinalSnapshot=True
        )

    def create_db_subnet_group(self):
        print('creating RDS subnet groups' + RDS_DB_SUBNET_NAME)
        self._client.create_db_subnet_group(
            DBSubnetGroupName= RDS_DB_SUBNET_NAME,
            DBSubnetGroupDescription='My own subnet group for RDS',
            SubnetIds=['subnet-5bc4a67a', 'subnet-467e1920', 'subnet-91722b9f', 'subnet-38268d09', 'subnet-e2eed9af', 'subnet-05b2d25a']

        )


    def create_db_security_group_and_add_rules(self):
        ec2_client = EC2Client().get_client()
        ec2 = EC2(ec2_client)

        # create security group
        security_group = ec2.create_security_group()


        # get id of Security group
        security_group_id = security_group['GroupId']
        print(security_group_id)
        print(type(security_group_id))
        print('created RDS security group with ID ' + security_group_id)

        # add public access rule to sg
        ec2.add_inbound_rule_to_SG(security_group_id)
        print('added inbound public access rule to SG with ID' + security_group_id)

        return security_group_id





