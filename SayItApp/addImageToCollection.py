import boto3
from pprint import pprint
import image_helpers

# imgurl = 'https://www.parrots.org/images/uploads/dreamstime_C_47716185.jpg'
# imgurl='https://blog.njsnet.co/content/images/2017/02/trumprecognition.png'
imgfile = 'image/DSC_0600_10kb.jpg';
imgbytes = image_helpers.get_image_from_file(imgfile)
#imgbytes = image_helpers.get_image_from_url(imgurl)

client = boto3.client('rekognition')
rekresp = client.index_faces(CollectionId='myCollection',Image={'Bytes': imgbytes},ExternalImageId='Mayank_Yadav',
      DetectionAttributes=['ALL'])

pprint(rekresp)

# Delete the Collection with collection id
# response = client.delete_collection(
#     CollectionId='myCollection'
#  )

# Display all the collection
# rekresp = client.list_collections()