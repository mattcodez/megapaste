import cgi
import mpDB

from google.appengine.ext import webapp
from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import run_wsgi_app

from mpDB import *

class ImgView(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self):
	imgKey = self.request.get('imgKey')
	if imgKey:
		if not blobstore.get(imgKey):
			self.error(500)
		else:
			self.send_blob(imgKey)
	else:
		shrinkKey = self.request.get('shrinkKey')
		shrinkImg = Image.get(db.Key(shrinkKey)).shrunk
		self.response.out.write(shrinkImg)
	
application = webapp.WSGIApplication(
                                     [('/imgview', ImgView)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()