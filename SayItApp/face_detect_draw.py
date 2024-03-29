from PIL import Image, ImageDraw
import boto3
from pprint import pprint
from io import BytesIO
import image_helpers

def bbox_to_coords(bbox, img_width, img_height):
    '''Given a BoundingBox map (from Rekognition)
       return the corresponding coords
       suitable for use with ImageDraw rectangle.'''
    upper_left_x = bbox['Left'] * img_width
    upper_y = bbox['Top'] * img_height
    bottom_right_x = upper_left_x + (bbox['Width'] * img_width)
    bottom_y = upper_y + (bbox['Height'] * img_height)
    return [upper_left_x, upper_y, bottom_right_x, bottom_y]

client = boto3.client('rekognition')

def acceptImagebytes(imagebytes):
    img = Image.open(BytesIO(imagebytes))
    (img_width, img_height) = img.size
    # prepare to draw on the image
    draw = ImageDraw.Draw(img)
    response = client.search_faces_by_image(CollectionId='myCollection', Image={'Bytes': imagebytes},
                                            FaceMatchThreshold=70)
    draw.rectangle(bbox_to_coords(response['SearchedFaceBoundingBox'], img_width, img_height),
                       outline=(0,200,0))
    del draw
    img.show()


#imgurl = 'http://media.comicbook.com/uploads1/2015/07/fox-comic-con-panel-144933.jpg'
#imgurl = 'https://blog.njsnet.co/content/images/2017/02/trumprecognition.png'

# imgurl = 'https://img.huffingtonpost.com/asset/59355ce52300003b00348d3f.jpeg?ops=scalefit_720_noupscale'
# imgfilename = 'image/maxresdefault-5-reasons-why-how-to-train-your-dragon-2-is-better-than-the-first-spoilers-jpeg-87341.jpg'
#
# imgbytes = image_helpers.get_image_from_url(imgurl)
#
#
# rekresp = client.detect_faces(Image={'Bytes': imgbytes},
#                               Attributes=['ALL'])
#
# # load the image in Pillow for processing
# img = Image.open(BytesIO(imgbytes))
#
# (img_width, img_height) = img.size
#
# # prepare to draw on the image
# draw = ImageDraw.Draw(img)
#
# pprint(rekresp)
# for facedeets in rekresp['FaceDetails']:
#     bbox = facedeets['BoundingBox']
#     draw.rectangle(bbox_to_coords(bbox, img_width, img_height),
#                    outline=(0,200,0))
# del draw

# img.show()
