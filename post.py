import cgi
import mpDB

from google.appengine.ext import blobstore
from google.appengine.ext import webapp
from google.appengine.api import images
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import run_wsgi_app

from mpDB import *

class Pastings(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		paste = Paste()
		paste.title = self.request.get('title')
		paste.content = self.request.get('content')
		if (self.request.get('private')):
			paste.private = True

		imgCount = 1
		try:
			paste.put()
			for i in range(1,4):
				for upload in self.get_uploads('img' + str(i)):
					img = Image()
					img.paste = paste.key()
					img.img = upload.key()
					img.localID = i
					self.checkResize(img, upload.key(), True if self.request.get('thumb' + str(i)) == '1' else False)
					img.put()
		except:
			self.redirect('/upload_failure.html')
		
		self.redirect('/view?id=' + str(paste.key()))
			
	def checkResize(self, uploadedImg, bKey, thumb):
		#image dimension limits
		limitW = 256 if thumb else 1024
		limitH = 192 if thumb else 768
	
		#can't view dimensions of blobstore items so have to load part of the file to check
		data = blobstore.fetch_data(bKey, 0, 50000) 
		imgCheck = images.Image(data)
		if not(imgCheck.width > limitW or imgCheck.height > limitH):
			return
		
		img = images.Image(blob_key = str(bKey))
		if (imgCheck.width/limitW) > (imgCheck.height/limitH):
			newWidth = limitW
			newHeight = imgCheck.height * (limitW/imgCheck.width)
		else:
			newWidth = imgCheck.width * (limitH/imgCheck.height)
			newHeight = limitH
		
		img.resize(newWidth, newHeight)
		uploadedImg.shrunk = img.execute_transforms(output_encoding=images.JPEG)

application = webapp.WSGIApplication(
                                     [('/new', Pastings)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()