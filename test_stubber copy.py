import datetime
import botocore.session
from botocore.stub import Stubber

def test_hi():
    s3 = botocore.session.get_session().create_client('s3')
    stubber = Stubber(s3)

    response = {
        'IsTruncated': False,
        'Name': 'test-bucket',
        'MaxKeys': 1000, 'Prefix': '',
        'Contents': [{
            'Key': 'test.txt',
            'ETag': '"abc123"',
            'StorageClass': 'STANDARD',
            'LastModified': datetime.datetime(2016, 1, 20, 22, 9),
            'Owner': {'ID': 'abc123', 'DisplayName': 'myname'},
            'Size': 14814
        }],
        'EncodingType': 'url',
        'ResponseMetadata': {
            'RequestId': 'abc123',
            'HTTPStatusCode': 200,
            'HostId': 'abc123'
        },
        'Marker': ''
    }

    response2 = {
    'Location': 'string'
}

    expected_params = {'Bucket': 'test-bucket'}
    expected_params2 = {'Bucket': 'test-bucket2'}
    stubber.add_response('create_bucket', response2, expected_params2)
    #stubber.add_response('list_objects', response, expected_params)
    stubber.activate()

    service_response2 = s3.create_bucket(Bucket='test-bucket2')
    service_response = s3.list_objects(Bucket='test-bucket2')
    print(service_response)

  
    assert service_response == response