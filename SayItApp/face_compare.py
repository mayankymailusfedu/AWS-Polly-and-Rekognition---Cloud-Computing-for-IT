import boto3
from pprint import pprint
import image_helpers

client = boto3.client('rekognition')

# bucket = 'bucket-name'
sourceFile = 'image/DSC_0600_10kb.jpg'
targetFile = 'image/IMG_20160402_155147.jpg'
# grab the image from local
imgsourcebytes = image_helpers.get_image_from_file(sourceFile)
imgtargetbytes = image_helpers.get_image_from_file(targetFile)

response = client.compare_faces(SimilarityThreshold=70,
                                SourceImage={'Bytes': imgsourcebytes},
                                TargetImage={'Bytes': imgtargetbytes})

for faceMatch in response['FaceMatches']:
    position = faceMatch['Face']['BoundingBox']
    confidence = str(faceMatch['Face']['Confidence'])
    print('The face at ' +
          str(position['Left']) + ' ' +
          str(position['Top']) +
          ' matches with ' + confidence + '% confidence')

pprint(response)

