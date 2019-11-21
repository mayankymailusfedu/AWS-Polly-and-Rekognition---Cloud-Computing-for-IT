I am creating tutorial on “Uses of Polly, Rekognition”.

I basically created a program that will describe the labels, print labels on the image, detect text, find celebrity, print the names of the celebrity on the image, find non-celebrity face (therefore, face stored in collection), Call AWS Polly to wish/greet and speak out these details.

“SayItApp” is the name of the project. When you open it in PyCharm, first run “createCollection.py” to create the collection, in which we will store the faces. Then run “addImageToCollection.py” to add faces to the collection. Run the “addImageToCollection.py” again with following changes:
imgfile = 'image/ 293af07.jpg';
rekresp = client.index_faces(CollectionId='myCollection',Image={'Bytes': imgbytes},ExternalImageId=' Phil_Ventura ',
      DetectionAttributes=['ALL'])


Now we are good to run the “labels_graphical.py”. Don’t run the “Doctests in labels_graphical.py”.

The “index.html” is the default page. There is a link of “Tutorial”, hover over it. The tutorial pages will be displayed.
