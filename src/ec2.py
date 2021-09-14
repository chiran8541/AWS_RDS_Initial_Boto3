RDS_SECURITY_GROUP_NAME = "my-rds-public-sg"

class EC2:
    def __init__(self, client):
        self._client = client
        """ :type : pyboto3.ec2"""

    def create_security_group(self):
        print("Creating RDS security group with name " + RDS_SECURITY_GROUP_NAME)
        return self._client.create_security_group(
            GroupName=RDS_SECURITY_GROUP_NAME,
            Description='RDS security got public access',
            VpcId='vpc-cdd261b0'
        )
    def add_inbound_rule_to_SG(self, security_group_id):
        print('adding inbound access rule to security group: ' + security_group_id)
        self._client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 5432,
                    'ToPort': 5432,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]

                }
            ]
        )



