from google.appengine.ext import db
from google.appengine.ext import blobstore

class Paste(db.Model):
	title = db.StringProperty(multiline=False)
	content = db.TextProperty() #Supports more than 500 characters unlike string but can't be searched, any way around this?
	date = db.DateTimeProperty(auto_now_add=True)
	private = db.BooleanProperty(None,None,False)

class Image(db.Model, blobstore.BlobReferenceProperty):
	paste	= db.ReferenceProperty(Paste)
	img		= blobstore.BlobReferenceProperty()
	localID = db.IntegerProperty()
	shrunk	= db.BlobProperty()

#If your app has a Blobstore value, you must add the following code to get the query API to recognize the __BlobInfo__ kind 
# class BlobInfo(db.Expando):
    # @classmethod
    # def kind(cls):
        # return '__BlobInfo__'