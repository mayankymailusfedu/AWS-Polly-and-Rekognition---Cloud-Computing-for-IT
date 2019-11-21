import boto3
from pprint import pprint
import image_helpers

def celeb(imgbytes):
    client = boto3.client('rekognition')

    # grab the image from online
    # imgurl = 'https://media1.popsugar-assets.com/files/thumbor/xptPz9chB_kMwxzqI9qMCZrK_YA/fit-in/1024x1024/filters:format_auto-!!-:strip_icc-!!-/2015/07/13/766/n/1922398/3d3a7ee5_11698501_923697884352975_2728822964439153485_n.jpg'
    # imgurl = 'http://media.comicbook.com/uploads1/2015/07/fox-comic-con-panel-144933.jpg'
    #imgurl = 'https://blog.njsnet.co/content/images/2017/02/trumprecognition.png'

    #imgbytes = image_helpers.get_image_from_url(imgurl)

    #imgfilename = 'image/1402693000020-450569482-10.jpg'
    # grab the image from local
    #imgbytes = image_helpers.get_image_from_file(imgfilename)

    rekresp = client.recognize_celebrities(Image={'Bytes': imgbytes})
    # pprint(rekresp['CelebrityFaces'])
    #for face in rekresp['CelebrityFaces']:
    #    print(face['Name'],'confidence:', face['MatchConfidence'], 'url:',face['Urls'])

    result = []
    for face in rekresp['CelebrityFaces']:
        result.append(face['Name'])

    return result
