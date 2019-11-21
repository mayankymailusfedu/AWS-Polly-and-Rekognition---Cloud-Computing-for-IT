import boto3
from pprint import pprint
import image_helpers

client = boto3.client('rekognition')

imgurl = 'https://www.parrots.org/images/uploads/dreamstime_C_47716185.jpg'
imgurl='https://blog.njsnet.co/content/images/2017/02/trumprecognition.png'
imgurl = 'http://www.idothat.us/images/idothat-img/features/pool-patio-lanai/ft-pool-patio-lanai-2.jpg'
imgurl='http://sim01.in.com/4fc598f2c9f2c0cdc5e0decc188d8d10_ft_xl.jpg'
imgurl='https://i.pinimg.com/736x/eb/db/23/ebdb2370397a9d3af913bca9a2fa8117--pretty-nature-dick.jpg'
#imgurl='http://www.52dazhew.com/data/out/167/586898131-nature-wallpaper-hd.jpg'
# grab the image from online
imgbytes = image_helpers.get_image_from_url(imgurl)

#imgfilename = 'image/1402693000020-450569482-10.jpg'
# grab the image from local
#imgbytes = image_helpers.get_image_from_file(imgfilename)

# # grab the image from bucket
#s3 = boto3.resource('s3')
#fileName='DSC_0600_10kb.jpg'
#bucket='cf-templates-wud8nc2d49ce-us-east-1'
# client=boto3.client('rekognition')
#rekresp = client.detect_faces(Image={'S3Object':{'Bucket':bucket,'Name':fileName}},Attributes=['ALL'])


rekresp = client.detect_labels(Image={'Bytes': imgbytes},
                               MinConfidence=1)

pprint(rekresp)
#pprint(rekresp['Labels'])
print("Here What I see in the image:")
for label in rekresp['Labels']:
    print(label['Name'])
