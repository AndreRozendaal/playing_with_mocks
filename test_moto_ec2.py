import boto3
import pytest
from moto import mock_ec2


def get_client():
    return boto3.client("ec2", region_name="eu-west-1")

def create_ec2(ec2):
    image_response = ec2.describe_images()
    image_id = image_response["Images"][0]["ImageId"]

    instance_response = ec2.run_instances(
        InstanceType="t2.micro", MaxCount=1, MinCount=1, ImageId=image_id
    )

    return instance_response["Instances"][0]["InstanceId"]

def create_ec2_environment():
    ec2 = get_client()
    instanceid = create_ec2(ec2)
    return ec2, instanceid

def get_state(ec2, instanceid):

    # get id of created instance
    response = ec2.describe_instances(
        InstanceIds=[instanceid],
    )

    return response["Reservations"][0]["Instances"][0]["State"]["Name"]

@mock_ec2 
def test_create_ec2():
    (ec2, instanceid) = create_ec2_environment()
    state = get_state(ec2, instanceid)

    assert state == "running"

@mock_ec2
def test_stop_ec2():
    (ec2, instanceid) = create_ec2_environment()
    print(instanceid)
    ec2.stop_instances(InstanceIds=[instanceid])
    state = get_state(ec2, instanceid)

    assert state == "stopped"

@mock_ec2
def test_terminate_ec2():
    (ec2, instanceid) = create_ec2_environment()

    ec2.terminate_instances(InstanceIds=[instanceid])
    state = get_state(ec2, instanceid)

    assert state == "terminated"
