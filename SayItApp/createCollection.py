import boto3
from pprint import pprint
import image_helpers

client = boto3.client('rekognition')

rekresp = client.create_collection(
    CollectionId='myCollection',
)

pprint(rekresp)

# {'CollectionArn': 'aws:rekognition:us-east-1:050122124972:collection/myCollection',
#  'FaceModelVersion': '2.0',
#  'ResponseMetadata': {'HTTPHeaders': {'connection': 'keep-alive',
#                                       'content-length': '124',
#                                       'content-type': 'application/x-amz-json-1.1',
#                                       'date': 'Sat, 25 Nov 2017 00:43:12 GMT',
#                                       'x-amzn-requestid': '9d729749-d179-11e7-a131-8fd57d6e1f6f'},
#                       'HTTPStatusCode': 200,
#                       'RequestId': '9d729749-d179-11e7-a131-8fd57d6e1f6f',
#                       'RetryAttempts': 0},
#  'StatusCode': 200}