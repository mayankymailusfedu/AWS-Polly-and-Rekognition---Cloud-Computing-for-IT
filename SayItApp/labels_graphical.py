from PIL import Image, ImageDraw, ImageFont
import boto3
from pprint import pprint, pformat
from io import BytesIO
import image_helpers
import celebs
import face_detect
import text_image
import apptext
import datetime
import searchFacesInCollection
import face_detect_draw


# --------------------------------------------------------------------
# DO NOT CHANGE THESE FUNCTIONS


def format_text(text, columns):
    '''
    Returns a copy of text that will not span more than the specified number of columns
    :param text: the text
    :param columns: the maximum number of columns
    :return: the formatted text
    '''
    # format the text to fit the specified columns
    import re
    text = re.sub('[()\']', '', pformat(text, width=columns))
    text = re.sub('\n ', '\n', text)
    return text


def text_rect_size(draw, text, font):
    '''
    Returns the size of the rectangle to be used to
    draw as the background for the text
    :param draw: an ImageDraw.Draw object
    :param text: the text to be displayed
    :param font: the font to be used
    :return: the size of the rectangle to be used to draw as the background for the text
    '''
    (width, height) = draw.multiline_textsize(text, font=font)
    return (width * 1.1, height * 1.3)


def add_text_to_img(img, text, pos=(0, 0), color=(0, 0, 0), bgcolor=(255, 255, 255, 128),
                    columns=60,
                    font=ImageFont.truetype('ariblk.ttf', 22)):
    '''
    Creates and returns a copy of the image with the specified text displayed on it
    :param img: the (Pillow) image
    :param text: the text to display
    :param pos: a 2 tuple containing the xpos, and ypos of the text
    :param color: the fill color of the text
    :param bgcolor: the background color of the box behind the text
    :param columns: the max number of columns for the text
    :param font: the font to use
    :return: a copy of the image with the specified text displayed on it
    '''

    # make a blank image for the text, initialized to transparent text color
    txt_img = Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_img)

    # format the text
    text = format_text(text, columns)
    # get the size of the text drawn in the specified font
    (text_width, text_height) = ImageDraw.Draw(img).multiline_textsize(text, font=font)

    # compute positions and box size
    (xpos, ypos) = pos
    rwidth = text_width * 1.1
    rheight = text_height * 1.4
    text_xpos = xpos + (rwidth - text_width) / 2
    text_ypos = ypos + (rheight - text_height) / 2

    # draw the rectangle (slightly larger) than the text
    draw.rectangle([xpos, ypos, xpos + rwidth, ypos + rheight], fill=bgcolor)

    # draw the text on top of the rectangle
    draw.multiline_text((text_xpos, text_ypos), text, font=font, fill=color)

    del draw # clean up the ImageDraw object
    return Image.alpha_composite(img.convert('RGBA'), txt_img)


def get_pillow_img(imgbytes):
    """
    Creates and returns a Pillow image from the given image bytes
    :param imgbytes: the bytes of the image
    """
    return Image.open(BytesIO(imgbytes))

# END DO NOT CHANGE SECTION
# --------------------------------------------------------------------

def get_labels(img, confidence=50):
    """
    Gets the labels from AWS Rekognition for the given image
    :param img: either the image bytes or a string that is the URL or filename for an image
    :param confidence: the confidence level (defaults to 50)

    >>> get_labels('http://www.idothat.us/images/idothat-img/features/pool-patio-lanai/ft-pool-patio-lanai-2.jpg')
    [{'Name': 'Pool', 'Confidence': 96.66264343261719}, {'Name': 'Water', 'Confidence': 96.66264343261719}, {'Name': 'Resort', 'Confidence': 76.01207733154297}, {'Name': 'Swimming Pool', 'Confidence': 76.01207733154297}, {'Name': 'Balcony', 'Confidence': 66.56996154785156}, {'Name': 'Patio', 'Confidence': 62.89345169067383}, {'Name': 'Flagstone', 'Confidence': 59.46694564819336}, {'Name': 'Backyard', 'Confidence': 56.5162467956543}, {'Name': 'Yard', 'Confidence': 56.5162467956543}, {'Name': 'Path', 'Confidence': 52.408050537109375}, {'Name': 'Sidewalk', 'Confidence': 52.408050537109375}, {'Name': 'Walkway', 'Confidence': 52.408050537109375}, {'Name': 'Alley', 'Confidence': 50.79618835449219}, {'Name': 'Alleyway', 'Confidence': 50.79618835449219}, {'Name': 'Road', 'Confidence': 50.79618835449219}, {'Name': 'Street', 'Confidence': 50.79618835449219}, {'Name': 'Town', 'Confidence': 50.79618835449219}, {'Name': 'Plant', 'Confidence': 50.6763801574707}]

    >>> get_labels('http://www.idothat.us/images/idothat-img/features/pool-patio-lanai/ft-pool-patio-lanai-2.jpg', 90)
    [{'Name': 'Pool', 'Confidence': 96.66264343261719}, {'Name': 'Water', 'Confidence': 96.66264343261719}]
    """
    # replace pass below with your implementation
    client = boto3.client('rekognition')
    imgbytes = image_helpers.get_image(img)
    rekresp = client.detect_labels(Image={'Bytes': imgbytes},
                                   MinConfidence=confidence)

    name = []
    for label in rekresp['Labels']:
        name.append({'Name' : label['Name'],'Confidence':label['Confidence']})
    print(name)
    return name

def bbox_to_coords(bbox, img_width, img_height):
    '''Given a BoundingBox map (from Rekognition)
       return the corresponding coords
       suitable for use with ImageDraw rectangle.'''
    upper_left_x = bbox['Left'] * img_width
    upper_y = bbox['Top'] * img_height
    bottom_right_x = upper_left_x + (bbox['Width'] * img_width)
    bottom_y = upper_y + (bbox['Height'] * img_height)
    return [upper_left_x, upper_y, bottom_right_x, bottom_y]

def label_image(img, confidence=50):
    '''
    Creates and returns a copy of the image, with labels from Rekognition displayed on it
    :param img: a string that is either the URL or filename for the image
    :param confidence: the confidence level (defaults to 50)
    :return: a copy of the image, with labels from Rekognition displayed on it
    '''
    # replace pass below with your implementation
    imgbytes=image_helpers.get_image(img)
    imgpillow = get_pillow_img(imgbytes)
    nametext = []
    name=get_labels(img,confidence)
    for label in name:
        nametext.append(label['Name'])
    text=', '.join(nametext)
    pprint(text)
    hour=datetime.datetime.now().time().hour
    if hour<=10:
        texttpspeech = "Good Morning. "
    elif hour>10 and hour<=16:
        texttpspeech = "Good Afternoon. "
    else:
        texttpspeech = "Good Evening. "
    texttpspeech=texttpspeech+"The image contains : "+text+". "
    text_on_image = text_image.textImage(imgbytes)
    if text_on_image == "" or text_on_image == " ":
        texttpspeech = texttpspeech
    else:
        texttpspeech = texttpspeech + " The text written on image is " + text_on_image + ". "
    myList = ['Human','People','Person','Female','Male','Girl','Boy','Woman','Man','Face','Laughing','Smile','Blonde','Crowd']
    flag = 0
    celebrity = []
    for i in myList:
        if flag == 0 and texttpspeech.__contains__(i):
            flag=1
            #pprint("Text found "+i)
            texttpspeech = texttpspeech + (str)(face_detect.describe_faces(imgbytes))
            celebrity = celebs.celeb(imgbytes)
            if not celebrity:
                foundFaces=searchFacesInCollection.search_faces(imgbytes)
                if foundFaces=="":
                    texttpspeech=texttpspeech
                else:
                    foundFaces=foundFaces.replace("_"," ")
                    texttpspeech = texttpspeech + "I can recognize the personal as "+ foundFaces+". "
                    face_detect_draw.acceptImagebytes(imgbytes)
            else:
                texttpspeech = texttpspeech + "I can recognize the personal as : " + ', '.join(celebrity) + '. '
                text = ', '.join(celebrity)
            break
    apptext.text_to_speech(texttpspeech,'Amy')

    return add_text_to_img(imgpillow,text)



if __name__ == "__main__":
    # can't use input since PyCharm's console causes problems entering URLs
    # img = input('Enter either a URL or filename for an image: ')
    img = 'https://blog.njsnet.co/content/images/2017/02/trumprecognition.png'
    img = 'http://cdn.cnn.com/cnnnext/dam/assets/170712202622-01-donald-trump-0712.jpg'
    img = 'https://blog.njsnet.co/content/images/2017/02/trumprecognition.png'
    # img= 'image/DSC_0600_10kb.jpg'
    img = 'image/293af07.jpg'
    # img = 'image/IMG_20171108_124915.jpg'
    #img = 'https://www.w3schools.com/css/trolltunga.jpg'
    #img='https://i.pinimg.com/736x/eb/db/23/ebdb2370397a9d3af913bca9a2fa8117--pretty-nature-dick.jpg'
    #img='http://www.52dazhew.com/data/out/167/586898131-nature-wallpaper-hd.jpg'
    #img = 'http://ww2.eclipseadvantage.com/images/Photos/people_resized.jpg'
    #img = 'http://epilepsyu.com/wp-content/uploads/2014/01/happy-people-1050x600.jpg'
    #img = 'https://timeincsecure-a.akamaihd.net/rtmp_uds/416418724/201709/102/416418724_5563555239001_5563565873001-vs.jpg?pubId=416418724&videoId=5563565873001'
    #img = 'http://s2.thingpic.com/images/rc/bQEtyDiwGtiben3qiCxw7emX.png'
    #img = 'https://peopleprogram.wiscweb.wisc.edu/wp-content/uploads/sites/118/2017/06/PEOPLE-Recognition-Banquet-20170721_01-4-1600x500.jpg'


    labelled_image = label_image(img)
    labelled_image.show()

