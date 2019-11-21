import boto3
from pprint import pprint
import image_helpers

def search_faces(imgbytes):
    client = boto3.client('rekognition')
    #imgbytes=image_helpers.get_image_from_file(imgbyte)
    response = client.search_faces_by_image(CollectionId='myCollection', Image={'Bytes': imgbytes},FaceMatchThreshold=70)
    # return response

    str=""
    if len(response['FaceMatches'])==0 :
        str=str
    else:
        for r in response['FaceMatches']:
             str=str+r['Face']['ExternalImageId']+" "

    return str