import boto3
from pprint import pprint
import image_helpers
import face_detect_draw
from PIL import Image, ImageDraw
from io import BytesIO

def faceCompare(imgtargetbytes):
    client = boto3.client('rekognition')

    # bucket = 'bucket-name'
    sourceFile = 'https://blog.njsnet.co/content/images/2017/02/trumprecognition.png'
    #targetFile = 'image/102824056.jpg'
    #targetFile = 'image/IMG_20160402_155147.jpg'
    # grab the image from local
    imgsourcebytes = image_helpers.get_image_from_url(sourceFile)
    #imgtargetbytes = image_helpers.get_image_from_url(targetFile)

    response = client.compare_faces(SimilarityThreshold=70,
                                    SourceImage={'Bytes': imgsourcebytes},
                                    TargetImage={'Bytes': imgtargetbytes})

    # for faceMatch in response['FaceMatches']:
    #     position = faceMatch['Face']['BoundingBox']
    #     confidence = str(faceMatch['Face']['Confidence'])
    #     print('The face at ' +
    #           str(position['Left']) + ' ' +
    #           str(position['Top']) +
    #           ' matches with ' + confidence + '% confidence')


    for faceMatch in response['FaceMatches']:
        if faceMatch == "":
            pprint("The face does not match")
        else:
            pprint("The face matches")
            pprint(faceMatch['Similarity'])
            pprint(faceMatch['Face']['BoundingBox'])
            img = Image.open(BytesIO(imgtargetbytes))
            (img_width, img_height) = img.size
            draw = ImageDraw.Draw(img)
            draw.rectangle(face_detect_draw.bbox_to_coords(faceMatch['Face']['BoundingBox'], img_width, img_height),
                           outline=(0, 200, 0))
            del draw
            img.show()

