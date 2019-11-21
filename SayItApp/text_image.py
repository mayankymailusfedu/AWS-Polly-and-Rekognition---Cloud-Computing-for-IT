import boto3
from pprint import pprint
import image_helpers


def textImage(imgbytes):
    client = boto3.client('rekognition')

    #imgurl = 'http://docs.aws.amazon.com/rekognition/latest/dg/images/text.png'
    #imgurl = 'https://image.slidesharecdn.com/howtooverlaytextonimagesjpgs-141214122828-conversion-gate01/95/how-to-overlay-text-on-images-5-simple-methods-1-638.jpg?cb=1433017251'
    #imgurl = 'https://lh3.ggpht.com/AIOlcNtjP5seRwQp62nUEpleulvRgvgMjTm9bR72uMQNJsJfp1O0Op1_ZXfnEYD5uA=h900'

    # grab the image from online
    #imgbytes = image_helpers.get_image_from_url(imgurl)

    rekresp = client.detect_text(Image={'Bytes': imgbytes})
    #pprint(rekresp['TextDetections'])
    imgString=""
    for img in rekresp['TextDetections']:
        imgString=imgString+img['DetectedText']+" "

    #pprint(imgString);
    half, rem = divmod(len(imgString), 2)
    frontA = imgString[:half + rem]
    backA = imgString[half + rem:]
    return frontA
    #pprint(', '.join(imgText))